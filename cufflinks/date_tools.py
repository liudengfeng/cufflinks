import datetime as dt
import pandas as pd


def getDatefromDate(date, delta, strfmt='%Y%m%d'):
    if type(date) == str:
        date = stringToDate(date, strfmt)
    return (date + dt.timedelta(delta)).strftime(strfmt)


def getDateFromToday(delta, strfmt='%Y%m%d'):
    """ Returns a string that represents a date n numbers of days from today.
    Parameters:
    -----------
        delta : int 
            number of days
        strfmt : string
            format in which the date will be represented
    """
    return (dt.date.today() + dt.timedelta(delta)).strftime(strfmt)


def stringToDate(stringDate, strfmt='%Y%m%d'):
    """ Converts a string format date into datetime
    Parameters:
    -----------
        stringDate : string 
            date in string format
        strfmt : string
            format in which the input date is represented
    """
    return dt.datetime.strptime(stringDate, strfmt).date()


def intToDate(intDate):
    """ Converts an int format date into datetime
    Parameters:
    -----------
        intDate : int
            date in int format
    Example:
        intDate(20151023)
    """
    return stringToDate(str(intDate))


def dateToInt(date, strfmt='%Y%m%d'):
    """ Converts a datetime date into int
    Parameters:
    -----------
        date : datetime
            date in datetime format
        strfmt : string
            format in which the int date will be generated
    Example:
        dateToInt(dt.date(2015,10,23),'%Y')
    """
    return int(date.strftime(strfmt))


def dateToString(date, strfmt='%Y%m%d'):
    return dt.datetime.strftime(date, strfmt)


def stringToString(date, from_strfmt='%d%b%y', to_strfmt='%Y%m%d'):
    return dt.datetime.strftime(stringToDate(date, from_strfmt), to_strfmt)


def infer_holidays(date_idx):
    """推断dates期间假日列表

    Args:
        date_idx (date_like): 类似日期对象

    Returns:
        list: 假日列表【除周六、周日外的非工作日】

    Examples:
    >>> from zipline.data.localdata import fetch_single_equity
    >>> df = fetch_single_equity('000001','2019-12-31','2020-04-01')
    >>> date_idx = df['date'].values
    >>> infer_holidays(date_idx)
    ['2020-01-01',
    '2020-01-24',
    '2020-01-27',
    '2020-01-28',
    '2020-01-29',
    '2020-01-30',
    '2020-01-31']
    """
    dt_fmt = r"%Y-%m-%d"
    idx = sorted(date_idx)
    start, end = idx[0], idx[-1]
    full_working = pd.date_range(start, end, freq='B', normalize=True)
    holidays = full_working.difference(pd.to_datetime(date_idx))
    holidays = [d.strftime(dt_fmt) for d in holidays]
    return holidays


def _is_date_like(x):
    """简单判断是否为类似date对象"""
    try:
        pd.to_datetime(x)
        return True
    except Exception:
        return False


def infer_xdate_fmt(x):
    """根据delta推断日期格式"""
    x = pd.to_datetime(x)
    d_min = x.min()
    d_max = x.max()
    delta = d_max - d_min
    if delta > pd.Timedelta(5*12*365, unit='days'):
        return r"%Y年%m月"
    elif delta > pd.Timedelta(5, unit='days'):
        return r"%Y年%m月%d日"
    if delta > pd.Timedelta(5, unit='hours'):
        return r"%m月%d日 %H"
    if delta > pd.Timedelta(5, unit='minutes'):
        return r"%d日 %H:%M"
    return r"%H:%M %S.%f"


def get_xdata(figure):
    """提取图中x数据"""
    x = []
    for t in figure.data:
        x.extend(list(t['x']))
    return sorted(set(x))


def autofmt_xdate_cn(figure, fmt=None, rotation=-30, hide=None):
    """标注x轴中文日期格式"""
    x = get_xdata(figure)
    if not _is_date_like(x):
        return figure
    if fmt is None:
        fmt = infer_xdate_fmt(x)
    if rotation != 0:
        fmt = fmt.replace('<br>', '')
    if hide == 'all':
        holidays = infer_holidays(x)
        figure.update_xaxes(
            tickformat=fmt,
            tickangle=rotation,
            tickfont=dict(size=12),
            rangebreaks=[
                dict(bounds=["sat", "mon"]),  # hide weekends
                dict(values=holidays)  # hide holidays
            ],
        )
    elif hide == 'weekend':
        figure.update_xaxes(
            tickformat=fmt,
            tickangle=rotation,
            tickfont=dict(size=12),
            rangebreaks=[
                dict(bounds=["sat", "mon"]),  # hide weekends
            ],
        )        
    else:
        figure.update_xaxes(
            tickformat=fmt,
            tickangle=rotation,
            tickfont=dict(size=12),
        )        
    return figure

"""
时间序列蜡烛图、美国线辅助处理模块

假设前提：
    1. 数据框`index`为时间`DatetimeIndex`;
    2. 不处理`rangeslider`;
"""

import pandas as pd
import numpy as np
import plotly.graph_objs as go


def get_xtick(x, percentile, ts_fmt):
    tickvals = []
    ticktext = []
    idx = np.percentile(range(len(x)), percentile).astype(int)
    # 取唯一值
    idx = pd.Series(idx).drop_duplicates().values
    for i in idx:
        tickvals.append(i)
        ticktext.append(pd.Timestamp(x[i]).strftime(ts_fmt))
    return tickvals, ticktext


def _fixed_layout(self, percentile=[5, 25, 50, 75, 95], ts_fmt=r'%Y-%m-%d'):
    tickvals, ticktext = get_xtick(self.index.values, percentile, ts_fmt)
    return dict(
        xaxis=dict(
            tickmode='array',
            tickvals=tickvals,
            ticktext=ticktext,
        )
    )


def get_figure(self, kind):
    if kind == 'candlestick':
        class_ = go.Candlestick
    else:
        class_ = go.Ohlc
    trace = class_(
        open=self['open'].values.tolist(),
        high=self['high'].values.tolist(),
        low=self['low'].values.tolist(),
        close=self['close'].values.tolist(),
        text=self.index,  # 将日期添加到悬停文本
    )

    layout = _fixed_layout(self)
    data = [trace]

    return go.Figure(data=data, layout=layout)

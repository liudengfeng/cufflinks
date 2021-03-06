"""
时间序列蜡烛图、美国线辅助处理模块

假设前提：
    1. 数据框`index`为时间`DatetimeIndex`;
"""

import pandas as pd
import numpy as np
import plotly.graph_objs as go


def get_xtick(x, locs, percentile, ts_fmt):
    tickvals = []
    ticktext = []
    idx = np.percentile(
        list(range(locs[0], locs[1]+1)), percentile).astype(int)
    # 取唯一值
    idx = pd.Series(idx).drop_duplicates().values
    for i in idx:
        tickvals.append(i)
        ticktext.append(pd.Timestamp(x[i]).strftime(ts_fmt))
    return tickvals, ticktext


def _fixed_layout(self, locs, percentile=[5, 25, 50, 75, 95], ts_fmt=r'%Y-%m-%d'):
    tickvals, ticktext = get_xtick(self.index.values, locs, percentile, ts_fmt)
    return dict(
        xaxis=dict(
            tickmode='array',
            tickvals=tickvals,
            ticktext=ticktext,
            # 默认不显示
            rangeslider=dict(
                visible=False,
            ),
            rangeselector=dict(
                visible=False,
            ),
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

    layout = _fixed_layout(self, (0, len(self)))
    data = [trace]

    return go.Figure(data=data, layout=layout)

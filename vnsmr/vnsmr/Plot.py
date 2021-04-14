from vnsmr import DataLoader
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import vnsmr.utils as utils
import pandas as pd

def _vnsmr_candle_stick_source(symbol,
                               start_date, end_date,
                               colors=['blue', 'red'],                                
                                 width=800, height=600,
                                 show_vol=True,
                                 data_source='VND',
                                 **kargs):
    loader = DataLoader.DataLoader(symbol, start_date, end_date, minimal=True, data_source=data_source)
    data = loader.download()
    symbol = list(data.columns.levels[1])[0]
    data.columns = ['high', 'low', 'open', 'close', 'adjust', 'volume']
    title = '{} stock price & volume from {} to {}'.format(symbol, start_date, end_date)
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02, row_heights=[0.6, 0.4])

    fig.append_trace(go.Candlestick(
        x=data.index,
        open=data['open'], high=data['high'],
        low=data['low'], close=data['close'],
        increasing_line_color=colors[0],
        decreasing_line_color=colors[1]),
        row=1, col=1)

    if show_vol:
        fig.append_trace(go.Bar(
            x=data.index,
            y=data['volume'],
            name='Volume',
            row=2, col=1
            ))

        fig.update_layout(
            title=title,
            yaxis_title='Price',
            xaxis_title='Date',
            width=width,
            height=height,
            showlegend=False
            )

        fig.show()

def _vnsmr_candle_stick(data,
                        title=None,
                        xlab='Date', ylab='Price',
                        start_date=None, end_date=None,
                        colors=['blue', 'red'],
                        width=800, height=600,
                        show_vol=True,
                        data_source='VND',
                        **kargs):
    # download data from source
    if isinstance(data, str):
       _vnsmr_candle_stick_source(symbol=data, start_date=start_date, end_date=end_date,
                                     colors=colors, width=width,
                                     height=height, show_vol=show_vol,
                                     data_source=data_source)
    else:
        if show_vol:
            assert utils._isOHLCV(data)
            defau_cols = ['high', 'low', 'open', 'close', 'volume']
            data = data[defau_cols].copy()
            data.columns = defau_cols
        else:
            assert utils._isOHLC(data)
            defau_cols = ['high', 'low', 'open', 'close']
            data = data[defau_cols].copy()
            data.columns = defa_cols

        x = data.index

        if not isinstance(x, pd.core.indexes.datetimes.DatetimeIndex):
            raise IndexError('index of dataframe must be DatetimeIndex!')

        if start_date is None:
            start_date = max(data.index)
        if end_date is None:
            end_date = max(data.index)

        fig = make_subplots(rows=2, cols=1, share_xaxes=True, vertical_spacing=0.02, row_heights=[0.6,0.4])

        fig.append_trace(go.Candlestick(
            x=x,
            open=data['open'], high=data['high'],
            low=data['low'], close=data['close'],
            increasing_line_color=colors[0],
            decreasing_line_color=colors[1]),
            row=1, col=1)

        if show_vol:
            fig.append_trace(go.Bar(
                x=x,
                y=data['volume'],
                name='Volume'),
                row=2, col=1)

        fig.update_layout(
            title=title,
            yaxis_title=xlab,
            xaxis_title=ylab,
            showlegend=False
            )

        fig.show()

#_vnsmr_candle_stick_source('VND', '2021-01-10', '2021-04-10', show_vol=False)
_vnsmr_candle_stick('VNINDEX', None, xlab='Date', ylab='Price',  start_date = '2021-01-10', end_date='2021-04-10', show_vol=True, data_source='CAFE')

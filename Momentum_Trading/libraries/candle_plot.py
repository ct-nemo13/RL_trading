import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os


def candle_plot(self):

    'Extract the Data Frame to plot candle chart.'
    self.df_for_plot = self.df[(self.start_time_index_in_int-1):self.end_time_int_index]
    
    df = self.df_for_plot
    
    
    
    
    
    'Define colour'
    colors = []
    for i in range(len(df)):
        if df.iloc[i]['close'] >= df.iloc[i]['open']:
            colors.append('green')
        else:
            colors.append('red')
    
    
    'Create subplot with two rows i.e., Price and Volume'
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.25,
                        subplot_titles=('Stock Price: ' + self.selected_stock , 'Trade Volume:' + self.selected_stock))
    
    
    'Make the Price Chart'
    fig.add_trace(go.Candlestick(x=df.index,
                                 open=df['open'],
                                 high=df['high'],
                                 low=df['low'],
                                 close=df['close'],
                                 name='Price',
                                 increasing_line_color='green',
                                 decreasing_line_color= 'red'),
                  row=1, col=1)
    
    
    'Buy signal plotting'
    buy_signals = df[df['action'] > 0]
    fig.add_trace(go.Scatter(x=buy_signals.index, y=buy_signals['execution_price'],
                             mode='markers',
                             marker=dict(color='green', symbol='triangle-up', size=10),
                             name='Buy Signals'),
                  row=1, col=1)
    
    
    'Sell signal plotting'
    sell_signals = df[df['action'] < 0]
    fig.add_trace(go.Scatter(x=sell_signals.index, y=sell_signals['execution_price'],
                             mode='markers',
                             marker=dict(color='red', symbol='triangle-down', size=10),
                             name='Sell Signals'),
                  row=1, col=1)
    
    
    'Volume plotting'
    fig.add_trace(go.Bar(x=df.index, y=df['volume'],
                         name='Volume',
                         marker=dict(color=colors)),
                  row=2, col=1)
    
    'Update Layout'
    fig.update_layout(yaxis1=dict(title='Price'),
                      yaxis2=dict(title='Volume', rangemode='tozero')
                      )
    
    'Folder Path to save plot'
    output_folder = self.dir
    
    'Save the HTML Plot'
    fig.write_html(os.path.join(output_folder, 'test_result_'+ self.selected_stock + '.html'))
    
    'Show the Plot'
    #fig.show(renderer="browser")

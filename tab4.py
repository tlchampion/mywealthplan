import helpers
import hvplot.pandas
import pandas as pd

from matplotlib.figure import Figure
from matplotlib import cm
from matplotlib.backends.backend_agg import FigureCanvas 



def make_chart(investment, weights, stocks):
#     weights = weights['weight']
#     allocation = [w * investment for w in weights]
#     amount = allocation/stocks.iloc[0]
#     stock_value = stocks * amount
#     stock_value = stock_value.sum(axis=1).reset_index().rename(columns={0:"Total Value ($)"})
#     plot = stock_value.hvplot.line(x="Date", height=500,width=1000)
#     return plot

    weights = weights['weight']
    allocation = [w * investment for w in weights]
    amount = allocation/stocks.iloc[0]
    stock_value = stocks * amount
    stock_value = stock_value.sum(axis=1).reset_index().rename(columns={0:"Total Value ($)"}).set_index('Date')
    plot_title = "title"
    fig0 = Figure(figsize=(16,8))
    ax0 = fig0.subplots()

    chart = ax0.plot(stock_value['Total Value ($)'])

    ax0.set_title(plot_title)
 
    return fig0
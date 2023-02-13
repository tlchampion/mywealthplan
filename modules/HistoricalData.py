import pandas as pd
from bokeh.palettes import Category20c, Category20
from bokeh.plotting import figure
from bokeh.transform import cumsum
from math import pi
import modules.helpers as helpers
import numpy as np

answers_dict = helpers.get_answers()






# def make_pie(data):
#     data = data.copy()
#     data = data.reset_index().rename(columns={'index': 'stock'})
#     data['angle'] = data['weight']/data['weight'].sum() * 2*pi
#     data['color'] = Category20c[data.shape[0]]
#     data['percent'] = data['weight'] * 100

#     p = figure(plot_height=350, title="Portfolo Distribution", toolbar_location=None,
#                tools="hover", tooltips="@stock: @percent%", x_range=(-0.5, 1.0))

#     r = p.wedge(x=0, y=1, radius=0.4,
#             start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
#             line_color="white", fill_color='color', legend_field='stock', source=data)

#     p.axis.axis_label=None
#     p.axis.visible=False
#     p.grid.grid_line_color = None
#     return p

def make_pie(data):
    data = data.copy()
    # data = data.reset_index().rename(columns={'index': 'stock'})
    data['angle'] = data['weight']/data['weight'].sum() * 2*pi
    data['color'] = Category20c[data.shape[0]]
    data['percent'] = data['weight'] * 100

    p = figure(plot_height=350, title="Portfolo Distribution", toolbar_location=None,
               tools="hover", tooltips="@category: @percent%", x_range=(-0.5, 1.0))

    r = p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend_field='category', source=data)

    p.axis.axis_label=None
    p.axis.visible=False
    p.grid.grid_line_color = None
    return p

def make_weight_chart(weight):
    w = weight.copy()
    w['Percent Allocation'] = w['weight'] * 100
    w = w.reset_index().drop(['weight', 'index'], axis=1).set_index('category')
    #w = w.drop(['weight', 'category'], axis=1)
    return w


def get_cum_returns(stocks, market, weights):
    #pull adjclose figures from portfolio performance and market performance
    stock_df, market_df = helpers.get_adjclose(stocks, market)
    
    #get weights for portfolio assets
    stock_weights = np.array(weights['weight'].to_list())
    
    #calculate portfolio return factoring in weights
    stock_daily_returns = stock_df.pct_change().dropna()
    portfolio_returns = pd.DataFrame(stock_daily_returns.dot(stock_weights)).rename(columns={0: 'adjclose'})
    
    #calculate market daily return
    market_daily_returns = market_df.pct_change().dropna()
    
    #calculate market and portfolio cumulative return
    df_market_cum_returns = (1 + market_daily_returns).cumprod()
    df_port_cum_returns = (1 + portfolio_returns).cumprod()
    
    return df_port_cum_returns, df_market_cum_returns, portfolio_returns
    
    
def make_comparison_chart(port_cum_return, market_cum_return):

    ax = port_cum_returns.plot(figsize=(10,5), title="Cumulative returns of Conservative Portfolio vs Market")
    market_cum_returns.plot(ax=ax)

    ax.legend(['Conservative Portfolio',
         'S&P'])
    
    return ax

def make_spread_plot(df_port_cum_returns):
    return df_port_cum_returns.plot(kind='box', figsize=(10,5), title="Spread of daily returns of Portfolio")


def get_stats(stocks, market, weights):
    #pull adjclose figures from portfolio performance and market performance
    stock_df, market_df = helpers.get_adjclose(stocks, market)
    
    #get weights for portfolio assets
    stock_weights = np.array(weights['weight'].to_list())
    
    #calculate portfolio return factoring in weights
    stock_df = stock_df.pct_change().dropna()
    portfolio_returns = pd.DataFrame(stock_df.dot(stock_weights)).rename(columns={0: 'adjclose'})

    #calculate market and portfolio cumulative return
    df_market_cum_returns = (1 + market_df).cumprod()
    df_port_cum_returns = (1 + portfolio_returns).cumprod()
    
    
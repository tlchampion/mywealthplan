import pandas as pd
from bokeh.palettes import Category20c, Category20
from bokeh.plotting import figure
from bokeh.transform import cumsum
from math import pi
import modules.helpers as helpers
import numpy as np
from matplotlib.figure import Figure
from matplotlib import cm
from matplotlib.backends.backend_agg import FigureCanvas 

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


# make pie chart showing portfolio asset distribution
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


# process downloaded asset data for use in other functions and calculations
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
    
    return df_port_cum_returns, df_market_cum_returns, portfolio_returns, market_daily_returns
    
# prepare chart comparing performance of selected portfolio with S&P 500

def make_comparison_chart(port_cum_returns, market_cum_returns, class_text):
    text = f"{class_text.capitalize()} Portfolio"
    title = f"Cumulative returns of {class_text.capitalize()} Portfolio vs Market"
    
    
    fig0 = Figure(figsize=(16,8))
    ax = fig0.subplots()
    #ax = port_cum_returns.plot(figsize=(10,5), title="Cumulative returns of Conservative Portfolio vs Market")
    #gmarket_cum_returns.plot(ax=ax)
    chart = ax.plot(port_cum_returns['adjclose'])
    ax.plot(market_cum_returns['^GSPC'])
    ax.set_title(title)

    ax.legend([text,
         'S&P'])
    
    
    
    return fig0

# prepare boxplot showing spread of daily returns for selected portfolio
def make_spread_plot(df_port_cum_returns):
    fig0 = Figure(figsize=(16,8))
    ax = fig0.subplots()
    chart = ax.boxplot(df_port_cum_returns)
    ax.set_title("Spread of Daily Returns for Portfolio")
    ax.axes.xaxis.set_ticklabels([])
    return fig0

#calculate statistics for portfolio

def get_stats(df_port_cum_returns, portfolio_returns):
    portfolio_std = df_port_cum_returns.std()
    
    annual_port_std = df_port_cum_returns.std() * np.sqrt(252)
    
    annual_avg_port_return = portfolio_returns.mean() * 252
    
    port_sharpe_ratio = annual_avg_port_return / annual_port_std
    li = [portfolio_std, annual_port_std, annual_avg_port_return, port_sharpe_ratio]
    df = pd.concat(li, axis=1, keys=['Portfolio Standard Deviation', 'Portfolio Annual Standard Deviation',
                                        'Average Annual Portfolio Return', 'Sharpe Ratio']).T
    df = df.rename(columns={'adjclose':'Statistic'})
    
    return df
 
# prepare 60 day rolling beta plot and retrieve average beta score for selected portfolio
    
# def beta_analysis(market_daily_returns, portfolio_returns):
#     market_daily_returns = market_daily_returns.rename(columns={'^GSPC':'adjclose'})
#     market_variance = market_daily_returns.rolling(window=60).var()
#     portfolio_cov = portfolio_returns.rolling(window=60).cov(market_daily_returns)
#     portfolio_beta = portfolio_cov/market_variance
    
#     portfolio_beta_mean = portfolio_beta.mean()
    
#     fig0 = Figure(figsize=(16,8))
#     ax = fig0.subplots()
#     chart = ax.plot(portfolio_beta)
#     ax.set_title("Portfolio 60-day Rolling Beta")
#     # ax.axes.xaxis.set_ticklabels([])
#     return fig0, portfolio_beta_mean
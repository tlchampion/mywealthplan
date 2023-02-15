# functions to create/define information displayed on the Past Performance tab

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

#get dictionary of answers

answers_dict = helpers.get_answers()



# process downloaded asset data for use in other functions and calculations
# returns portfolio cumulative returns, market cumulative returns, 
#    portfolio daily returns and market daily returns
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
    title = f"{class_text.capitalize()} Portfolio Cumulative Returns vs S&P 500"
    fig0 = Figure(figsize=(16,8))
    ax = fig0.subplots()
    #ax = port_cum_returns.plot(figsize=(10,5), title="Cumulative Returns of Conservative Portfolio vs S&P 500")
    #gmarket_cum_returns.plot(ax=ax)
    chart = ax.plot(port_cum_returns['adjclose'])
    ax.plot(market_cum_returns['^GSPC'])
    ax.set_title(title)
    ax.legend([text,
         'S&P'])
    
    return fig0



# prepare histogram showing spread of daily returns for selected portfolio
def make_spread_plot(df_port_cum_returns):
    fig0 = Figure(figsize=(16,8))
    ax = fig0.subplots()
    chart = ax.hist(df_port_cum_returns)
    ax.set_title("Spread of Daily Returns")
    
    return fig0



# calculate statistics for portfolio
# includes portfolio standard deviation, annual portfolio standard deviation
#    annual average portfolio return, potfolio sharpe ratio
# returns a dataframe

def get_stats(df_port_cum_returns, portfolio_returns):
    portfolio_std = df_port_cum_returns.std()
    
    annual_port_std = df_port_cum_returns.std() * np.sqrt(252)
    
    annual_avg_port_return = portfolio_returns.mean() * 252
    
    port_sharpe_ratio = annual_avg_port_return / annual_port_std
    li = [portfolio_std, annual_port_std, annual_avg_port_return, port_sharpe_ratio]
    df = pd.concat(li, axis=1, keys=['Standard Deviation', 'Annualized Standard Deviation',
                                        'Annual Average Portfolio Return', 'Portfolio Sharpe Ratio']).T
    df = df.rename(columns={'adjclose':'Statistic'})
    
    return df


# define the text that will be displayed at the top of the Past Performance tab

def get_past_performance_intro(port_class_text):
    
    return f""" <h4>
    Below you can find information on the historical performance of the {port_class_text} portfolio, including a comparison to the performance of the S&P 500.<br><br>

    These metrics provide valuable information, but it's important to remember that they are based on historical data and that past performance is not indicative of future results. Additionally, these metrics should be used in conjunction with other factors, such as your investment goals and risk tolerance, to make informed investment decisions.
    
    
    The following two charts are presented:<br><br>

The "Portfolio Cumulative Returns vs S&P 500", which provides a visual comparison of historic performance of your portfolio against that of the S&P 500, an often-used market standard. The returns include both capital appreciation and income.
<br><br>

The "Spread of Daily Returns" chart which provides a visual representation of the frequency and distribution of returns of an investment over a specified time period. It can help you understand how volatile the investment is, or how much its returns can fluctuate over time.
<br><br><br>

In addition to the charts, a table with the following statistical values is included:
<br><br>
Standard Deviation: This is a statistical measure of the volatility of an investment's returns. It measures how far the returns deviate from their average over a specified time period. The higher the standard deviation, the more volatile the investment is.
<br><br>
Annualized Standard Deviation: This is the standard deviation of an investment's returns, adjusted to an annual basis. This allows you to compare the volatility of different investments on an apples-to-apples basis.
<br><br>
Annual Average Portfolio Returns: This is the average return of an investment portfolio over a specified time period, expressed on an annual basis. For example, if a portfolio generated a total return of 10% over the course of 5 years, its annual average return would be 2%.
<br><br>
Portfolio Sharpe Ratio: This is a risk-adjusted performance metric that measures the return of an investment relative to its risk.  The higher the Sharpe ratio, the better the portfolio's return relative to its risk. 
<br><br>
    </h4>"""


# define the text that will be dispalyed at the bottom of the Past Performance tab

def get_past_performance_footer():
    return """These metrics provide valuable information, but it's important to remember that they are based on historical data and that past performance is not indicative of future results. Additionally, these metrics should be used in conjunction with other factors, such as your investment goals and risk tolerance, to make informed investment decisions."""
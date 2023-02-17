# set of functions that define the questions and answers for the risk analysis survery,
# portfolio contents and distributions
# 
# also contains functions that will calculate user's risk score
# and translate that into a risk category
#
# additional functions retrieve historical stock performance information from yahoo
# and also extract closing data from the historical data

import pandas as pd
from pathlib import Path
import pandas as pd
import datetime
from yahoo_fin.stock_info import get_data





# defining the set of questions for the risk analysis survery

questions_dict = {
1: 'What is your current age?',
2: 'I plan to withdraw money from my retirement plan account in:',
3: 'I should have enough savings and stable/guaranteed income (such as, Social Security, pension, retirement plan, annuities) to maintain my planned standard of living in retirement',
4: 'The following statement best describes my willingness to take risk',
5: 'If I invested $100,000 and my portfolio value decreased to $70,000 in just a few months, I would:',
6:  'My assets (excluding home and car) are invested in:'
}


# defining the set of answeres for each question on the risk analysis survery

answers_dict = { 
1: {'Over 70': 1, '60 to 70': 3, '46 to 59': 7, '45 or younger': 10},
2: {'Less than 5 years': 1,
                 '5 to 9 years': 3,
                 '10 to 15 years': 6,
                 'More than 15 years': 8},

3: {'Not confident': 1,
           'Somewhat confident': 2,
           'Confident': 4,
           'Very confident': 6}, 

4: {'I’m more concerned with avoiding losses in my account value than with experiencing growth': 1,
           'I desire growth of my account value, but I’m more concerned with avoiding losses': 3,
           'I’m concerned with avoiding losses, but this is outweighed by my desire to achieve growth': 5,
           'To maximize the chance of experiencing high growth, I’m willing to accept losses': 7}, 

5: {'Be very concerned and sell my investments': 1,
           'Be somewhat concerned and consider allocating to lower risk investments': 2,
           'Be unconcernded about the temporary fluctuations in my returns': 4,
           'Invest more in my current portfolio': 5}, 

6: {"I don't know how my assets are invested": 1,
           "My pension, certificates of deposit, annuities, IRA and savings accounts": 2,
           "A mix of stocks and bonds, including mutual funds": 3,
           "Stocks or stock mutual funds": 4}
}


# define dictionary containg portfolio descriptions

port_descr = {"conservative": "This portfolio has a low-risk, low-reward strategy, with the majority of investments being in bonds (60%) and a smaller portion in stocks (20%). It also includes a small allocation to cryptos (10%) and commodities (10%) to add some diversity. This portfolio is suitable for individuals who are risk-averse and prioritize stability over potential higher returns.",
 "balanced": "This portfolio strikes a balance between risk and reward with equal allocations to stocks (40%) and bonds (40%). It also includes a small allocation to cryptos (10%) and commodities (10%) for diversity. This portfolio is suitable for individuals who are looking for a moderate level of risk and a moderate level of returns.",
 "growth": "This portfolio has a high-risk, high-reward strategy, with the majority of investments being in stocks (60%) and a smaller portion in bonds (20%). It also includes a small allocation to cryptos (10%) and commodities (10%) for diversity. This portfolio is suitable for individuals who have a long-term investment horizon and are willing to take on a higher level of risk in exchange for potential higher returns.",
 "aggressive": "This portfolio has a very high-risk, very high-reward strategy, with the majority of investments being in stocks (70%) and a small portion in bonds (5%). It also includes a substantial allocation to cryptos (15%) and a small allocation to commodities (10%) for diversity. This portfolio is suitable for individuals who are willing to take on a significant amount of risk in pursuit of potentially high returns and have a long-term investment horizon.",
             "alternative": "This portfolio comprises of a equally weighted basket of 4 assets, all in different asset classes. This portfolio is suitable for the investor who has a long term sight for the growth of new frontier technology in crypto, global growth with an exposure to global commodities, traditional technology sector with an emphasis in tech in the S&P 500,  and of course a fundamental backing with exposure to the global real estate market." }

# define the asset contents, weights and categories for the portfolios

conservative = {'XLK': [0.20, 'STOCKS'], 'BNDX': [0.60, "BONDS"], 'GBTC': [0.10, "CRYPTO"], 'AAAU': [0.10, "COMMODOTIES"]}
balanced ={'IVV': [0.40, 'STOCKS'], 'IEI': [0.40, 'BONDS'], 'GBTC': [0.10, 'CRYPTO'], 'AAAU': [0.10, 'COMMODOTIES']}
growth = {'XLK': [0.60, 'STOCKS'], 'BNDX': [0.20, "BONDS"], 'GBTC': [0.10, "CRYPTO"], 'USCI': [0.10, "COMMODOTIES"]}
aggressive = {'XLK': [0.70, 'STOCKS'], 'IEI': [0.05, 'BONDS'], 'GBTC': [0.15, 'CRYPTO'], 'USCI': [0.10, 'COMMODOTIES']}
alternative = {'XLK': [0.50, 'STOCKS'], 'REZ': [0.25, "REAL ESTATE"], 'GBTC': [0.10, "CRYPTO"], 'GSG': [0.15, "COMMODOTIES"]}


# functions to return list of questions and answers

def get_questions():
    return questions_dict

def get_answers():
    return answers_dict

def get_port_assets(port):
    if port == 'conservative':
        return conservative
    elif port == 'balanced':
        return balanced
    elif port == 'growth':
        return growth
    elif port == 'aggressive':
        return aggressive
    else:
        return alternative
    

# functions to load in weights and category for the assets in a portfolio

def get_weights(total_score):

    if (total_score < 13):
        return pd.DataFrame.from_dict(conservative, orient='index', columns=['weight', 'category'])
    elif (total_score < 21):
        return pd.DataFrame.from_dict(balanced, orient='index', columns=['weight', 'category'])
    elif (total_score < 29):
        return pd.DataFrame.from_dict(growth, orient='index', columns=['weight', 'category'])
    elif (total_score < 35):
        return pd.DataFrame.from_dict(aggressive, orient='index', columns=['weight','category'])
    else:
        return pd.DataFrame.from_dict(alternative, orient='index', columns=['weight', 'category'])

# obtain the ticker symbols to be passed to the yahoo_fin api
# ticker symbols are the keys to the portfolio dictionaries

def get_tickers(total_score):
    if (total_score < 13):
        return list(conservative.keys())
    elif (total_score < 21):
        return list(balanced.keys())
    elif (total_score < 29):
        return list(growth.keys())
    elif (total_score < 35):
        return list(aggressive.keys())
    else:
        return list(alternative.keys())
    
# calls the api to retrieve historical stock data and formats into a dataframe for use in other functions

def get_stocks(ticker_list):

    start = datetime.datetime(2017, 12, 31)
    historical_datas = {}
    for ticker in ticker_list:
        historical_datas[ticker] = get_data(ticker, start_date = start, interval="1d")

    df = []
    for ticker in ticker_list:
        dfs = historical_datas[ticker].drop('ticker', axis=1)
        df.append(dfs)
    return  pd.concat(df, axis=1, keys=ticker_list).dropna()

    


# calculate total risk score based upon answers to risk analysis survey
def get_score(a,b,c,d,e,f):
    q1_points = answers_dict[1][a]
    q2_points = answers_dict[2][b]
    q3_points = answers_dict[3][c]
    q4_points = answers_dict[4][d]
    q5_points = answers_dict[5][e]
    q6_points = answers_dict[6][f]
    return q1_points + q2_points + q3_points + q4_points + q5_points + q6_points

    
    
# translate answers to risk analysis survey into a risk category
def get_risk(a,b,c,d,e,f):

    total_score = get_score(a,b,c,d,e,f)
    if (total_score < 13):
        risk = 'conservative'
    elif (total_score < 21):
        risk = 'balanced'
    elif (total_score < 29):
        risk = "growth"
    elif (total_score < 35):
        risk = "aggressive"
    else:
        risk = 'alternative'
        
        
    return risk


# obtain a description of the portfolio selected based upon risk score

def get_descr(a,b,c,d,e,f):
    risk = get_risk(a,b,c,d,e,f)
    return port_descr[risk]

# obtain just the adjclose amount for the portfolio asssets
# uses both the historical data from the selected portfolio
# as well as the historical data from S&P 500

def get_adjclose(stocks, market):
    ticker_list = list(stocks.columns.levels[0])
    ticker_data = stocks
    df = []
    for ticker in ticker_list:
        dfs = ticker_data[ticker]['adjclose']
        df.append(dfs)
    stock_adjclose = pd.concat(df, axis=1, keys=ticker_list)
    
    ticker_list = list(market.columns.levels[0])
    ticker_data = market
    df = []
    for ticker in ticker_list:
        dfs = ticker_data[ticker]['adjclose']
        df.append(dfs)
    market_adjclose = pd.concat(df, axis=1, keys=ticker_list)
    

    return stock_adjclose, market_adjclose

# function to load the 5 datasets for the selected portfolio
# returns a dictionary containg the datasets
# used to create display elements for the Monte Carlo simulation tab ("Future Performance")
def get_data_files(port):
    data_5= pd.read_csv(f"./data/{port}_5.csv")
    data_10= pd.read_csv(f"./data/{port}_10.csv")
    data_15= pd.read_csv(f"./data/{port}_15.csv")
    data_20= pd.read_csv(f"./data/{port}_20.csv")
    data_25= pd.read_csv(f"./data/{port}_25.csv")
    return {5 : data_5, 10: data_10, 15: data_15, 20: data_20, 25: data_25}
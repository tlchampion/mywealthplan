import pandas as pd
from pathlib import Path
import os
import requests
import json
import pandas as pd
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi





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


conservative = {'MSFT': 0.4, 'AAPL': .2, 'GOOG': 0.4}
mod_conservative = {'MSFT': .2, 'IBM': .5, 'AMZN': .3}
moderate = {'IBM': 0.4, 'AAPL': 0.5, 'GOOG': 0.1}
mod_aggressive = {"MSFT": 0.3, "CSCO": 0.3, "IMB": 0.4}
aggressive = {"CSCO": 0.2, "AAPL": 0.5, "GOOG": 0.3}
            
     


# functions to return list of questions and answers

def get_questions():
    return questions_dict

def get_answers():
    return answers_dict

# functions to load in weights and stocks from saved files

def get_weights(total_score):
    # return [0.30,0.20,0.40,0.10]
    # return pd.read_csv(Path("./weights1.csv"))
    if (total_score < 13):
        return pd.DataFrame.from_dict(conservative, orient='index', columns=['weight'])
    elif (total_score < 21):
        return pd.DataFrame.from_dict(mod_conservative, orient='index', columns=['weight'])
    elif (total_score < 29):
        return pd.DataFrame.from_dict(moderate, orient='index', columns=['weight'])
    elif (total_score < 35):
        return pd.DataFrame.from_dict(mod_aggressive, orient='index', columns=['weight'])
    else:
        return pd.DataFrame.from_dict(aggressive, orient='index', columns=['weight'])

    

def get_tickers(total_score):
    if (total_score < 13):
        return ['MSFT', 'AAPL','GOOG']
    elif (total_score < 21):
        return ['MSFT', 'IBM','AMZN']
    elif (total_score < 29):
        return ['IBM', 'AAPL','GOOG']
    elif (total_score < 35):
        return ['MSFT', 'CSCO','IBM']
    else:
        return ['CSCO', 'AAPL','GOOG']

def get_stocks(tickers):
    # return pd.read_csv(Path("./stocks.csv"), index_col='Date', parse_dates=True, infer_datetime_format=True)
    load_dotenv()
    alpaca_api_key = os.getenv("ALPACA_API_KEY")
    alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")

    api = tradeapi.REST(
        alpaca_api_key,
        alpaca_secret_key,
        api_version = "v2"
    )

    # Tickers for all assets, timeframe, timezone amd 10 years history

    tickers = tickers

    timeframe = "1Day"

    start_date = pd.Timestamp("2011-12-31", tz="America/New_York").isoformat()
    end_date = pd.Timestamp("2023-02-07", tz="America/New_York").isoformat()


    # Use the Alpaca get_bars function to get current closing prices the portfolio

    ticker_data = api.get_bars(
        tickers,
        timeframe,
        start=start_date,
        end=end_date
    ).df

    return ticker_data.pivot(columns='symbol', values='close')



    


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

    total_score = score(a,b,c,d,e,f)
    if (total_score < 13):
        risk = 'Conservative'
    elif (total_score < 21):
        risk = 'Moderately Conservative'
    elif (total_score < 29):
        risk = "Moderate"
    elif (total_score < 35):
        risk = "Moderately Aggressive"
    else:
        risk = "Aggressive"
        
    return f"You scored {total_score} out of 40, indicating that you are a {risk} investor"
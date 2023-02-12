import os
import requests
import json
import pandas as pd
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
from MCForecastTools import MCSimulation
import warnings
warnings.filterwarnings(action='ignore')




from matplotlib.figure import Figure
from matplotlib import cm
from matplotlib.backends.backend_agg import FigureCanvas  # not needed for mpl >= 3.1

def prep_MC_data():
    # Load the environment variables from the .env file
    load_dotenv()

    # Set the variables for the Alpaca API and secret keys
    alpaca_api_key = os.getenv("ALPACA_API_KEY")
    alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")

    api = tradeapi.REST(
        alpaca_api_key,
        alpaca_secret_key,
        api_version = "v2"
    )

    # Tickers for all assets, timeframe, timezone amd 10 years history

    tickers = ["MSFT", "BOND", "BTC", "OIL"]

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

    # Reorganize the DataFrame
    # Separate ticker data
    STOCK = ticker_data[ticker_data['symbol']=='MSFT'].drop('symbol', axis=1)
    BOND = ticker_data[ticker_data['symbol']=='BOND'].drop('symbol', axis=1)
    CRYPTO = ticker_data[ticker_data['symbol']=='BTC'].drop('symbol', axis=1)
    COMMS = ticker_data[ticker_data['symbol']=='OIL'].drop('symbol', axis=1)

    # Concatenate the ticker DataFrames
    ticker_data = pd.concat([STOCK, BOND, CRYPTO, COMMS],axis=1, keys=tickers).dropna()


    simulation = MCSimulation(
        portfolio_data = ticker_data,
        weights=[0.20,0.60,0.10,0.10],
        num_simulation = 500,
        num_trading_days =252*10
    )


    simulation.calc_cumulative_return()
    
    simulation_plot = simulation.plot_simulation()
    distribution_plot = simulation.plot_distribution()
    
    return simulation_plot, distribution_plot
    
def get_simulation_plot():
    return simulation.plot_simulation()


def get_distribution_plot():
    return simulation.plot_distribution()


def get_statistics():
    pass

def get_text():
    text = """
    <h4>A Monte Carlo Simulation is available to be run, providing some probabilistic insights into the potential future performance of your selected portfolio.
    <br><br>
    The simulation is not run automatically but can be provided by clicking on the button below. Please be aware that the simulation involved a large number of calculations, which may result in a waiting period of one to two mintues. 
    </h4>
    """
    return text
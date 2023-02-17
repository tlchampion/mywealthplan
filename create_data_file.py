import modules.helpers as helpers
import pandas as pd
import numpy as np
import datetime as dt
import warnings
warnings.filterwarnings(action='ignore')
import sys
import argparse



def create_mc_data_file(portfolio_data, weights, num_simulations, num_years):
    
    nSim = num_simulations
    nTrading = num_years * 252

# Check to make sure that all attributes are set
    if not isinstance(portfolio_data, pd.DataFrame):
        raise TypeError("portfolio_data must be a Pandas DataFrame")

    # Set weights if empty, otherwise make sure sum of weights equals one.
    if weights == "":
        num_stocks = len(portfolio_data.columns.get_level_values(0).unique())
        weights = [1.0/num_stocks for s in range(0,num_stocks)]
    else:
        if round(sum(weights),2) < .99:
            raise AttributeError("Sum of portfolio weights must equal one.")

    # Calculate daily return if not within dataframe
    if not "daily_return" in portfolio_data.columns.get_level_values(1).unique():
        close_df = portfolio_data.xs('close',level=1,axis=1).pct_change()
        tickers = portfolio_data.columns.get_level_values(0).unique()
        column_names = [(x,"daily_return") for x in tickers]
        close_df.columns = pd.MultiIndex.from_tuples(column_names)
        portfolio_data = portfolio_data.merge(close_df,left_index=True,right_index=True).reindex(columns=tickers,level=0)   

    
  # Get closing prices of each stock
    last_prices = portfolio_data.xs('close',level=1,axis=1)[-1:].values.tolist()[0]

    # Calculate the mean and standard deviation of daily returns for each stock
    daily_returns = portfolio_data.xs('daily_return',level=1,axis=1)
    mean_returns = daily_returns.mean().tolist()
    std_returns = daily_returns.std().tolist()

    # Initialize empty Dataframe to hold simulated prices
    portfolio_cumulative_returns = pd.DataFrame()
    
    

        # Run the simulation of projecting stock prices 'nSim' number of times
    for n in range(nSim):

        # if n % 10 == 0:
        #     print(f"Running Monte Carlo simulation number {n}.")

        # Create a list of lists to contain the simulated values for each stock
        simvals = [[p] for p in last_prices]

        # For each stock in our data:
        for s in range(len(last_prices)):

            # Simulate the returns for each trading day
            for i in range(nTrading):

                # Calculate the simulated price using the last price within the list
                simvals[s].append(simvals[s][-1] * (1 + np.random.normal(mean_returns[s], std_returns[s])))

        # Calculate the daily returns of simulated prices
        sim_df = pd.DataFrame(simvals).T.pct_change()

        # Use the `dot` function with the weights to multiply weights with each column's simulated daily returns
        sim_df = sim_df.dot(weights)

        # Calculate the normalized, cumulative return series
        portfolio_cumulative_returns[n] = (1 + sim_df.fillna(0)).cumprod()


    return portfolio_cumulative_returns
    
    




if __name__ == "__main__":
    

    num_simulations = 2500
    
        

    
    portfolios = ['conservative', 'balanced', 'growth', 'aggressive', 'alternative']
    
    for port in portfolios:
        years = [5,10,15,20,25]
        for year in years:
            
            assets = helpers.get_port_assets(port)
            ticker_data = helpers.get_stocks(assets)
            weights_df = pd.DataFrame.from_dict(assets, orient='index', columns=['weight', 'category'])
            weights = weights_df['weight'].to_list()
            data = create_mc_data_file(ticker_data, weights, num_simulations, year)

            data.to_csv(f"./data/{port}_{year}.csv", index=False)
            print(f"{port} for {year} years is done")
    




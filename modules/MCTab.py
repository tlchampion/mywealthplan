# this file contains functions used to assemble the Future Performance tab


import pandas as pd
from modules.MCForecastTools import MCSimulation
import warnings
warnings.filterwarnings(action='ignore')
from matplotlib.figure import Figure
from matplotlib import cm
from matplotlib.backends.backend_agg import FigureCanvas  # not needed for mpl >= 3.1


# # use the historical stock data to call the functions in the MCForecastTools script
# # return the plots, summary statistics and CI text for display on dashboard
# def prep_MC_data(ticker_data, weights):

#     weight_list = weights['weight'].to_list()


#     simulation = MCSimulation(
#         portfolio_data = ticker_data,
#         weights=weight_list,
#         num_simulation = 200,
#         num_trading_days =252*10
#     )


#     simulation.calc_cumulative_return()
#     invested_amount = 100000
#     simulation_plot = simulation.plot_simulation()
#     distribution_plot = simulation.plot_distribution()
#     summary = simulation.summarize_cumulative_return()
#     ci_lower_ten_cumulative_return = round(summary[8]*invested_amount,2)
#     ci_upper_ten_cumulative_return = round(summary[9]*invested_amount,2)
#     text = f"""
#             There is a 95% chance that the final portfolio value after 10 years will be within the range of ${ci_lower_ten_cumulative_return:,.2f} and ${ci_upper_ten_cumulative_return:,.2f} based upon an initial investment of ${invested_amount:,.2f}
#             """
    
#     return simulation_plot, distribution_plot, summary, text

def prep_MC_data(df):
    
    invested_amount = 100000
    nTrading = (df.shape[0] - 1) // 252
    nSim = df.shape[1]
    # simulation_plot = make_sim_plot(df)
    dist_plot = make_dist_plot(df)
    summary = make_summary(df)
    ci_lower_ten_cumulative_return = round(summary[8]*invested_amount,2)
    ci_upper_ten_cumulative_return = round(summary[9]*invested_amount,2)
    text = f"""
            There is a 95% chance that the final portfolio value after {nTrading} years will be within the range of ${ci_lower_ten_cumulative_return:,.2f} and ${ci_upper_ten_cumulative_return:,.2f} based upon an initial investment of ${invested_amount:,.2f}
            """
    
    return dist_plot, summary, text



def make_sim_plot(df):
        # Use Pandas plot function to plot the return data
        nTrading = (df.shape[0] - 1)
        nSim = df.shape[1]
        plot_title = f"{nSim} Simulations of Cumulative Portfolio Return Trajectories Over the Next {nTrading} Trading Days ({nTrading/252} years)."
        return df.hvplot(legend=False,title=plot_title,height=250, width=500)




def make_dist_plot(df):
        # Use the `plot` function to create a probability distribution histogram of simulated ending prices
        # with markings for a 95% confidence interval
        nTrading = (df.shape[0] - 1)//252
        nSim = df.shape[1]
        plot_title = f"Distribution of Final Cumuluative Returns Across All {nSim} Simulations for {nTrading} years"
        x_label = "Final Cumulative Return in \$USD per \$1 Invested"
        y_label = "Frequency"
        ci = df.iloc[-1, :].quantile(q=[0.025, 0.975])
        fig0 = Figure(figsize=(8, 6))
        ax0 = fig0.subplots()
        # FigureCanvas(fig0)  # not needed for mpl >= 3.1
        chart = ax0.hist(df.iloc[-1, :], bins=200)
        ax0.axvline(ci.iloc[0], color='r')
        ax0.axvline(ci.iloc[1], color='r')
        ax0.set_title(plot_title)
        ax0.set_xlabel(x_label)
        ax0.set_ylabel(y_label)
                   

        return fig0



def make_summary(df):
        ci = df.iloc[-1, :].quantile(q=[0.025, 0.975])
        metrics = df.iloc[-1].describe()
       
        ci.index = ["95% CI Lower","95% CI Upper"]
        return metrics.append(ci)
    
    

    


    
# def get_simulation_plot():
#     return simulation.plot_simulation()


# def get_distribution_plot():
#     return simulation.plot_distribution()


# def get_statistics():
#     pass


# define text to display at top of Future Performance tab
def get_text():
    text = """
    <h4>The results of 5 Monte Carlo Simulations are available for review. A Monte Carlo simulation is a computer-based modeling technique used to estimate the potential range of returns for an investment over a specified time period. It uses statistical algorithms to generate multiple simulations of potential returns and can help to assess the potential risk and reward of an investment. In this case the simulations are run over 5, 10, 15, 20 and 25 years with 2500 iterations per simulation.
    <br><br>
    The summary charts are not compiled automatically but can be provided by clicking on the button below. Please be aware that it may take one to two minutes to compite the charts due to the volume of data involved. 
    <br><br>
    Once completed, you will be presented with the following:
    <br>
    <ul>


<li>
A series of distribution charts providing a visual representation of the frequency of the portoflio's final cumulative return for each of the 2500 simulations. Distribution charts are compiled for a 5, 10, 15, 20 and 25 year time period. These charts can provide and indication for the likelihood for a certain outcome
</li>

<li>
A statement for each time period indicating the range of values in which 95% of simulations run are likely to fall. This again provides an indication of the portfolio's potential future performance
</li>

</ul>


    </h4>
    """
    return text


# define text to display at bottom of Future Performance tab
def get_mc_footer():
    return """
    The projections or other information generated by Monte Carlo analysis tools regarding the likelihood of various investment outcomes are hypothetical in nature, do not reflect actual investment results, and are not guarantees of future results. Results may vary with each use and over time. Because of the many variables involved, an investor should not rely on forecasts without realizing their limitations."""
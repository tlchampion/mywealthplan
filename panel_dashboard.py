#!/usr/bin/env python
# coding: utf-8

# In[1]:


import panel as pn
# pn.extension(template='bootstrap')
pn.extension('tabulator')
# pn.extension('ipywidgets')
import pandas as pd
import numpy as np
import hvplot.pandas
# from panel.template import BootstrapTemplate
from panel.template import FastListTemplate
from pathlib import Path
from yahoo_fin.stock_info import get_data
import datetime

# import matplotlib.pyplot as plt
# import seaborn as sn
# %matplotlib ipympl





# from bokeh.palettes import Category20c, Category20
# from bokeh.plotting import figure
# from bokeh.transform import cumsum
# from math import pi


from matplotlib.figure import Figure
from matplotlib import cm
from matplotlib.backends.backend_agg import FigureCanvas 

# from test_modules.intro import make_pie, image, get_html, make_weight_chart
import modules.helpers as helpers
import modules.HistoricalData as hst
from test_modules.tab4 import make_chart
import modules.MCTab as MCTab
import modules.intro as intro


# In[2]:


# initialize the dashboard framework

template = FastListTemplate(title="Portfolio Selection Tool", header_background = 'blue')


# In[3]:


# defining the risk analysis survey questions

# questions_dict = {
# 1: 'What is your current age?',
# 2: 'I plan to withdraw money from my retirement plan account in:',
# 3: 'I should have enough savings and stable/guaranteed income (such as, Social Security, pension, retirement plan, annuities) to maintain my planned standard of living in retirement',
# 4: 'The following statement best describes my willingness to take risk',
# 5: 'If I invested $100,000 and my portfolio value decreased to $70,000 in just a few months, I would:',
# 6:  'My assets (excluding home and car) are invested in:'
# }

questions_dict = helpers.get_questions()


# In[4]:


# defining the valid answers to the questions and assigninig points to each answer

# answers_dict = { 
# 1: {'Over 70': 1, '60 to 70': 3, '46 to 59': 7, '45 or younger': 10},
# 2: {'Less than 5 years': 1,
#                  '5 to 9 years': 3,
#                  '10 to 15 years': 6,
#                  'More than 15 years': 8},

# 3: {'Not confident': 1,
#            'Somewhat confident': 2,
#            'Confident': 4,
#            'Very confident': 6}, 

# 4: {'I’m more concerned with avoiding losses in my account value than with experiencing growth': 1,
#            'I desire growth of my account value, but I’m more concerned with avoiding losses': 3,
#            'I’m concerned with avoiding losses, but this is outweighed by my desire to achieve growth': 5,
#            'To maximize the chance of experiencing high growth, I’m willing to accept losses': 7}, 

# 5: {'Be very concerned and sell my investments': 1,
#            'Be somewhat concerned and consider allocating to lower risk investments': 2,
#            'Be unconcernded about the temporary fluctuations in my returns': 4,
#            'Invest more in my current portfolio': 5}, 

# 6: {"I don't know how my assets are invested": 1,
#            "My pension, certificates of deposit, annuities, IRA and savings accounts": 2,
#            "A mix of stocks and bonds, including mutual funds": 3,
#            "Stocks or stock mutual funds": 4}
# }

answers_dict = helpers.get_answers()


# In[5]:


# define functions to aggregate risk analysis response scores for presentation or usage in other functions

# calculate total risk score based upon answers to risk analysis survey
def score(a,b,c,d,e,f):
    q1_points = answers_dict[1][a]
    q2_points = answers_dict[2][b]
    q3_points = answers_dict[3][c]
    q4_points = answers_dict[4][d]
    q5_points = answers_dict[5][e]
    q6_points = answers_dict[6][f]
    return q1_points + q2_points + q3_points + q4_points + q5_points + q6_points

    
    
# translate answers to risk analysis survey into a risk category
def risk(a,b,c,d,e,f):

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

# test function to select an image for display based upon total score value
# this can be deleted once the functionality in 'tab 1' is changed
# def image(a,b,c,d,e,f):

#     total_score = score(a,b,c,d,e,f)
#     if (total_score < 13):
#         return "image1.jpg"
#     elif (total_score < 29):
#         return "image2.jpg"
#     else:
#         return "image3.jpg"


# In[6]:


# define the dropdown/selection boxes for the risk analysis survey answers
# will be included in sidebar

q1 = pn.widgets.Select(value=list(answers_dict[1].keys())[0],
                        options = list(answers_dict[1].keys()), name='')

q2 = pn.widgets.Select(value=list(answers_dict[2].keys())[0],
                        options = list(answers_dict[2].keys()), name='')

q3 = pn.widgets.Select(value=list(answers_dict[3].keys())[0],
                        options = list(answers_dict[3].keys()), name='')
q4 = pn.widgets.Select(value=list(answers_dict[4].keys())[0],
                       options = list(answers_dict[4].keys()), name='')

q5 = pn.widgets.Select(value=list(answers_dict[5].keys())[0],
                        options = list(answers_dict[5].keys()), name='')
q6 = pn.widgets.Select(value=list(answers_dict[6].keys())[0],
                        options = list(answers_dict[6].keys()), name='')

# define the button to submit risk analysis survey responses
# contents of main panel will only be updated after responses are submitted
button = pn.widgets.Button(name="Submit")


# In[7]:


# define the header box for the sidebar
text = "Please begin by answering the following questions so we can determine your risk tolerance level"
header_box = pn.WidgetBox(text,width=300, height=75, align='center')

# define a spacer element to seperate elements in sidebar
spacer = pn.layout.Spacer(margin=10)


# In[8]:


# assembling the sidebar
template.sidebar.append(pn.Row(pn.Column(header_box,
                                          spacer,
                                          spacer,
                                          questions_dict[1],q1,
                                          spacer,
                                          questions_dict[2], q2,
                                          spacer,
                                          questions_dict[3],q3,
                                          spacer,
                                          questions_dict[4], q4,
                                          spacer,
                                          questions_dict[5], q5,
                                          spacer,
                                          questions_dict[6],q6,
                                          spacer,
                                          button
                                         )))


# In[9]:


# get values for each of the answers
def get_values():
    return q1.value, q2.value, q3.value, q4.value, q5.value, q6.value


# def get_stocks():
#     return pd.read_csv(Path("./stocks.csv"), index_col='Date', parse_dates=True, infer_datetime_format=True)

# def get_weights():
#     # return [0.30,0.20,0.40,0.10]
#     return pd.read_csv(Path("./weights1.csv"))




# def make_chart2(investment, weights, stocks):
#     weights = weights['weight']
#     allocation = [w * investment for w in weights]
#     amount = allocation/stocks.iloc[0]
#     stock_value = stocks * amount
#     stock_value = stock_value.sum(axis=1).reset_index().rename(columns={0:"Total Value ($)"}).set_index('Date')
#     plot_title = "title"
#     fig0 = Figure(figsize=(16,8))
#     ax0 = fig0.subplots()
#     # FigureCanvas(fig0)  # not needed for mpl >= 3.1
#     chart = ax0.plot(stock_value['Total Value ($)'])

#     ax0.set_title(plot_title)
#    # plot = stock_value.hvplot.line(x="Date", height=500,width=1000)
#     return fig0



# In[10]:


# def show_distr():

#     distribution = get_weights()
#     plt = distribution.set_index('stock').plot.pie(y='weight',figsize=(5,5), ylabel="",
#                                              title = "Conservative Portfolio Composition", legend=False, autopct='%.2f%%')
#     return plt
  



# In[11]:


a,b,c,d,e,f = get_values()
tickers = helpers.get_tickers(helpers.get_score(a,b,c,d,e,f))
stocks = helpers.get_stocks(tickers)
weights = helpers.get_weights(helpers.get_score(a,b,c,d,e,f))
market = helpers.get_stocks(['^GSPC'])


# In[ ]:


stock, market = helpers.get_adjclose(stocks,market)



# In[ ]:


# defining the contents of the main (right-hand) pane in the Panel dashboard
# the contents are dependent upon the answers given and will be updated once the 'submit' button in the sidebar pane is clicked

@pn.depends(button.param.clicks)
def main_display(_):
    
    # setting variables for use in defining dashboard components
    a,b,c,d,e,f = get_values()
    tickers = helpers.get_tickers(helpers.get_score(a,b,c,d,e,f))
    stocks = helpers.get_stocks(tickers)
    weights = helpers.get_weights(helpers.get_score(a,b,c,d,e,f))
    market = helpers.get_stocks(['^GSPC'])
    # determing the text to display describing portfolio based upon risk analsys survey  
    port_desc_text = helpers.get_descr(a,b,c,d,e,f)
    port_class_text = helpers.get_risk(a,b,c,d,e,f)
    score = helpers.get_score(a,b,c,d,e,f)
    
    # prepare cumulative return information for use in displays
    df_port_cum_returns, df_market_cum_returns, portfolio_returns, market_daily_returns = hst.get_cum_returns(stocks, market, weights)

    
##########
    # Setting up Introduction tab
 

    
    intro_text = intro.get_intro()
   # disclaimer_text = tab0.get_disclaimer()
    
    intro_pane = pn.pane.HTML(intro_text)
    #disclaimer_pane = pn.pane.HTML(disclaimer_text)
    
#########
    # defining contents for 'Portfolio Profile' pane
    
    #port_stats = hst.get_stats(df_port_cum_returns, portfolio_returns)
    
    # creating pie chart and table to visualize portfolio distribution
    p = hst.make_pie(weights)
    weight_chart = hst.make_weight_chart(weights)
    
    # define pane to provide risk score and portfolio description
    port_desc_pane = pn.pane.HTML(f"""<h3> Based upon your Risk Tolerance Score of {score} you are classified as a {port_class_text.capitalize()} Investor. 
    <br><br>{port_desc_text} </h3>""",
                                  width=800)
    
    # define panes for inclusion in tab
    bokeh_pane = pn.pane.Bokeh(p, theme="dark_minimal")
    df_weights_pane = pn.pane.DataFrame(weight_chart, width=200)
    

##########
    # defining contents for 'Past Performance' tab  
    
    
 
    
    # prepare cumulative return information for use in 
    #df_port_cum_returns, df_market_cum_returns, portfolio_returns, market_daily_returns = hst.get_cum_returns(stocks, market, weights)
    
    #create portfolio vs market chart, portfolio box plot and basic statistics dataframe along with the page intro text
    compare_chart = hst.make_comparison_chart(df_port_cum_returns, df_market_cum_returns, port_class_text)
    spread_plot = hst.make_spread_plot(df_port_cum_returns)
    port_stats = hst.get_stats(df_port_cum_returns, portfolio_returns)
    header_text = hst.get_past_performance_intro(port_class_text)
    footer_text = hst.get_past_performance_footer()
    

    
    # # creating pie chart and table to visualize portfolio distribution
    # p = hst.make_pie(weights)
    # weight_chart = hst.make_weight_chart(weights)
    
    
    
    
    # defiing panes for display
    
    # beta_plot_pane = pn.pane.Matplotlib(beta_plot)
    compare_pane = pn.pane.Matplotlib(compare_chart)
    spread_pane = pn.pane.Matplotlib(spread_plot)
    stats_pane = pn.pane.DataFrame(port_stats, width=200)
    header_pane = pn.pane.HTML(header_text, width = 900)
    footer_pane = pn.pane.HTML(footer_text, width = 900)
    # port_desc_pane = pn.pane.HTML(f"""<h3> Based upon your Risk Tolerance Score of {score} you are classified as a {port_class_text.capitalize()} Investor. 
    # <br><br>{port_desc_text} </h3>""",
    #                               width=800)


#     bokeh_pane = pn.pane.Bokeh(p, theme="dark_minimal")
    
#     df_pane = pn.pane.DataFrame(weight_chart, width=200)
    
    
    # text_pane = pn.pane.HTML(get_html())
    
    # tab1_grid = pn.GridSpec()
    # tab1_grid[0,0] = bokeh_pane
    # tab1_grid[0,1] = df_pane
    
    


    
    
##########
    # defining contents of 'Monte Carlo Simulation' tab
    
    # call function to run MC simulation and return plots and statistics
    
    # tab5_grid = pn.GridSpec(width=800,height=600)
    
    
    mc_text = MCTab.get_text()
    mc_text_pane = pn.pane.HTML(mc_text, width = 800)
    mc_button = pn.widgets.Button(name="Show Monte Carlo Simulation Results")

    # tab5_column = pn.Column(mc_text_pane, mc_button, spacer, spacer)
    
    mc_column = pn.Column(spacer)
    mc_row1 = pn.Row(spacer)
    mc_row2 = pn.Row(spacer)
    mc_footer = pn.pane.HTML(MCTab.get_mc_footer(), width = 800)
    
       
   
    # tab5_grid[0,:] = mc_text_pane
    # tab5_grid[1,:] = mc_column
    
    async def change_pane(event):

        if (mc_button.clicks == 1):

            simulation_plot, distribution_plot, summary, text = MCTab.prep_MC_data(stocks, weights)

            distribution_pane = pn.pane.Matplotlib(distribution_plot, dpi=144)
            summary_pane = pn.pane.DataFrame(summary.to_frame(name='statistics'))
            ci_pane = pn.pane.HTML(f"""<h4> {text} </h4>""", width = 800)
            
                                             
            # tab5_column.append(simulation_plot)
            # tab5_column.append(distribution_pane)
            mc_column.append(simulation_plot)
            mc_column.append(distribution_pane)
            # mc_row2.append(summary_pane)
            mc_row2.append(pn.layout.Spacer(margin=10))
            mc_row2.append(pn.layout.Spacer(margin=10))
            mc_row2.append(ci_pane)
            

             

    mc_button.on_click(change_pane)

    
#     simulation_plot, distribution_plot = tab5.prep_MC_data()
    
#     distribution_pane = pn.pane.Matplotlib(distribution_plot, dpi=144)
    

    # combine main pane components into a tabbed structure and return to main script for usage
#     return pn.Tabs(("Introduction", pn.Column(intro_pane, sizing_mode='stretch_width')),
#                    ("Tab 1", pn.Column("This tab can hold a variety of plots or details about the portfolio selected",photo,spacer,text_pane, pn.Row(df_pane,spacer, bokeh_pane))),
#                    ("Tab 2", pn.Row(pn.Column("This tab can hold even more plots or details!!", pn.pane.markup.Markdown(text)),html_pane)),
#                    ("Tab 3", pn.Row(pn.Column(jpg_pane,second_button,textb ),"Who Knows?")),
#                    ("Tab 4", pn.Column(pn.Row(investment_amount),chart,sizing_mode="stretch_width")),
#                    ("Tab 5", pn.Row(tab5_grid, width=800))
#                     )
                  
 
    return pn.Tabs(("Introduction", pn.Column(intro_pane, sizing_mode='stretch_width')),
                   ("Portfolio Profile", pn.Column(pn.Row(port_desc_pane),
                                                   pn.Row(bokeh_pane, df_weights_pane))),
                   ("Past Performance", pn.Column(pn.Row(header_pane),
                                                  pn.Row(compare_pane),
                                                  pn.Row(spread_pane),
                                                  pn.Row(stats_pane, width=50),
                                                  pn.Row(spacer),
                                                 pn.Row(footer_pane))),
                   ("Monte Carlo Simulation", pn.Column(pn.Row(mc_text_pane),
                                                        pn.Row(mc_button),
                                                        pn.Row(mc_column), 
                                                        pn.Row(mc_row2),
                                                       pn.Row(mc_footer)))
                   
                
                  )
#                    ("Tab 1", pn.Column("This tab can hold a variety of plots or details about the portfolio selected",photo,spacer,text_pane, pn.Row(df_pane,spacer, bokeh_pane))),
#                    ("Tab 2", pn.Row(pn.Column("This tab can hold even more plots or details!!", pn.pane.markup.Markdown(text)),html_pane)),
#                    ("Tab 3", pn.Row(pn.Column(jpg_pane,second_button,textb ),"Who Knows?")),
#                    ("Tab 4", pn.Column(pn.Row(investment_amount),chart,sizing_mode="stretch_width")),
#                    ("Tab 5", pn.Row(tab5_grid, width=800))
#                     )


# In[ ]:


#adding main display area to dashboard

template.main.append(main_display)


# In[ ]:


# displaying dashboard
# if dashboard is being served through a servise this needs to be updated to .servicable() rather than .show()

template.show()


# In[ ]:





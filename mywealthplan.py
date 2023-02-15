
# import modules
import panel as pn
pn.extension('tabulator')
import pandas as pd
import numpy as np
from panel.template import FastListTemplate
from pathlib import Path
from yahoo_fin.stock_info import get_data
import datetime
from matplotlib.figure import Figure
from matplotlib import cm


# import modules that help build tabs
import modules.helpers as helpers
import modules.HistoricalData as hst
import modules.MCTab as MCTab
import modules.intro as intro
import modules.profile as prf




template = FastListTemplate(title="MyWealthPath", header_background = 'blue')





# define list of questions

questions_dict = helpers.get_questions()





# defining the valid answers to the questions and assigninig points to each answer

answers_dict = helpers.get_answers()





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





# define the header box for the sidebar
text = "Please begin by answering the following questions so we can determine your risk tolerance level"
header_box = pn.WidgetBox(text,width=300, height=75, align='center')

# define a spacer element to seperate elements in sidebar
spacer = pn.layout.Spacer(margin=10)





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





# get values for each of the answers
# necessary to use for calculating risk score
def get_values():
    return q1.value, q2.value, q3.value, q4.value, q5.value, q6.value





# defining the contents of the main (right-hand) pane in the Panel dashboard
# the contents are dependent upon the answers given and will be updated once the 'submit' button in the sidebar pane is clicked

# setup listener for survey results submission button
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
    
    # getting total risk tolerance score
    score = helpers.get_score(a,b,c,d,e,f)
    
    # prepare cumulative return information for use in displays
    df_port_cum_returns, df_market_cum_returns, portfolio_returns, market_daily_returns = hst.get_cum_returns(stocks, market, weights)

    
##########


# Setting up Introduction tab
# grabbing contents from modules/intro.py file and assembling into panel panes
    intro_text = intro.get_intro()
    portfolios_intro_text = intro.get_portfolios_intro()
    disclaimer_text = intro.get_disclaimer()
    intro_pane = pn.pane.Markdown(intro_text)
    tabs_pane = pn.pane.PNG("https://drive.google.com/uc?id=1RuqJmAkdxuNSkFoDk4OB6Qi_JIsGgLlD", width=400)
    portfolios_intro_pane = pn.pane.Markdown(portfolios_intro_text)
    portfolios_pane = pn.pane.PNG("https://drive.google.com/uc?id=1lr_nc7ayQNyIvSJll5E61f4cZZPokKlK", width=1000)
    disclaimer_pane = pn.pane.Markdown(disclaimer_text)



    
#########
    # defining contents for 'Portfolio Profile' pane
    

    
    # creating pie chart and table to visualize portfolio distribution
    p = prf.make_pie(weights)
    weight_chart = prf.make_weight_chart(weights)
    
    # define pane to provide risk score and portfolio description
    port_desc_pane = pn.pane.HTML(f"""<h3> Based upon your Risk Tolerance Score of {score} you are classified as a {port_class_text.capitalize()} Investor. 
    <br><br>{port_desc_text} </h3>""",
                                  width=800)
    
    # define panes for inclusion in tab
    bokeh_pane = pn.pane.Bokeh(p, theme="dark_minimal")
    df_weights_pane = pn.pane.DataFrame(weight_chart, width=200)
    

##########
    # defining contents for 'Past Performance' tab  
    
    
    #create portfolio vs market chart, portfolio box plot and basic statistics dataframe along with the page intro text
    compare_chart = hst.make_comparison_chart(df_port_cum_returns, df_market_cum_returns, port_class_text)
    spread_plot = hst.make_spread_plot(df_port_cum_returns)
    port_stats = hst.get_stats(df_port_cum_returns, portfolio_returns)
    header_text = hst.get_past_performance_intro(port_class_text)
    footer_text = hst.get_past_performance_footer()

    
    # defiing panes for display
    
    compare_pane = pn.pane.Matplotlib(compare_chart)
    spread_pane = pn.pane.Matplotlib(spread_plot)
    stats_pane = pn.pane.DataFrame(port_stats, width=200)
    header_pane = pn.pane.HTML(header_text, width = 900)
    footer_pane = pn.pane.HTML(footer_text, width = 900)

    


    
    
##########
    # defining contents of 'Monte Carlo Simulation' tab
    
    # grab text to display in pane, define panel pane to hold text and setup button to launch MC simulation
    mc_text = MCTab.get_text()
    mc_text_pane = pn.pane.HTML(mc_text, width = 800)
    mc_button = pn.widgets.Button(name="Show Monte Carlo Simulation Results")

    # setup partial layout framework for tab. results of MC simulation will be appened to these panel objects for display
    
    mc_column = pn.Column(spacer)
    mc_row1 = pn.Row(spacer)
    mc_row2 = pn.Row(spacer)
    mc_footer = pn.pane.HTML(MCTab.get_mc_footer(), width = 800)
    
       
    # this function is triggered once the button to perform a MC simulation is clicked. 
    # Initiates simulation and recives plots and statistics for display
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
            

    # listener for button click    

    mc_button.on_click(change_pane)

    #######
    
    # returning panel components defined above to main script for appending to dashboard
    # components are organized into serperate tabs
    # each tab is organized using panels Column and Row functionality
                 
 
    return pn.Tabs(("Introduction", pn.Column(intro_pane, portfolios_intro_pane, portfolios_pane, disclaimer_pane)),
                   ("Portfolio Profile", pn.Column(pn.Row(port_desc_pane),
                                                   pn.Row(bokeh_pane, df_weights_pane))),
                   ("Past Performance", pn.Column(pn.Row(header_pane),
                                                  pn.Row(compare_pane),
                                                  pn.Row(spread_pane),
                                                  pn.Row(stats_pane, width=50),
                                                  pn.Row(spacer),
                                                 pn.Row(footer_pane))),
                   ("Future Performance", pn.Column(pn.Row(mc_text_pane),
                                                        pn.Row(mc_button),
                                                        pn.Row(mc_column), 
                                                        pn.Row(mc_row2),
                                                       pn.Row(mc_footer)))
                   
                
                  )





#adding main display area to dashboard

template.main.append(main_display)





# displaying dashboard
# if dashboard is being served through a servise this needs to be updated to .servicable() rather than .show()

template.servable()








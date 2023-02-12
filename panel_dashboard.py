#!/usr/bin/env python
# coding: utf-8

# In[1]:


import panel as pn
pn.extension(template='bootstrap')
# pn.extension('ipywidgets')
import pandas as pd
import hvplot.pandas
from panel.template import BootstrapTemplate
from pathlib import Path

# import matplotlib.pyplot as plt
# import seaborn as sn
get_ipython().run_line_magic('matplotlib', 'ipympl')


get_ipython().run_line_magic('matplotlib', 'inline')


# from bokeh.palettes import Category20c, Category20
# from bokeh.plotting import figure
# from bokeh.transform import cumsum
# from math import pi


from matplotlib.figure import Figure
from matplotlib import cm
from matplotlib.backends.backend_agg import FigureCanvas 

from tab1 import make_pie, image, get_html, make_weight_chart
import helpers
from tab4 import make_chart
import tab5
import tab0


# In[2]:


# initialize the dashboard framework

bootstrap = BootstrapTemplate(title="Portfolio Analysis", header_background = 'blue')


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
bootstrap.sidebar.append(pn.Row(pn.Column(header_box,
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




def make_chart2(investment, weights, stocks):
    weights = weights['weight']
    allocation = [w * investment for w in weights]
    amount = allocation/stocks.iloc[0]
    stock_value = stocks * amount
    stock_value = stock_value.sum(axis=1).reset_index().rename(columns={0:"Total Value ($)"}).set_index('Date')
    plot_title = "title"
    fig0 = Figure(figsize=(16,8))
    ax0 = fig0.subplots()
    # FigureCanvas(fig0)  # not needed for mpl >= 3.1
    chart = ax0.plot(stock_value['Total Value ($)'])

    ax0.set_title(plot_title)
   # plot = stock_value.hvplot.line(x="Date", height=500,width=1000)
    return fig0



# In[10]:


# def show_distr():

#     distribution = get_weights()
#     plt = distribution.set_index('stock').plot.pie(y='weight',figsize=(5,5), ylabel="",
#                                              title = "Conservative Portfolio Composition", legend=False, autopct='%.2f%%')
#     return plt
  



# In[11]:


helpers.get_weights()


# In[12]:


make_weight_chart()


# In[17]:


# defining the contents of the main (right-hand) pane in the Panel dashboard
# the contents are dependent upon the answers given and will be updated once the 'submit' button in the sidebar pane is clicked

@pn.depends(button.param.clicks)
def main_display(_):
    
    # setting variables for use in defining dashboard components
    a,b,c,d,e,f = get_values()
    stocks = helpers.get_stocks()
    weights = helpers.get_weights()
    

##########
    # defining contents of tab 0
    

    
    intro_text = tab0.get_intro()
    disclaimer_text = tab0.get_disclaimer()
    
    intro_pane = pn.pane.HTML(intro_text)
    disclaimer_pane = pn.pane.HTML(disclaimer_text)
    

##########
    # defining contents for 'tab 1'  
    # calling image function from outer script to determine which photo to display based upon survey responses    
    photo = image(a,b,c,d,e,f)
    
    p = make_pie()
    bokeh_pane = pn.pane.Bokeh(p, theme="dark_minimal")
    
    df_pane = pn.pane.DataFrame(make_weight_chart(), width=400)
    text_pane = pn.pane.HTML(get_html())
    
    

##########
    # defining contents of 'tab 2'
    
    # calling risk() function from main script to obtain statement regarding risk category
    text=risk(a,b,c,d,e,f)
    
    # defining contents of HTML pane to be display
    html_pane = pn.pane.HTML("""
    <h1>This is an HTML pane</h1>
    
    <br>
    <h2>{}</h2>

      

    <br>
    <h2>We can include a diagram (pie chart) showing portfolio breakdown.
    <br>
    i.e. x% fixed income, y% international equity/stocks, z% US equity/stocks, w% crytpo/etc <h2>

    """.format(text), style={'background-color': '#F6F6F6', 'border': '2px solid black',
                'border-radius': '5px', 'padding': '10px'},sizing_mode='stretch_width')
    
##########
    
    # defining contents of 'tab 3'
    # 
    # define initial image to display. image will be updated when button is clicked
    jpg_pane = pn.pane.JPG('https://www.gstatic.com/webp/gallery/4.sm.jpg', width=500)
    
    # define button to be clicked to change image
    second_button = pn.widgets.Button(name='Click me!')
    
    # define textbox that will display the number of times the button has been clicked
    textb = pn.widgets.TextInput(value="Button has not been clicked yet")
    
    # define function that will switch images when button is clicked
    async def button2(event):
        if (second_button.clicks % 2) != 0:
            jpg_pane.object = "image1.jpg"
        else:
            jpg_pane.object = 'https://www.gstatic.com/webp/gallery/4.sm.jpg'
        textb.value = "Button has been clicked {0} times".format(second_button.clicks)

    # watch/listen for button clicks
    second_button.on_click(button2)
    
    
    
##########

    # defining contents of 'tab 4'
    
    # setup widget to allow user to alter initial investment amount
    # will cause cumulative return graph to be updated
    investment_amount = pn.widgets.Spinner(value=5000, step=500, start=1000, end=100000)
    

    


    # create dynamic object that will display the cumulative return.
    # will be updated as investment amount is changed
    # graph is created using make_chart() function from outer script
    # chart = pn.bind(make_chart,investment_amount,weights,stocks)
    chart = pn.bind(make_chart,investment_amount, weights, stocks)


    
    
##########
    # defining contents of 'tab 5'
    
    # call function to run MC simulation and return plots and statistics
    
    mc_text = tab5.get_text()
    mc_text_pane = pn.pane.HTML(mc_text)
    mc_button = pn.widgets.Button(name="Show MC Simulation Results")
    text_holder = pn.widgets.TextInput(value="")
    tab5_column = pn.Column(mc_text_pane, mc_button, spacer,text_holder, spacer)
   
    
    async def change_pane(event):
        new_text = "new new new"
        neat = "neat neat"
        if (mc_button.clicks == 1):
            text_holder.value = "One moment please and your simulation data will be displayed..."
            simulation_plot, distribution_plot = tab5.prep_MC_data()

            distribution_pane = pn.pane.Matplotlib(distribution_plot, dpi=144)
            tab5_column.append(simulation_plot)
            tab5_column.append(distribution_pane)
            
    async def change_text(event):
      
        if (mc_button.clicks == 1):
            text_holder.value = "One moment please and your simulation data will be displayed..."
             
    mc_button.on_click(change_text)
    mc_button.on_click(change_pane)

    
#     simulation_plot, distribution_plot = tab5.prep_MC_data()
    
#     distribution_pane = pn.pane.Matplotlib(distribution_plot, dpi=144)
    

    # combine main pane components into a tabbed structure and return to main script for usage
    return pn.Tabs(("Tab 0", pn.Row(pn.Column(intro_pane, width=800),pn.Column(disclaimer_pane), sizing_mode='stretch_width')),
                   ("Tab 1", pn.Column("This tab can hold a variety of plots or details about the portfolio selected",photo,spacer,text_pane, df_pane,spacer, bokeh_pane)),
                   ("Tab 2", pn.Row(pn.Column("This tab can hold even more plots or details!!", pn.pane.markup.Markdown(text)),html_pane)),
                   ("Tab 3", pn.Row(pn.Column(jpg_pane,second_button,textb ),"Who Knows?")),
                   ("Tab 4", pn.Column(pn.Row(investment_amount),chart,sizing_mode="stretch_width")),
                   ("Tab 5", pn.Column(tab5_column))
                  )
 
   


# In[18]:


#adding main display area to dashboard

bootstrap.main.append(main_display)


# In[19]:


# displaying dashboard
# if dashboard is being served through a servise this needs to be updated to .servicable() rather than .show()

bootstrap.show()


# In[ ]:





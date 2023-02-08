

import panel as pn
pn.extension(template='bootstrap')
import pandas as pd
import hvplot.pandas
from panel.template import BootstrapTemplate
from pathlib import Path





# initialize the dashboard framework
bootstrap = BootstrapTemplate(title="Portfolio Analysis", header_background = 'blue')





# defining the risk analysis survey questions

questions_dict = {
1: 'What is your current age?',
2: 'I plan to withdraw money from my retirement plan account in:',
3: 'I should have enough savings and stable/guaranteed income (such as, Social Security, pension, retirement plan, annuities) to maintain my planned standard of living in retirement',
4: 'The following statement best describes my willingness to take risk',
5: 'If I invested $100,000 and my portfolio value decreased to $70,000 in just a few months, I would:',
6:  'My assets (excluding home and car) are invested in:'
}





# defining the valid answers to the questions and assigninig points to each answer

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
def image(a,b,c,d,e,f):

    total_score = score(a,b,c,d,e,f)
    if (total_score < 13):
        return "image1.jpg"
    elif (total_score < 29):
        return "image2.jpg"
    else:
        return "image3.jpg"





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





# define functions that will be used inside the main_display function

def get_values():
    return q1.value, q2.value, q3.value, q4.value, q5.value, q6.value


def get_stocks():
    return pd.read_csv(Path("./stocks.csv"), index_col='Date', parse_dates=True, infer_datetime_format=True)

def get_weights():
    return [0.30,0.20,0.40,0.10]


def make_chart(investment, weights, stocks):
    # weight = weights
    allocation = [w * investment for w in weights]
    amount = allocation/stocks.iloc[0]
    stock_value = stocks * amount
    stock_value = stock_value.sum(axis=1).reset_index().rename(columns={0:"Total Value ($)"})
    plot = stock_value.hvplot.line(x="Date", height=500,width=1000)
    return plot





# defining the contents of the main (right-hand) pane in the Panel dashboard
# the contents are dependent upon the answers given and will be updated once the 'submit' button in the sidebar pane is clicked

@pn.depends(button.param.clicks)
def main_display(_):
    
    # setting variables for use in defining dashboard components
    a,b,c,d,e,f = get_values()
    stocks = get_stocks()
    weights = get_weights()
    

##########
    # defining contents of tab 0
    
    # using Markdown to display text
    static = pn.Column(pn.pane.markup.Markdown("# Instructions"),
    pn.pane.markup.Markdown("## Put some instructions here like:"),
    pn.pane.markup.Markdown("* What do you do?\n* What will you see?\n* What's next?"), sizing_mode='stretch_width')

##########
    # defining contents for 'tab 1'  
    # calling image function from outer script to determine which photo to display based upon survey responses    
    photo = image(a,b,c,d,e,f)
    
    
    

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
    investment_amount = pn.widgets.Spinner(name="Investment value in $", value=5000, step=500, start=1000, end=100000)
    

    


    # create dynamic object that will display the cumulative return.
    # will be updated as investment amount is changed
    # graph is created using make_chart() function from outer script
    chart = pn.bind(make_chart,investment_amount,weights,stocks)
    
    

    

    # combine main pane components into a tabbed structure and return to main script for usage
    return pn.Tabs(("Tab 0", static),
                   ("Tab 1", pn.Column("This tab can hold a variety of plots or details about the portfolio selected",photo)),
                   ("Tab 2", pn.Row(pn.Column("This tab can hold even more plots or details!!", pn.pane.markup.Markdown(text)),html_pane)),
                   ("Tab 3", pn.Row(pn.Column(jpg_pane,second_button,textb ),"Who Knows?")),
                   ("Tab 4", pn.Column(pn.Row(investment_amount),chart,sizing_mode="stretch_width"))
                  )
 
   





#adding main display area to dashboard

bootstrap.main.append(main_display)





# displaying dashboard
# if dashboard is being served through a servise this needs to be updated to .servicable() rather than .show()

bootstrap.show()






import panel as pn
pn.extension(template='bootstrap')
import pandas as pd
import hvplot.pandas
from panel.template import BootstrapTemplate

bootstrap = pn.template.BootstrapTemplate(title="Portfolio Analysis")





q1_dict = {'Over 70': 1, '60 to 70': 3, '46 to 59': 7, '45 or younger': 10}
q2_dict = {'Less than 5 years': 1,
                 '5 to 9 years': 3,
                 '10 to 15 years': 6,
                 'More than 15 years': 8}

q3_dict = {'Not confident': 1,
           'Somewhat confident': 2,
           'Confident': 4,
           'Very confident': 6}

q4_dict = {'I’m more concerned with avoiding losses in my account value than with experiencing growth': 1,
           'I desire growth of my account value, but I’m more concerned with avoiding losses': 3,
           'I’m concerned with avoiding losses, but this is outweighed by my desire to achieve growth': 5,
           'To maximize the chance of experiencing high growth, I’m willing to accept losses': 7}

q5_dict = {'Be very concerned and sell my investments': 1,
           'Be somewhat concerned and consider allocating to lower risk investments': 2,
           'Be unconcernded about the temporary fluctuations in my returns': 4,
           'Invest more in my current portfolio': 5}

q6_dict = {"I don't know how my assets are invested": 1,
           "My pension, certificates of deposit, annuities, IRA and savings accounts": 2,
           "A mix of stocks and bonds, including mutual funds": 3,
           "Stocks or stock mutual funds": 4}


q1_name = 'What is your current age?'
q2_name = 'I plan to withdraw money from my retirement plan account in:'
q3_name = 'I should have enough savings and stable/guaranteed income (such as, Social Security, pension, retirement plan, annuities) to maintain my planned standard of living in retirement'
q4_name = 'The following statement best describes my willingness to take risk'
q5_name = 'If I invested $100,000 and my portfolio value decreased to $70,000 in just a few months, I would:'
q6_name = 'My assets (excluding home and car) are invested in:'

spacer = pn.layout.Spacer(margin=10)
text = "Please begin by answering the following questions so we can determine your risk tolerance level"







def risk(a,b,c,d,e,f):
    q1_points = q1_dict[a]
    q2_points = q2_dict[b]
    q3_points = q3_dict[c]
    q4_points = q4_dict[d]
    q5_points = q5_dict[e]
    q6_points = q6_dict[f]
    score = q1_points + q2_points + q3_points + q4_points + q5_points + q6_points
    
    if (score < 13):
        risk = 'Conservative'
    elif (score < 21):
        risk = 'Moderately Conservative'
    elif (score < 29):
        risk = "Moderate"
    elif (score < 35):
        risk = "Moderately Aggressive"
    else:
        risk = "Aggressive"
        
    return f"You scored {score} out of 40, indicating that you are a {risk} investor"

def score(a,b,c,d,e,f):
    q1_points = q1_dict[a]
    q2_points = q2_dict[b]
    q3_points = q3_dict[c]
    q4_points = q4_dict[d]
    q5_points = q5_dict[e]
    q6_points = q6_dict[f]
    return q1_points + q2_points + q3_points + q4_points + q5_points + q6_points


def image(a,b,c,d,e,f):
    q1_points = q1_dict[a]
    q2_points = q2_dict[b]
    q3_points = q3_dict[c]
    q4_points = q4_dict[d]
    q5_points = q5_dict[e]
    q6_points = q6_dict[f]
    score = q1_points + q2_points + q3_points + q4_points + q5_points + q6_points
    
    if (score < 13):
        return "image1.jpg"
    elif (score < 29):
        return "image2.jpg"
    else:
        return "image3.jpg"
        





q1_val = "Unknown"
q1 = pn.widgets.Select(value=list(q1_dict.keys())[0],
                        options = list(q1_dict.keys()), name='')

q2 = pn.widgets.Select(value=list(q2_dict.keys())[0],
                        options = list(q2_dict.keys()), name='')

q3 = pn.widgets.Select(value=list(q3_dict.keys())[0],
                        options = list(q3_dict.keys()), name='')
q4 = pn.widgets.Select(value=list(q4_dict.keys())[0],
                       options = list(q4_dict.keys()), name='')

q5 = pn.widgets.Select(value=list(q5_dict.keys())[0],
                        options = list(q5_dict.keys()), name='')
q6 = pn.widgets.Select(value=list(q6_dict.keys())[0],
                        options = list(q6_dict.keys()), name='')

button = pn.widgets.Button(name="Submit")


bound_risk = pn.bind(risk, a=q1, b=q2, c=q3, d=q4, e=q5, f=q6)
bound_score = pn.bind(score, a=q1, b=q2, c=q3, d=q4, e=q5, f=q6)

header_box2 = pn.WidgetBox(bound_risk)
img = (pn.bind(image, a=q1, b=q2, c=q3, d=q4, e=q5, f=q6))





header_box = pn.WidgetBox(text,width=300, height=75, align='center')

bootstrap.sidebar.append(pn.Row(pn.Column(header_box,
                                          spacer,
                                          spacer,
                                          q1_name,q1,
                                          spacer,
                                          q2_name, q2,
                                          spacer,
                                          q3_name,q3,
                                          spacer,
                                          q4_name, q4,
                                          spacer,
                                          q5_name, q5,
                                          spacer,
                                          q6_name,q6,
                                          spacer,
                                          button
                                         )))








def get_values():
    return q1.value, q2.value, q3.value, q4.value, q5.value, q6.value
    





@pn.depends(button.param.clicks)
def main_display(_):
    a,b,c,d,e,f = get_values()
    
    def image(a,b,c,d,e,f):
        q1_points = q1_dict[a]
        q2_points = q2_dict[b]
        q3_points = q3_dict[c]
        q4_points = q4_dict[d]
        q5_points = q5_dict[e]
        q6_points = q6_dict[f]
        score = q1_points + q2_points + q3_points + q4_points + q5_points + q6_points

        if (score < 13):
            return "image1.jpg"
        elif (score < 29):
            return "image2.jpg"
        else:
            return "image3.jpg"
        
    def textblock(a,b,c,d,e,f):
        q1_points = q1_dict[a]
        q2_points = q2_dict[b]
        q3_points = q3_dict[c]
        q4_points = q4_dict[d]
        q5_points = q5_dict[e]
        q6_points = q6_dict[f]
        score = q1_points + q2_points + q3_points + q4_points + q5_points + q6_points

        if (score < 13):
            risk = 'Conservative'
        elif (score < 21):
            risk = 'Moderately Conservative'
        elif (score < 29):
            risk = "Moderate"
        elif (score < 35):
            risk = "Moderately Aggressive"
        else:
            risk = "Aggressive"

        return f"You scored {score} out of 40, indicating that you are a {risk} investor"
    
    text=textblock(a,b,c,d,e,f)
    static = pn.Column(pn.pane.markup.Markdown("# Instructions"),
    pn.pane.markup.Markdown("## Put some instructions here like:"),
    pn.pane.markup.Markdown("* What do you do?\n* What will you see?\n* What's next?"), sizing_mode='stretch_width')
 
 
        
    return pn.Tabs(("Tab 0", static),
                   ("Tab 1", pn.Column("This tab can hold a variety of plots or details about the portfolio selected",image(a,b,c,d,e,f))),
                   ("Tab 2", pn.Column("This tab can hold even more plots or details!!", pn.pane.markup.Markdown(text))))
 
   
    





bootstrap.main.append(main_display)





bootstrap.show()








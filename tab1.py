import pandas as pd
from bokeh.palettes import Category20c, Category20
from bokeh.plotting import figure
from bokeh.transform import cumsum
from math import pi
import helpers

answers_dict = helpers.get_answers()

def score(a,b,c,d,e,f):
    
    q1_points = answers_dict[1][a]
    q2_points = answers_dict[2][b]
    q3_points = answers_dict[3][c]
    q4_points = answers_dict[4][d]
    q5_points = answers_dict[5][e]
    q6_points = answers_dict[6][f]
    return q1_points + q2_points + q3_points + q4_points + q5_points + q6_points


def make_pie():
    data = helpers.get_weights()
    data['angle'] = data['weight']/data['weight'].sum() * 2*pi
    data['color'] = Category20c[data.shape[0]]
    data['percent'] = data['weight'] * 100

    p = figure(plot_height=350, title="Portfolo Distribution", toolbar_location=None,
               tools="hover", tooltips="@stock: @percent%", x_range=(-0.5, 1.0))

    r = p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend_field='stock', source=data)

    p.axis.axis_label=None
    p.axis.visible=False
    p.grid.grid_line_color = None
    return p
#     x = {
#     'United States': 157,
#     'United Kingdom': 93,
#     'Japan': 89,
#     'China': 63,
#     'Germany': 44,
#     'India': 42,
#     'Italy': 40,
#     'Australia': 35,
#     'Brazil': 32,
#     'France': 31,
#     'Taiwan': 31,
#     'Spain': 29
# }

#     data = pd.Series(x).reset_index(name='value').rename(columns={'index':'country'})
#     data['angle'] = data['value']/data['value'].sum() * 2*pi
#     data['color'] = Category20c[len(x)]

#     p = figure(plot_height=350, title="Pie Chart", toolbar_location=None,
#                tools="hover", tooltips="@country: @value", x_range=(-0.5, 1.0))

#     r = p.wedge(x=0, y=1, radius=0.4,
#             start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
#             line_color="white", fill_color='color', legend_field='country', source=data)

#     p.axis.axis_label=None
#     p.axis.visible=False
#     p.grid.grid_line_color = None
#     return p


def image(a,b,c,d,e,f):

    total_score = score(a,b,c,d,e,f)
    if (total_score < 13):
        return "image1.jpg"
    elif (total_score < 29):
        return "image2.jpg"
    else:
        return "image3.jpg"
    
def get_html():
    text = """
    <H2> The following table and pie chart show distribution of asset types within your selected portfolio</H2>
"""
    return text

def make_weight_chart():
    weights = helpers.get_weights()
    weights['Percent Allocation'] = weights['weight'] * 100
    weights = weights.set_index('stock').drop('weight', axis=1)
    return weights
                                            
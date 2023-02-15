# these functions define 3 text blocks that are displayed on the Introduction tab

def get_intro():
    text = """\
    ## Welcome to the MyWealthPlan Portfolio Selection Tool
    
    ### To begin, please complete the Risk Analysis Survey found in the left-hand side panel. Once you have selected your answers click on the 'submit' button.

    ### Once your answers are submitted a Risk Score will be calculated and you will be placed into one of four Risk Tolerance Categories.

    ### Based upon your Risk Category you will be shown details related to a portfolio of assets that best conforms to your Risk Tolerance Category.

    ### You may naviate through the informational displays by selecting the desired tab from the menu above. The information is organized as follows:

    ----
   
    * "Portfolio Profile" provides information on the allocation of assets between Stocks, Bonds, Cryptocurrencies and Commodoties
    * "Past Performance" provides information regarding the historical performance of the selected portfolio along with a comparison to the historical performance of the S&P 500
    * "Future Performance" provides the results of a Monte Carlo simulation using 200 iterations and can be useful to gauge the potential future performance of the portfolio
   
    """
    
    return text


def get_portfolios_intro():
    text = """\
    
    ----
    ### Based on your answers, you will be matched with one of these five portfolios: 

    """    
    
    return text

def get_disclaimer():
    text = """
    
    ----
    
The information provided on this website is for information and educational purposes only. 
It is not intended to be, nor should be used as, investment advice. 
Seek a duly licensed professional for investment advice.
    
    ----
    
    © 2023 MyWealthPath.
    
    """
    
    return text

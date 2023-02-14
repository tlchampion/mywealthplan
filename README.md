# Portfolio Selection Tool

The Portfolio Selection Tool is a web application designed to determine a user's risk tolerance for investments, and based upon that tolerance present them with information on one of 4 preselected portfolios who's assets align with the user's risk tolerance.  




---

## Technologies

The Portfolio Selection Tool is written in Python and uses the [Panel](https://panel.holoviz.org/index.html) dashboarding solution to present information to the user. 

Visualizations are provided by the [Bokeh](https://bokeh.org) and [Matplotlib](https://matplotlib.org) libraries. 

Details on asset performance are retrieved using the [Alpaca](https://alpaca.markets) API.

The [Pandas](https://pandas.pydata.org) library is used to work with the asset data retrieved from the API.




---

## Installation Guide

The contents of the repository should be placed into the desired folder on the users computer, being sure to maintain the directory structure. 

The following python packages must be installed to run the application locally:
* pandas
* panel
* bokeh
* matplotlib
* yahoo_fin
* numpy

These packages may be individually installed into the environment of your choice or you may create a new conda environment using the included environment.yml file. If you prefer using pip, the included requirements.txt file may be used.









---

## Usage

The Portfolio Selection Tool can be run from the jupyter notebook or by using the included python script. In either case, once launched a new browser tab will be opened displaying a [Panel](https://panel.holoviz.org/index.html) dashboard.

The left-hand portion of the dashboard consists of a six-question risk tolerance questionnaire. Once the questions are answered and the submit button is clicked the a risk tolerance score will be calculated for the user and they will be assigned a risk tolerance category. 

Once determined, the risk tolerance category is used to assign the user to one of four predetermined portfolios that vary in their overall level of investment risk. Details on the assigned portfolio are provided in the tabs found in the right-hand portion of the dashboard.  The following information will presented to the user:


| Tab  |  Contents | Example Image |
|---|---|---|
| Tab0  | Instructions and Disclaimer  |image|
| Tab1  | Portfolio Description, Composition, etc  |image|
| Tab2  | Historic Performance  |image|
| Tab3  | Monte Carlo Simulation |image|

---

## Contributors

* Ahmad Takatkah
* Lourdes
* Patricio Gomez
* Lovedeep Dingh
* Thomas L. Champion

---

## License

License information can be found in the included LICENSE file.

---
## Credits
* Risk Analysis Survey was compiled based upon a survey provided by [Lincoln Financial Group](https://bit.ly/3InwBMP)
* Code for generating the Monte Carlo Simulation was modified from code provided by UC Berkeley Extension FInTech Bootcamp

___
## Future Work

Future work and/or enhancements to this project include:
* implementing a more robust Risk Analysis Survey
* adding in features to allow a user to fine-tuning their portfolio
* leveraging a Machine Learning algorithm


---

## Disclaimer

The information provided through this application is for information and educational purposes only. 
It is not intended to be, nor should it be used as, investment advice. 
Seek a duly licensed professional for investment advice.



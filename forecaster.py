#importing needed python libraries
import pandas as pd
#pandas will be used for working with data sets
import numpy as np
#numpy is a library that will be used for working with arrays and math functions
import matplotlib.pyplot as plt
#matplotlib.pyplot will be used for plotting figures just as in MATLAB
import plotly.graph_objects as go
#plotly.graph_objects will be used for creating plots
import plotly.express as px
#ex will be used for creating the entire figure at once
import plotly.io as pio
#pio will be used for displaying, reading and writing figures
pio.templates.default = "plotly_dark"
#templates object is used to set the template/theme for the current figure
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

#reading the data now
data = pd.read_csv('Netflix-Subscriptions.csv')
#cpnverting the time period column into datetime format (preparing data for analysis)
data['Time Period'] = pd.to_datetime(data['Time Period'], format='%d/%m/%Y')
print(data.head())
#creating a figure for the data set which has quaterly subscription growth for netflix
fig = go.Figure()
fig.add_trace(go.Scatter(x= data['Time Period'],
                         y= data['Subscribers'],
                         mode='lines',
                         name='Subscribers'))
fig.update_layout(title='Netflix Quaterly Subscription Growth',
                  xaxis_title='Date',
                  yaxis_title='Netflix Subscriptions')
fig.show()

#as the above graph formed isn't seasonal, we can use ARIMA model to forecast the quaterly growth rate
data['Quaterly Growth Rate'] = data['Subscribers'].pct_change()*100
#creating a column for bar colors , green for positive growth, red for negative growth)
data['Bar Color'] = data["Quaterly Growth Rate"].apply(lambda x: 'green' if x>0 else 'red')

#Plot the quaterly growth rate using the bar graphs
fig = go.Figure()
fig.add_trace(go.Bar(
    x=data['Time Period'],
    y=data['Quaterly Growth Rate'],
    marker_color=data['Bar Color'],
    name='Quaterly Growth Rate'
))
fig.update_layout(title='Netflix Quaterly Subscription Growth Rate',
                  xaxis_title='Time Period',
                  yaxis_title='Quaterly Growth Rate (%)'
)
fig.show()

#Calculating the yearly growth rate
data['Year'] = data['Time Period'].dt.year
yearly_growth = data.groupby('Year')['Subscribers'].pct_change().filna(0)*100

#create a new column for bar color , green for positive growth, red for negative growth)
data['Bar Color'] = yearly_growth.apply(lambda x: 'green' if x>0 else 'red')

#Plot the yearly subscriber growth rate 
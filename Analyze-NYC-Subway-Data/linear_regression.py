import statsmodels.api as sm
import numpy as np
import pandas
from ggplot import *
import matplotlib.pyplot as plt

def linear_regression(features, values):
    """
    Perform linear regression given a data set with an arbitrary number of features.
    """
    
    features = sm.add_constant(features)
    model = sm.OLS(values, features)
    results = model.fit()
    intercept = results.params[0]
    params = results.params[1:]
    
    print params[0:15]
    return intercept, params
    
def predictions(dataframe):
    '''
    Predict ridership of NYC subway using linear regression 
    '''
   
    features = dataframe[['hour', 'tempi', 'wspdi','rain']] 
    dummy_days = pandas.get_dummies(dataframe['day_week'], prefix='day')
    dummy_conds = pandas.get_dummies(dataframe['conds'], prefix='conds')
    dummy_units = pandas.get_dummies(dataframe['UNIT'], prefix='unit')
    dummy_dates = pandas.get_dummies(dataframe['DATEn'], prefix='date')   
    features = features.join(dummy_days)    
    features = features.join(dummy_conds)
    features = features.join(dummy_units)
    features = features.join(dummy_dates)

    # Values
    values = dataframe['ENTRIESn_hourly']

    # Perform linear regression
    intercept, params = linear_regression(features, values)
    predictions = intercept + np.dot(features, params)
 
    return predictions


def plot_residuals(data, predictions):

    plt.figure()
    (data - predictions).hist(bins = range(-10000,10000,1000))
    plt.show()

    
def compute_r_squared(data, predictions):
    
    
    ymean = np.mean(data)
    denom = np.sum(np.square(data - ymean))
    num = np.sum(np.square(predictions - data))
    r_squared = 1 - (num/denom)
    
    return r_squared

if __name__ == "__main__":
    dataframe = pandas.read_csv('/Users/SherryT/Documents/Projects/Analyze-NYC-Subway-Data/turnstile_weather_v2.csv')
    predictions = predictions(dataframe)
    plot_residuals(dataframe['ENTRIESn_hourly'], predictions)
    r2 =  compute_r_squared(dataframe['ENTRIESn_hourly'], predictions)
    print "R-squared: ", r2
  
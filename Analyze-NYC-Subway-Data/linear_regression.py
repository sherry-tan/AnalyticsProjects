import statsmodels.api as sm
import numpy as np
import pandas

def linear_regression(features, values):
    """
    Perform linear regression given a data set with an arbitrary number of features.
    """
    
    features = sm.add_constant(features)
    model = sm.OLS(values, features)
    results = model.fit()
    intercept = results.params[0]
    params = results.params[1:]
    
    print params[0:5]
    return intercept, params
    
def predictions(dataframe):
    '''
    Predict ridership of NYC subway using linear regression 
    '''
    
    features = dataframe[['precipi', 'Hour', 'meantempi']]
    dummy_units = pandas.get_dummies(dataframe['UNIT'], prefix='unit')
    #dummy_dates = pandas.get_dummies(dataframe['DATEn'], prefix='date')
    features = features.join(dummy_units)
    #features = features.join(dummy_dates)

    # Values
    values = dataframe['ENTRIESn_hourly']

    # Perform linear regression
    intercept, params = linear_regression(features, values)
    predictions = intercept + np.dot(features, params)
 
    return predictions


def plot_residuals(data, predictions):

    plt.figure()
    (turnstile_weather['ENTRIESn_hourly'] - predictions).hist(bins = range(-10000,10000,1000))
    return plt
    
def compute_r_squared(data, predictions):
    
    
    ymean = np.mean(data)
    denom = np.sum(np.square(data - ymean))
    num = np.sum(np.square(predictions - data))
    r_squared = 1 - (num/denom)
    
    return r_squared

turnstile_weather = pandas.read_csv('/Users/SherryT/Documents/AnalyticsProjects/UND/NYC/turnstile_weather_v1.csv')
predictions = predictions(turnstile_weather)
plot_residuals(turnstile_weather['ENTRIESn_hourly'], predictions)
r2 =  compute_r_squared(turnstile_weather['ENTRIESn_hourly'], predictions)
print r2

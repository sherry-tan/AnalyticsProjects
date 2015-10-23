import numpy as np
import pandas
from sklearn.linear_model import SGDRegressor


def normalize_features(features):
    ''' 
    Returns the means and standard deviations of the given features, along with a normalized feature
    matrix.
    ''' 
    means = np.mean(features, axis=0)
    std_devs = np.std(features, axis=0)
    normalized_features = (features - means) / std_devs
    return means, std_devs, normalized_features

def recover_params(means, std_devs, norm_intercept, norm_params):
    ''' 
    Recovers the weights for a linear model given parameters that were fitted using
    normalized features. 
    ''' 
    intercept = norm_intercept - np.sum(means * norm_params / std_devs)
    params = norm_params / std_devs
    return intercept, params

def linear_regression(features, values):
    """
    Perform linear regression given a data set with an arbitrary number of features.
    """
    
    model = SGDRegressor()
    sgd = model.fit(features, values)
    intercept = sgd.intercept_
    params = sgd.coef_


    return intercept, params

def predictions(dataframe):
    '''
     Predict ridership of NYC subway using gradient descent
    '''
  
    features = dataframe[['precipi', 'Hour', 'meantempi']]
    dummy_units = pandas.get_dummies(dataframe['UNIT'], prefix='unit')
    #dummy_dates = pandas.get_dummies(dataframe['DATEn'], prefix='date')
    features = features.join(dummy_units)
    #features = features.join(dummy_dates)
    
    # Values
    values = dataframe['ENTRIESn_hourly']
    
    # Get numpy arrays
    features_array = features.values
    values_array = values.values
    
    means, std_devs, normalized_features_array = normalize_features(features_array)
    m = len(values)

    features['ones'] = np.ones(m) # Add a column of 1s (y intercept)
    # Perform gradient descent
    norm_intercept, norm_params = linear_regression(normalized_features_array, values_array)
    
    intercept, params = recover_params(means, std_devs, norm_intercept, norm_params)
    print params[0:4]
    predictions = intercept + np.dot(features_array, params)
   
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

dataframe = pandas.read_csv('/Users/SherryT/Documents/AnalyticsProjects/UND/NYC/turnstile_weather_v1.csv')
predictions = predictions(dataframe)
plot_residuals(dataframe['ENTRIESn_hourly'], predictions)
r2 =  compute_r_squared(dataframe['ENTRIESn_hourly'], predictions)
print r2
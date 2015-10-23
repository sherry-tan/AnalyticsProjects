import numpy as np
import pandas
import matplotlib.pyplot as plt
import scipy
import scipy.stats

def entries_histogram(dataframe):
    '''
    Looks at distribution of 'ENTRIESn_hourly'when raining vs not raining
    '''
    
    plt.figure()
    
    rain = dataframe[(dataframe.rain==1)]
    norain = dataframe[(dataframe.rain==0)]
    
    # Histograms for hourly entries when raining and not raining
    norain.ENTRIESn_hourly.hist(bins = 25, color ='blue', range=[0,6000], label = 'no rain')    
    rain.ENTRIESn_hourly.hist(bins = 30, color = 'green', range=[0,6000], label = 'rain') 
    plt.title('Histogram of ENTRIESn_hourly')
    plt.xlabel('ENTRIESn_hourly')
    plt.ylabel('Frequency')
    
    plt.legend()
    plt.show()

def mann_whitney_plus_means(dataframe):
    '''
    This function will calculate:
        1) the mean of entries with rain
        2) the mean of entries without rain
        3) the Mann-Whitney U-statistic and p-value comparing the number of entries
           with rain and the number of entries without rain
    
    '''
    wr = dataframe[(dataframe.rain==1)].ENTRIESn_hourly
    wor = dataframe[(dataframe.rain==0)].ENTRIESn_hourly
    with_rain_mean= np.mean(wr)
    without_rain_mean= np.mean(wor)
    U, p = scipy.stats.mannwhitneyu(wr, wor)
    
    return with_rain_mean, without_rain_mean, U, 2*p


dataframe = pandas.read_csv('/Users/SherryT/Documents/AnalyticsProjects/UND/NYC/turnstile_weather_v1.csv')
entries_histogram(dataframe)
    
with_rain_mean, without_rain_mean, U, p = mann_whitney_plus_means(dataframe)
print 'with_rain_mean = %.2f ' %with_rain_mean
print 'without_rain_mean = %.2f'%without_rain_mean
print 'Two-tailed p-value = %.2f' %p
from pandas import *
from ggplot import *


def plot_weather_data(dataframe):

    '''plot variation of total ridership with time'''
    totalride = dataframe.groupby ('Hour', as_index=False).sum()
    plot1 = ( ggplot(aes( x = 'Hour', y= 'ENTRIESn_hourly'), data = totalride) + 
                geom_point() + geom_line() + xlab("Hour") +ylab("Ridership") + 
                ggtitle("Ridership for different times of day")  + xlim (0,23))
    
    print plot1
  

    '''plot variation of mean ridership with unie'''
    ridebysubway = dataframe.groupby (['UNIT'], as_index=False).mean()
    ridebysubway['UNIT'] = ridebysubway['UNIT'].map(lambda x: x.lstrip('R'))
    ridebysubway['UNIT'] = ridebysubway['UNIT'].astype(float)
    
    plot2 = (ggplot(aes(x='UNIT',y='ENTRIESn_hourly'), data=ridebysubway) + geom_point()
            + xlim(0,600))
            
    print plot2
    
    plot3 = (ggplot(aes( x = 'precipi', y= 'ENTRIESn_hourly'), data = dataframe) + 
                geom_point() + geom_line())
                
    print plot3
    #data=dataframe) + geom_boxplot() + 
    #ggtitle("Mean entries for each station")
    #+ xlab("Station number") + ylab("Mean Entries") + xlim(0,600) + ylim(0,15000))
    #dataframe['UNIT'] = dataframe['UNIT'].map(lambda x: x.lstrip('R'))
    #dataframe['UNIT'] = dataframe['UNIT'].astype(float)
    ##plot2 =  (ggplot(dataframe, aes('UNIT','ENTRIESn_hourly')) + geom_boxplot()+ xlim(0,600))
    #print plot2
    
dataframe = pandas.read_csv('/Users/SherryT/Documents/AnalyticsProjects/UND/NYC/turnstile_weather_v1.csv')
plot_weather_data(dataframe)

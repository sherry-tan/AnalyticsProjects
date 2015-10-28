from pandas import *
from ggplot import *


def plot_weather_data(dataframe):

    '''plot variation of total ridership with time'''
    totalride = dataframe.groupby ('hour', as_index=False).mean()
    plot1 = ( ggplot(aes( x = 'hour', y= 'ENTRIESn_hourly'), data = totalride) + 
                geom_point() + geom_line() + xlab("Hour") +ylab("Ridership") + 
                ggtitle("Mean Ridership for different times of day")  + xlim (0,20))
    
    print plot1
  

    '''plot variation of mean ridership with weekday'''
    
    wkride = dataframe.groupby ('day_week', as_index=False).mean()
    plot2 = ( ggplot(aes( x = 'day_week', y= 'ENTRIESn_hourly'), data = wkride) + 
                geom_point() + geom_line() +  xlab("Day of Week") +ylab("Ridership") + 
                ggtitle("Mean Ridership for different days of the week")+
                scale_x_discrete(breaks=[0,1,2,3,4,5,6], labels=["Monday","Tuesday",
                                 "Wednesday", "Thursday", "Friday", "Saturday",
                                 "Sunday"]) +xlim(0,6))
    print plot2
   
  
  

if __name__ == "__main__":
        
    dataframe = pandas.read_csv('/Users/SherryT/Documents/Projects/Analyze-NYC-Subway-Data/turnstile_weather_v2.csv')
    plot_weather_data(dataframe)

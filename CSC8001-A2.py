import csv
import pandas as pd
import numpy as np
import os
from dateutil import parser
# from datetime import datetime


filename = "201507-citibike-tripdata.csv"
dir_path = os.path.dirname(os.path.realpath(__file__))
csv_file_path = os.path.join('data', filename)

# Load CSV
# rides = pd.read_csv(csv_file_path, low_memory=False, parse_dates=[1])
rides = pd.read_csv(csv_file_path, low_memory=False)


# Set Column Name
rides.columns = ['tripduration', 'starttime', 'stoptime', 'start station id', 'start station name', 'start station latitude', 'start station longitude',
                 'end station id', 'end station name', 'end station latitude', 'end station longitude', 'bikeid', 'User Type', 'birth year', 'gender']
rides.rename(columns={'usertype': 'User Type'})


# Set StartTime as index
rides.set_index('starttime')


def a1(rides):
    """
    Most popular stations for all riders
    Function a1() should return a Series object indexed by station names in descending order of popularity.
    """

    five_popular_station_end_trip = rides['end station name'].value_counts().head()
    return five_popular_station_end_trip


def a2(rides):
    """
    Most popular stations for Customers
    Function a2() should return a Series object indexed by station names in descending order of popularity.
    """
    df1 = rides[rides['User Type'] == 'Customer']
    five_popular_station_customers = df1['end station name'].value_counts().head()
    return five_popular_station_customers


def a3(rides):
    """
    Customer rides Visiting Central Park
    Function a3() should return a Series object indexed by station names in descending order of popularity.
    """
    df1 = rides[rides['User Type'] == 'Customer']
    mask = df1['end station name'].str.contains('Central Park')
    central_park_total_rides = df1.loc[mask, 'end station name'].value_counts()
    return central_park_total_rides


def a4(rides):
    """
    Average trip duration for Subscribers
    The mean trip duration for Subscribers on any workday (Monday - Friday)?
    Function a4() should return the mean value (float to two decimals).
    """
    rides['starttime'] = pd.to_datetime(rides['starttime'])

    ## Method 1
    # df = rides
    # df = df[(df.starttime.dt.dayofweek < 5) & df['User Type'].eq('Subscriber')]
    # g = np.round(df.groupby(df.starttime.dt.dayofweek).tripduration.mean(), 2)
    # print g
    # return g

    ## Method 2
    m = (rides['starttime'].dt.dayofweek < 5) & (rides['User Type'] == 'Subscriber')
    mean_trip_duration = round(rides.loc[m, 'tripduration'].mean(), 2)
    print mean_trip_duration
    return mean_trip_duration

    ## with weekday_name
    # df1 = rides[(rides['User Type'] == 'Subscriber') & (rides['starttime'].dt.dayofweek < 5)]
    # return df1.groupby(df1['starttime'].dt.weekday_name)['tripduration'].mean().round(2)


def a5(rides):
    """
    Longest trip duration of any rider
    Function a5() should return an integer.
    """
    print rides.loc[rides['tripduration'].idxmax()]
    # longest_trip = rides['tripduration'].max
    # print longest_trip


# print "\n\tMost popular stations for all riders : \n",a1(rides)
# print "\n\tMost popular stations for Customers : \n", a2(rides)
# print "\n\tCustomer rides Visiting Central Park : \n", a3(rides)
print a4(rides)
# print a5(rides)

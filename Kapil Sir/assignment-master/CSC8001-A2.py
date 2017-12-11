import csv
import pandas as pd
import numpy as np

import seaborn
seaborn.set()
import matplotlib.pyplot as plt

import os
from dateutil import parser
# from datetime import datetime


filename = "201507-citibike-tripdata.csv"
dir_path = os.path.dirname(os.path.realpath(__file__))
csv_file_path = os.path.join('data', filename)

# Load CSV file
# rides = pd.read_csv(csv_file_path, low_memory=False, parse_dates=[1])     # with parse_dates
rides = pd.read_csv(csv_file_path, low_memory=False)                        # without parse_dates


# Set Column Name
rides.columns = ['tripduration', 'starttime', 'stoptime', 'start station id', 'start station name', 'start station latitude', 'start station longitude',
                 'end station id', 'end station name', 'end station latitude', 'end station longitude', 'bikeid', 'User Type', 'birth year', 'gender']

# Rename Column Name
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
    df1 = rides[rides['User Type'] == 'Customer']       # set df as Customer user type
    five_popular_station_customers = df1['end station name'].value_counts().head()  # count 5 most popular station name
    return five_popular_station_customers


def a3(rides):
    """
    Customer rides Visiting Central Park
    Function a3() should return a Series object indexed by station names in descending order of popularity.
    """
    df1 = rides[rides['User Type'] == 'Customer']
    mask = df1['end station name'].str.contains('Central Park')     # mast end station name with Central park
    central_park_total_rides = df1.loc[mask, 'end station name'].value_counts()    # count total rides
    return central_park_total_rides


def a4(rides):
    """
    Average trip duration for Subscribers
    The mean trip duration for Subscribers on any workday (Monday - Friday)?
    Function a4() should return the mean value (float to two decimals).
    """

    rides['starttime'] = pd.to_datetime(rides['starttime'], infer_datetime_format=True)     # parse starttime object to datetime

    # Method 1
    # df = rides
    # df = df[(df.starttime.dt.dayofweek < 5) & df['User Type'].eq('Subscriber')]
    # g = np.round(df.groupby(df.starttime.dt.dayofweek).tripduration.mean(), 2)
    # print g
    # return g

    # Method 2
    m = (rides['starttime'].dt.dayofweek < 5) & (rides['User Type'] == 'Subscriber')    # count rides between weekdays and user is Subscriber
    mean_trip_duration = round(rides.loc[m, 'tripduration'].mean(), 2)  # count mean value and round it to 2 digit
    print mean_trip_duration
    return mean_trip_duration

    # with weekday_name
    # df1 = rides[(rides['User Type'] == 'Subscriber') & (rides['starttime'].dt.dayofweek < 5)]
    # return df1.groupby(df1['starttime'].dt.weekday_name)['tripduration'].mean().round(2)


def a5(rides):
    """
    Longest trip duration of any rider
    Function a5() should return an integer.
    """
    # Method 1
    return rides['tripduration'].max()  # tripduration max value

    # Method 2
    # longest_trip_row = rides.loc[rides['tripduration'].idxmax()]
    # longest_trip_duration = longest_trip_row.tolist()[0]
    # return longest_trip_duration


def a6(rides):
    """
    What is the breakdown of the rides in our data set by user type?
    How many of the rides in our data set are for Customers and how many for Subscribers?
    Function a6() should return a Series object indexed by the rider type.
    """
    df1 = rides.groupby('User Type')  # group rides by Usaer Type
    return df1['User Type'].value_counts()  # Count values of Customers & Subscribers


def a7(rides):
    """
    Weekday usage
    Create a pandas DataFrame with the number of rides by User Type for each day of the week. Use  starttime to determine the rides week day. Your DataFrame should be similar to the one show below, but your data values will vary.
    """
    rides['starttime'] = pd.to_datetime(rides['starttime'], infer_datetime_format=True)

    # cats = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    # days = pd.Categorical(rides.starttime.dt.strftime('%a'), categories=cats, ordered=True)

    df = rides

    # Method 1
    # df = rides.groupby([days, 'User Type']).size().unstack(fill_value=0).assign(All=lambda x: x.sum(1))
    # ## Method 2
    df = pd.crosstab(rides.starttime.dt.dayofweek, rides['User Type']).assign(All=lambda x: x.sum(1))
    return df



def a8(rides):
    """
    Provide a plot which shows the weekday usage pattern by user type. Include a plot line for All weekday rides
    """
    rides['starttime'] = pd.to_datetime(rides['starttime'], infer_datetime_format=True)

    cats = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    days = pd.Categorical(rides.starttime.dt.strftime('%a'), categories=cats, ordered=True)

    df = rides

    df = rides.groupby([days, 'User Type']).size().unstack(fill_value=0).assign(All=lambda x: x.sum(1))

    y_label = 'Daily Rides by User Types'
    x_label = 'Days of the Week'
    title = 'Number of Rides by User Types and Week Day'

    ax = df.plot()
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_title(title)
    plt.show()


def a9(rides):
    """
    Time of day usage
    Create a pandas DataFrame with the number of rides by User Type for each hour of the day. Use starttime to determine each ride's hour. Your DataFrame should be similar to the one show below, but your data values will vary.
    """
    rides['starttime'] = pd.to_datetime(rides['starttime'], infer_datetime_format=True)
    df = pd.crosstab(rides.starttime.dt.strftime("%I%p"), rides['User Type'])
    print df


def a10(rides):
    """
    Provide a plot which shows the time of day usage pattern by user type. Include a plot line for All hourly rides.
    """
    rides['starttime'] = pd.to_datetime(rides['starttime'], infer_datetime_format=True)
    cats = ['12 AM', '01 AM', '02 AM', '03 AM', '04 AM', '05 AM', '06 AM', '07 AM', '08 AM', '09 AM', '10 AM', '11 AM', '12 PM', '01 PM', '02 PM', '03 PM', '04 PM', '05 PM', '06 PM', '07 PM', '08 PM', '09 PM', '10 PM', '11 PM']
    dates = pd.Categorical(rides.starttime.dt.strftime('%I %p'), categories=cats, ordered=True)
    df = pd.crosstab(dates, rides['User Type']).assign(All=lambda x: x.sum(1))

    y_label = 'Hourly Rides by User Types'
    x_label = 'Hours of the Day'
    title = 'Number of Rides by User Types and Hour'

    ax = df.plot()
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_title(title)
    plt.show()



# print "\nMost popular stations for all riders : \n",a1(rides)
# print "\nMost popular stations for Customers : \n", a2(rides)
# print "\nCustomer rides Visiting Central Park : \n", a3(rides)
# print "\nAverage trip duration for Subscribers : \n", a4(rides)
# print "\nLongest trip duration of any rider : \n", a5(rides)
# print \nTotal Numbers of Riders : \n",a6(rides)
# print "\nnumber of rides by User Type for each day of the week :\n", a7(rides)
# a9(rides)
a10(rides)

import csv
import pandas as pd
import numpy as np
import os
from dateutil import parser
from datetime import datetime

filename = "201507-citibike-tripdata.csv"
dir_path = os.path.dirname(os.path.realpath(__file__))
csv_file_path = os.path.join('data', filename)

# Load CSV
rides = pd.read_csv(csv_file_path, low_memory=False, parse_dates=True)

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
    # print rides.sort_values(['User Type'])
    df1 = rides[rides['User Type'] == 'Customer']
    five_popular_station_customers = df1['end station name'].value_counts().head()
    return five_popular_station_customers

def a3(rides):
    rides = rides[rides['User Type'] == 'Customer']
    rides = rides['end station name'].str.contains('Central Park')
    central_park_total_rides = rides.value_counts()
    # central_park_total_rides = rides['end station name'].str.contains('Central Park').value_counts().head()
    return central_park_total_rides
    # return five_popular_station_customers



# print "\nMost popular stations for all riders : \n",a1(rides)
# print "\nMost popular stations for Customers : \n", a2(rides)
print a3(rides)

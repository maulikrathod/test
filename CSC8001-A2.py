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
rides = pd.read_csv(csv_file_path, header=None, low_memory=False)

 # Set StartTime as index
rides.set_index('starttime', inplace=True)


# Set Column Name
rides.columns = ['tripduration', 'starttime', 'stoptime', 'start station id', 'start station name', 'start station latitude', 'start station longitude', 'end station id', 'end station name', 'end station latitude', 'end station longitude', 'bikeid', 'User Type', 'birth year', 'gender' ]

print rides.head()
# print rides['tripduration']

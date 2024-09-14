
# use the strava API, and upload all the activities from a spreadsheet of runs with the following columns:
# date, distance, time, name, notes

# first get API key from environment variable
import os
import requests
import pandas as pd
import json
import datetime

# get the API key
api_key = os.environ['STRAVA_API_KEY']

# read in the spreadsheet
df = pd.read_csv('runs/runs.csv')

# loop through the rows
for index, row in df.iterrows():
    # break after 1 row for testing
    if index == 1:
        break


    # get the date, distance, time, and notes
    date = row['date']
    distance = row['distance']
    time = row['time']
    notes = row['notes']
    name = row['name']

    
    # Parse the date and set the start time to 5 PM
    date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
    start_time = date_obj.replace(hour=17, minute=0, second=0)
    timestamp = int(start_time.timestamp())

    # Process the 'time' variable for elapsed time
    if ':' in time:
        # Assume format is 'minutes:seconds'
        minutes, seconds = map(int, time.split(':'))
        total_seconds = minutes * 60 + seconds
    else:
        # Assume 'time' is in minutes
        total_seconds = int(time) * 60

    # Create the payload
    payload = {
        'name': name,
        'type': 'Run',
        'start_date_local': timestamp,
        'elapsed_time': total_seconds,
        'distance': distance,
        'description': notes
    }


    # make the request
    url = 'https://www.strava.com/api/v3/activities'
    headers = {'Authorization': 'Bearer ' + api_key}
    r = requests.post(url, headers=headers, data=payload)

    # print the response
    print(r.text)

# use the strava API, and upload all the activities from a spreadsheet of runs with the following columns:
# date, distance, time, name, notes

# first get API key from environment variable
import os
import requests
import pandas as pd
import json
import datetime


CLIENT_ID = os.environ['STRAVA_CLIENT_ID']  # Your app's client ID
CLIENT_SECRET = os.environ['STRAVA_CLIENT_SECRET']  # Your app's client secret


# get the access token from the temp file
access_token = None
if os.path.exists('access_token.json'):
    with open('access_token.json', 'r') as f:
        token_data = json.load(f)
        access_token = token_data['access_token']
        refresh_token = token_data['refresh_token']
        expires_at = token_data['expires_at']
        print("Access Token obtained successfully!")

        # if the token is expired, refresh it
        if expires_at < datetime.datetime.now().timestamp():
            print("Token expired, refreshing token")
            token_response = requests.post(
                'https://www.strava.com/oauth/token',
                data={
                    'client_id': CLIENT_ID,
                    'client_secret': CLIENT_SECRET,
                    'refresh_token': refresh_token,
                    'grant_type': 'refresh_token'
                }
            )

            token_data = token_response.json()

            if 'access_token' in token_data:
                access_token = token_data['access_token']
                refresh_token = token_data['refresh_token']
                expires_at = token_data['expires_at']
                print("Access Token obtained successfully!")
                # save the access token to an temp file
                with open('access_token.json', 'w') as f:
                    json.dump(token_data, f)
            else:
                print("Error obtaining access token:", token_data)
                exit()
else:

    # Replace these with your app's details
    REDIRECT_URI = 'http://localhost'  # Redirect URI (must match the one set in your app settings)
    SCOPE = 'read,activity:write'      # Scopes you need

    # Construct the authorization URL
    auth_url = (
        f"https://www.strava.com/oauth/authorize?client_id={CLIENT_ID}"
        f"&response_type=code&redirect_uri={REDIRECT_URI}"
        f"&approval_prompt=force&scope={SCOPE}"
    )

    print("Visit this URL in your browser to authorize the application:")
    print(auth_url)

    authorization_code = input("Enter the code parameter from the URL after authorization: ")

    # Exchange the authorization code for an access token
    token_response = requests.post(
        'https://www.strava.com/oauth/token',
        data={
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': authorization_code,
            'grant_type': 'authorization_code'
        }
    )

    token_data = token_response.json()

    if 'access_token' in token_data:
        access_token = token_data['access_token']
        refresh_token = token_data['refresh_token']
        expires_at = token_data['expires_at']
        print("Access Token obtained successfully!")
        # save the access token to an temp file
        with open('access_token.json', 'w') as f:
            json.dump(token_data, f)
    else:
        print("Error obtaining access token:", token_data)
        exit()


# read in the spreadsheet
df = pd.read_csv('runs/runs.csv')

# loop through the rows
from tqdm import tqdm
for index, row in tqdm(df.iterrows()):
    # get the date, distance, time, and notes
    date = row['date']
    distance = row['distance']
    time = row['time']
    notes = row['notes']
    name = row['name']


    # Parse the date and set the start time to 5 PM
    date_obj = datetime.datetime.strptime(date, '%m/%d/%Y')
    start_time = date_obj.replace(hour=17, minute=0, second=0)
    # Convert start_time to ISO 8601 format
    start_time_iso = start_time.isoformat()

    # Process the 'time' variable for elapsed time
    if ':' in time:
        # Assume format is 'minutes:seconds'
        minutes, seconds = map(int, time.split(':'))
        total_seconds = minutes * 60 + seconds
    else:
        # Assume 'time' is in minutes
        total_seconds = int(time) * 60

    # get distance meters (convert miles to meters)
    distance = float(distance) * 1609.34

    # Create the payload
    print
    payload = {
        'name': name,
        'type': 'Run',
        'start_date_local': start_time_iso,
        'elapsed_time': total_seconds,
        'distance': distance,
        'description': notes
    }


    # make the request
    url = 'https://www.strava.com/api/v3/activities'
    headers = {'Authorization': 'Bearer ' + access_token}
    r = requests.post(url, headers=headers, data=payload)

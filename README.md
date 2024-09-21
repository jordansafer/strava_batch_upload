## Strava Batch Uploader

Upload a large number of runs to strava at once

### Usage

#### CSV preperation

Make a CSV of runs to upload with the following columns:
* date - format is mm/dd/yyyy
* distance - distance in miles
* time - time in minutes, or mm:ss with seconds
* notes - notes from the run
* name - name of the run

Save the file in runs/runs.csv

#### Dependencies

Run to install required dependencies

```
pip install -r requirements.txt
```

#### Running

Set environment variables, from your strava API-application settings, then run the script.

```
export CLIENT_ID=<>
export CLIENT_SECRET=<>
python batch_upload.py
```
If this is your first time running the script, you will be prompted to log in to strava at a given URL. To continue:
1. Open the URL and log in to strava
2. Copy the authentorization token from the new URL after you login
3. Paste the token into the terminal prompt where the script requests it, and hit enter

Your runs will now be uploaded to Strava!!



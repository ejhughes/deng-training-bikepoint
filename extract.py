import os
import json
import time
from datetime import datetime
import requests

# Create timestamp for output file name
timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')  ### strftime: string format time
# Create folder for output file, it's ok if it already exists
data_dir = "data"
os.makedirs(data_dir, exist_ok=True)
# Create output file name with timestamp, in the data folder
filename = f'{data_dir}/{timestamp}.json'


# Set up API endpoint variable
url = "https://api.tfl.gov.uk/BikePoint"

# Set up other varibles
attempts = 1
max_attempts = 3

# Loop to make API call, save response to file, and retry if it fails
while attempts <= max_attempts:
    # Call API
    response = requests.get(url)
    # Record status code
    status_code = response.status_code

    # If status code is 2xx, save the data to a file
    if 200 <= status_code < 300:
        try:   ### Try/except block to catch any errors that may occur while saving the file
            data = response.json()   ### Save the json (data) part of the response then exit the loop .json() isolates the data returned from the API, rather than returning all the results of an API call, including headers, status codes, etc.

            with open(filename, "w") as file:   ###Write the json data response into the file variable created above, called filename, "w" for write
                json.dump(data, file)

            print(f'File {filename} saved successfully')
        except Exception as e:
            print(f'An error occurred while saving the file: {e}')

        break   ### break out of loop if API call is successful

    elif 300 <= status_code < 500:
        print(f'API call failed, status code: {status_code}')
        break   ### for 3xx or 4xx status codes, likely need to make some changes to the API call, so break of out the loop

    else:
        if attempts == max_attempts:
            print(f'Attempt {attempts} failed, status code: {status_code}. Max attempts reached, exiting...')
            break   ### if max attempts reached, exit the loop
        else:
            print(f'Attempt {attempts} failed, status code: {status_code}. Retrying...') 
            time.sleep(30)   #### Wait 30 seconds before retrying the API call
        attempts += 1
           



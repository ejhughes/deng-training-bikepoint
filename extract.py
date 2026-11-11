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
        # Save the json (data) part of the response then exit the loop
        data = response.json()   ### .json() isolates the data returned from the API, rather than returning all the results of an API call, including headers, status codes, etc.

        # Write the json data response into the file variable created above, called filename
        with open(filename, "w") as file:   ### "w" for write
            json.dump(data, file)

        print(f'File {filename} saved successfully')

        break   ### break out of loop if API call is successful

    elif 300 <= status_code < 500:
        print(f'API call failed, status code: {status_code}')
        break   ### for 3xx or 4xx status codes, likely need to make some changes to the API call, so break of out the loop

    else:
        print(f'Attempt {attempts} failed, status code: {status_code}. Retrying...')
        attempt += 1
        time.sleep(30)   #### Wait 30 seconds before retrying the API call
else:
    print(f'API call failed after {max_attempts} attempts, status code: {status_code}')



import os
import json
from datetime import datetime
import requests

# Create timestamp for output file name
timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')  ### strftime: string format time
# Create folder for output file, it's ok if it already exists
data_dir = "data"
os.makedirs(data_dir, exist_ok=True)
# Create output file name with timestamp, in the data folder
filename = f'{data_dir}/{timestamp}.json'
print(filename)

# Set up API endpoint variable
url = "https://api.tfl.gov.uk/BikePoint"

# Call API
response = requests.get(url)

# Save the response from the API as a data variable. 
data = response.json()   ### .json() isolates the data returned from the API, rather than returning all the results of an API call, including headers, status codes, etc.

# Write the json data response into the file variable created above, called filename
with open(filename, "w") as file:   ### "w" for write
    json.dump(data, file)


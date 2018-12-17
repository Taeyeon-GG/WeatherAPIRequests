import requests # HTTP Requests.
import re       # Regular Expressions.

# Get API Key from Open Weather Maps
APIKEY = ""


def getLocation(): # Prompt user for location.
    while(True):

        location = input("Location: ") # Get user input for location & remove whitespace

        if (location == ""): # Check if location string is empty, if so ask again.
            print("Please enter a location")
            continue
        if (re.search(r'[^a-zA-Z,]', location)): # Check if location string contains anything other than letters, if so ask again.
            print("Please enter a location without numbers or symbols")
            continue
        else:
            location.replace(" ", "") # remove whitespace from location string.
            return location


def sendRequest(APIKEY): # Supply APIKEY as parameter
    return requests.get("http://api.openweathermap.org/data/2.5/weather?q=" + getLocation() + "&APPID=" + APIKEY) # Send API call with location parameter and API Key.


def getResults(json_results):

    try:
        loc_name = json_results["name"]
        loc_id = json_results["sys"]["country"]
        desc = re.search("description': '(.+?)',",str(json_results["weather"][0])).group(1) # User Regular Expression to get description of location.
        temp_celsius = round(float(json_results["main"]["temp"]) - 273.15, 1) # Convert returned temp (Kelvin) to Celsius.

        print(f"The Temperature in {loc_name}, {loc_id} is {temp_celsius}℃. The description given is: '{desc}'")

    except KeyError: # make sure valid data was returned from the API call, if not, start again.
        print("Was not able to find information on this location, did you spell it right?\n")
        getResults(sendRequest(APIKEY).json())


getResults(sendRequest(APIKEY).json()) # Start process on file run.

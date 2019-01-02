import re        # Regular Expressions.
import sys       # System Functions.

import requests  # HTTP Requests.

# Get API Key from Open Weather Maps, supplied as Command Line Argument.
APIKEY = sys.argv[1]


def get_location():
    while True:
        location = input("Location: ")

        # Check if location string is empty, if so ask again.
        if not location:
            print("Please enter a location")
            continue

        # Check if location string contains anything other than letters, if so ask again.
        if re.search(r'[^a-zA-Z, ]', location):
            print("Please enter a location without numbers or symbols")
            continue

        # remove whitespace from location string.
        location.replace(" ", "")

        return location


def send_request(APIKEY, location):
    # Send API call with location parameter and API Key.
    return requests.get("http://api.openweathermap.org/data/2.5/weather?q="
                        + location
                        + "&APPID="
                        + APIKEY)


def get_results(json_results):
    try:
        # Get name of returned data.
        loc_name = json_results["name"]

        # Get Country Code of returned data.
        loc_id = json_results["sys"]["country"]

        # User Regular Expression to get description of returned data.
        desc = re.search("description': '(.+?)',", str(json_results["weather"][0])).group(1)

        # Convert returned temp (Kelvin) to Celsius.
        temp_celsius = round(float(json_results["main"]["temp"]) - 273.15, 1)

    except KeyError:  # Handle error when API returns unusable or invalid data.
        print("Was not able to find information on this location, did you spell it right?\n")

        # Start process again.
        display_data(get_results(send_request(APIKEY, get_location()).json()))

    else:
        result_data = (loc_name, loc_id, temp_celsius, desc)  # Location data to be formatted.

        return result_data


def display_data(tuple_loc_data):  # Take location data and format it for user.

    if not tuple_loc_data:
        return
    else:
        print(f"The Temperature in {tuple_loc_data[0]}, {tuple_loc_data[1]} "
              f"is {tuple_loc_data[2]}℃. The description given is: '{tuple_loc_data[3]}'")
        return


display_data(get_results(send_request(APIKEY, get_location()).json()))  # Start process on initialisation.


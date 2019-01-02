import requests # HTTP Requests.
import re       # Regular Expressions.

# Get API Key from Open Weather Maps.
APIKEY = "ac5940b013891b1e87b89938adf18cf8"


def get_location():
    while(True):
        location = input("Location: ")

        # Check if location string is empty, if so ask again.
        if (location == ""):
            print("Please enter a location")
            continue

        # Check if location string contains anything other than letters, if so ask again.
        if (re.search(r'[^a-zA-Z, ]', location)):
            print("Please enter a location without numbers or symbols")
            continue

        # remove whitespace from location string.
        location.replace(" ", "")

        return location


def send_request(APIKEY):
    # Send API call with location parameter and API Key.
    return requests.get("http://api.openweathermap.org/data/2.5/weather?q="
                        + get_location()
                        + "&APPID="
                        + APIKEY)


def get_results(json_results):
    try:
        # Get name of returned data.
        loc_name = json_results["name"]

        # Get Country Code of returned data.
        loc_id = json_results["sys"]["country"]

        # User Regular Expression to get description of returned data.
        desc = re.search("description': '(.+?)',",str(json_results["weather"][0])).group(1)

        # Convert returned temp (Kelvin) to Celsius.
        temp_celsius = round(float(json_results["main"]["temp"]) - 273.15, 1)

    except KeyError:  # Handle error when API returns unusable or invalid data.
        print("Was not able to find information on this location, did you spell it right?\n")

        # Start process again.
        get_results(send_request(APIKEY).json())

    return print(f"The Temperature in {loc_name}, {loc_id} is {temp_celsius}℃. The description given is: '{desc}'")


get_results(send_request(APIKEY).json())  # Start process on initialisation.

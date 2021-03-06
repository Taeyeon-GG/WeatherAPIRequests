import re        # Regular Expressions.
import sys       # System Functions.

import requests  # HTTP Requests.


class InvalidDataException(Exception):
    # Do Exception stuff.
    pass


def get_api_key():
    try:
        key = sys.argv[1]
        return str(key)
    except IndexError:
        exit("Please launch with APIKEY Argument")


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


def send_request(apikey, location):
    # Send API call with location parameter and API Key.
    return requests.get("http://api.openweathermap.org/data/2.5/weather?q="
                        + location
                        + "&APPID="
                        + apikey)


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
        raise InvalidDataException

    result_data = (loc_name, loc_id, temp_celsius, desc)  # Location data to be formatted.

    return result_data


def display_data(tuple_loc_data):  # Take location data and format it for user.

    print(f"The Temperature in {tuple_loc_data[0]}, {tuple_loc_data[1]} "
          f"is {tuple_loc_data[2]}℃. The description given is: '{tuple_loc_data[3]}'")
    return


def main():
    while True:
        try:
            apikey = get_api_key()  # Get API Key from Open Weather Maps, supplied as Command Line Argument.
            parsed_data = get_results(send_request(apikey, get_location()).json())
            display_data(parsed_data)  # Start process on initialisation.
            break
        except InvalidDataException:
            print("Was not able to find information on this location, did you spell it right?\n")


if __name__ == '__main__':
    main()

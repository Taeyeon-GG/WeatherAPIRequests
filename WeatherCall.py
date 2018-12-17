import requests # HTTP Requests
import re       # Regular Expressions

# API Key from Open Weather Map

APIKEY = "8f41886e4509ae7998aa2d428e05ce26"

# Get location for API Call & send

location = (input("Location: ").replace(" ", ""))   # Get user input for location & remove whitespace

r = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+ location +"&APPID=" + APIKEY)     # Send API call with location parameter and API Key

# Data from API Call

json_results = r.json() # Get results in JSON format

loc_name = json_results["name"]
loc_id = json_results["sys"]["country"]
desc = re.search("description': '(.+?)',",str(json_results["weather"][0])).group(1)     # User Regular Expression to get description of location
temp_celsius = round(float(json_results["main"]["temp"]) - 273.15, 1)   # Convert returned temp (Kelvin) to Celsius

# Formatted String with Information

print(f"The Temperature in {loc_name}, {loc_id} is {temp_celsius}. The description given is: '{desc}'")





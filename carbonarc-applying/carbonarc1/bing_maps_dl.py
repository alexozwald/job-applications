# bing_maps_dl.py
import requests
import json

# https://boundingbox.klokantech.com/
# query: New York City, New York
# -74.258843,40.476578
# -73.700233,40.917630

# 40.476578,-74.258843
# 40.917630,-73.700233
lat_sw = "40.476578"
lon_sw = "-74.258843"
lat_ne = "40.917630"
lon_ne = "-73.700233"
NYC_BOUNDING_BOX = f"{lat_sw},{lon_sw},{lat_ne},{lon_ne}"

# bing search
# https://dev.virtualearth.net/REST/v1/LocalSearch/?query={query}&userMapView={lat,lon,lat,lon}&key={BingMapsKey}
# 
# - Latitude of the Southwest corner
# - Longitude of the Southwest corner
# - Latitude of the Northeast corner
# - Longitude of the Northeast corner
query = "coffee"
maxResults = 25  # the max
BINGMAPS_API_KEY = "AqsrQRjyl4yQ4OlpOjuKdZDsh8zlbENgrWZ-ikJit6IQA0vQRDxQn1G08K9F2dUc"
url = f"https://dev.virtualearth.net/REST/v1/LocalSearch/?query={query}&maxResults={maxResults}&userMapView={NYC_BOUNDING_BOX}&key={BINGMAPS_API_KEY}"
print(url)

# make the request
data_raw = requests.get(url).text
data_raw_json = json.loads(data_raw)

# pretty print to file (bounding box results)
with open("./data/coffee_shops_max_bing.json", "w") as file:
	json.dump(data_raw_json, file, indent=4)

# pars: keep data that's actually in NYC only


# pretty print to file (filtered NYC results)
#with open("coffee_shops_nyc.json", "w") as file:
#	json.dump(JSON_DATA, file, indent=4)

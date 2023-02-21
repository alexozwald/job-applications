# bing_maps_dl2.py
import numpy as np
import requests
import json

# https://boundingbox.klokantech.com/
# query: New York City, New York
# 40.476578,-74.258843
# 40.917630,-73.700233
max_lat_sw =  40.476578
max_lon_sw = -74.258843
max_lat_ne =  40.917630
max_lon_ne = -73.700233

lat_diff = 0.441052  # 40.917630 - 40.476578
lon_diff = 0.558610  # 74.258843 - 73.700233
# 0.558610 / 0.441052 = 50 / 39.47763198  ~  50/40 ratio
latSqs = 40
lonSqs = 50

# nyc is taller (more longitudinal) than wide (less latitudinal)

# SW   ->   SE
# SW+1 -> SE+1
# ...  ->  ...
# NW-1 -> NE-1
# NW   ->   NE

# fill grid with coordinates
lat_series = np.linspace(max_lat_sw, max_lat_ne, 40)
lon_series = np.linspace(max_lon_sw, max_lon_ne, 50)
grid = np.empty(shape=(50,40))
for idx_lon, lon_x in enumerate(lon_series):
	for idx_lat, lat_x in enumerate(lat_series):
		grid[idx_lat][idx_lon] = (lat_x, lon_x)

# geographic center of nyc
lat_center =  40.697104  # (40.476578 + 40.917630) / 2
lon_center = -73.979538  # (-74.258843 + -73.700233) / 2

# make smaller grid of sqares
grid2 = np.empty(shape=(49,39))
for idx_sqY, sqSW in enumerate()

# index
idx_series_total = list(range(40*50))
idx_lat_series = list(range(50))
idx_lon_series = list(range(40))

# bing search
BINGMAPS_API_KEY = "AqsrQRjyl4yQ4OlpOjuKdZDsh8zlbENgrWZ-ikJit6IQA0vQRDxQn1G08K9F2dUc"
query = "coffee"
maxResults = 25 #max

# generate url list
url_array = []

url = f"https://dev.virtualearth.net/REST/v1/LocalSearch/?query={query}&maxResults={maxResults}&userMapView={BBOX}&key={BINGMAPS_API_KEY}"
url_array.append(idx, url)




# make the request
data_raw = requests.get(url).text
data_raw_json = json.loads(data_raw)

# pretty print to file (bounding box results)
with open("coffee_shops_max_bing.json", "w") as file:
	json.dump(data_raw_json, file, indent=4)

# pars: keep data that's actually in NYC only


# pretty print to file (filtered NYC results)
#with open("coffee_shops_nyc.json", "w") as file:
#	json.dump(JSON_DATA, file, indent=4)

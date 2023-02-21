import pandas as pd
#import plotly.graph_objs as go
import os.path
import json
import geopy.distance
import numpy as np
import plotly.express as px
from sklearn import neighbors


# files
PLUTO           = "./maps/pluto_22v2.csv"
PLUTO_SM        = "./maps/pluto_22v2_sm.csv"
PLUTO_PRQT      = "./maps/pluto_22v2_sm.parquet"
PLUTOJSON_SM    ="./maps/MapPLUTO22v2_bbl.geojson"  # geojson via https://mapshaper.org/
PLUTOJSON_NBRHD = "./maps/pluto_neighborhood.geojson"
#PLUTOJSON_SM    = "./maps/pluto_sm.geojson"  # OLD

# info for importing
csv_usecols = ['bbl','borough','numbldgs','firecomp','policeprct','yearbuilt','ownername','zipcode','latitude','longitude']
csv_dtypes = {
    'bbl':          np.uint64,
    'borough':      'category',
    'firecomp':     'string',  
    'latitude':     np.float32,
    'longitude':    np.float32,
    'numbldgs':     np.uint32, 
    'ownername':    'string',  
    'policeprct':   np.uint32, 
    'yearbuilt':    np.uint32, 
    'zipcode':      np.uint32,
}
pluto_na_fill = {
    'borough':      "",
    'zipcode':      99999,
    'firecomp':     "",
    'policeprct':   99999,
    'ownername':    "",
    'numbldgs':     99999,
    #'yearbuilt':    99999,
    'bbl':          99999,
}
borough_cat_names = {}


# read in pluto info
if os.path.isfile(PLUTO_PRQT):
    city_csv = pd.read_parquet(PLUTO_PRQT)
elif os.path.isfile(PLUTO_SM):
    city_csv = pd.read_csv(PLUTO_SM, dtype=csv_dtypes)
else:
    # read unninhibited
    df = pd.read_csv(PLUTO, usecols=['bbl','borough','numbldgs','firecomp','policeprct','yearbuilt','ownername','zipcode','latitude','longitude'], low_memory=False)


    print("THE BEFORE ERA")
    print(df.head(), '\n\n')
    print(df.info(), '\n\n')
    print(df.dtypes, '\n\n')
    print(df.memory_usage(), '\n\n')

    # fill bad/NA values of some cells to something nonexistent
    for key, value in pluto_na_fill.items():
        df[key] = df[key].fillna(value=value)

    # change types to something efficient
    df = df.astype(csv_dtypes, errors='ignore')

    # remove rows with no coordinates
    df = df.dropna(axis=0, how='any', subset=['latitude','longitude'])


    print("THE AFTER ERA")
    print(df.info(), '\n\n')
    print(df.dtypes, '\n\n')
    print(df.memory_usage(), '\n\n')


    df.to_parquet(PLUTO_PRQT)
    df.to_csv(PLUTO_SM)
    city_csv = df

# read in maps
with open(PLUTOJSON_SM, 'r') as f:
    nycmap = json.load(f)
with open(PLUTOJSON_NBRHD, 'r') as f:
    nycmap_nbrhd = json.load(f)

# edit coords -> to radians for local mapping
city_csv['latitude'] = city_csv['latitude'].apply(func=np.radians)
city_csv['longitude'] = city_csv['longitude'].apply(func=np.radians)
city_csv['coords'] = list(zip(city_csv['latitude'],city_csv['longitude']))

# set index as bbl (identifier column)
city_csv.set_index('bbl')

# graph 1 - whole city
print("starting map #1...")
#px.choropleth_mapbox(city_csv,
#                     geojson=nycmap,
#                     locations='bbl',
#                     featureidkey="properties.BBL",
#                     color='yearbuilt',
#                     #hover_name='ownername',
#                     #hover_data=['borough', 'yearbuilt'],
#                     #color_continuous_scale=px.colors.sequential.Brwnyl[::-1],
#                     #mapbox_style="carto-positron",
#                     zoom=9, center={"lat": 40.7, "lon": -74.0},
#                     )
print("map #1 finished.")

# graph 2 - neighborhoods
print("starting map #2...")
px.choropleth_mapbox(city_csv,
                     geojson=nycmap_nbrhd,
                     locations='bbl',
                     featureidkey="properties.BBL",
                     color='yearbuilt',
                     #hover_name='ownername',
                     #hover_data=['borough', 'yearbuilt'],
                     #color_continuous_scale=px.colors.sequential.Brwnyl[::-1],
                     #mapbox_style="carto-positron",
                     zoom=9, center={"lat": 40.7, "lon": -74.0},
                     )
print("map #1 finished.")




# separate by years built
# REMOVE 0 AND 999
#tmp_yrs = ~city_csv['yearbuilt'].isin([0,100000])
tmp_yrs = city_csv['yearbuilt'].loc[ ~city_csv['yearbuilt'].isin([0,100000]) ]

min_decade = np.round(tmp_yrs['yearbuilt'].min(), -1)
max_decade = np.uint32(np.ceil(tmp_yrs['yearbuilt'].max() / 10) * 10)
print( min_decade, type(min_decade) )
print( max_decade, type(max_decade) )



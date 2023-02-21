import json
import numpy as np
import pandas as pd
import plotly.express as px
from sklearn import neighbors


DINERS_CSV        = './maps/all_diners.csv'
PLUTO_GEOJSON     = './maps/nycpluto_manhattan.geojson'
PLUTO_CSV         = './maps/pluto_small.csv'

DINERS_DTYPES = {'area':'category', 'venue_name':'string', 'address':'string',
                 'lat':np.float64, 'lon':np.float64, 'tip_count':np.uint32,
                 'rating':np.uint32,'rating_signals':np.uint32, 'price':np.uint32}
PLUTO_DTYPES = {'borough':'category', 'ownername':'string', 'lotarea':np.uint32,
                'bldgarea':np.uint32, 'assesstot':np.uint64, 'bbl':np.uint64,
                'latitude':np.float64, 'longitude':np.float64}
var_renames = {'bbl':'BBL#', 'dist_diner':'Distance (rad)', 'ownername':"Owner's Name",
               'bldgarea':'Building Area', 'lotarea':'Lot Area', 'borough':'Borough',
               'assesstot':'Assess Total', 'dist_diner_rad':'Distance (rad)',
               'dist_diner_ft':'Distance (ft)', 'ddist_min':'Min Distance (ft)',
               'ddist_max':'Max Distance (ft)', 'color':'color'}


## load geojson map
with open(PLUTO_GEOJSON) as f:
    mnhttn_map = json.load(f)

## DINER DATA
# load data
diners = pd.read_csv(DINERS_CSV, usecols=['area','venue_name','address','lat','lon','tip_count','rating','rating_signals','price'])
diners = diners.astype(DINERS_DTYPES, errors='ignore')
diners = diners[diners['area'] == "Manhattan, NY"]

# convert coordinates to radians -> coordinate pairs
diners['lat'] = diners['lat'].apply(func=np.radians)
diners['lon'] = diners['lon'].apply(func=np.radians)
diners['coordinates'] = list(zip(diners['lat'], diners['lon']))

# generate balltree
diner_locs = diners[['lat', 'lon']].to_numpy()
tree = neighbors.BallTree(diner_locs, metric='haversine')


## PLUTO DATA
df = pd.read_csv(PLUTO_CSV)
df = df.dropna(axis=0)
df = df.astype(PLUTO_DTYPES)
df = df.rename(columns={'latitude':'lat', 'longitude':'lon'})

# convert coordinates to radians -> coordinate pairs
df['lat'] = df['lat'].apply(func=np.radians)
df['lon'] = df['lon'].apply(func=np.radians)
df['coordinates'] = list(zip(df['lat'], df['lon']))

# query existing tree of diner locs with lot locs to get distances
lot_locs = df[['lat','lon']].to_numpy()
dist_diner_rad, _ = tree.query(lot_locs, k=1)
df['dist_diner_rad'] = dist_diner_rad
# multiply by radius of earth (20902464 ft)
df['dist_diner_ft'] = df['dist_diner_rad'].apply(lambda x: x*20902464)

# get range for proper colorization
ddist_min = np.round(np.percentile(df['dist_diner_ft'], 20), -2)
ddist_max = np.round(np.percentile(df['dist_diner_ft'], 80), -2)
coloraxis_range = (ddist_min, ddist_max)


# PX choropleth map
fig = px.choropleth_mapbox(df,
                           geojson=mnhttn_map,
                           locations='bbl',
                           featureidkey='properties.bbl',
                           color=df['dist_diner_ft'],
                           range_color=coloraxis_range,
                           color_continuous_scale=px.colors.sequential.Viridis_r,
                           mapbox_style='carto-positron',
                           zoom=13, center={'lat': 40.7831, 'lon': -73.9712},
                           hover_name='ownername',
                           hover_data=['bldgarea', 'lotarea'],
                           labels=var_renames,
                           title=f'Distance to the Nearest Diner, Manhattan',
                           )
fig.show()
fig.write_html(file='./figure.html')

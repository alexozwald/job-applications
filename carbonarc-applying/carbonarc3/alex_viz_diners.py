import numpy as np
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
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
var_renames = {'color':'color', 'bbl':'BBL#', 'dist_diner':'Distance (rad)',
               'ownername':"Owner's Name", 'bldgarea':'Building Area',
               'lotarea':'Lot Area', 'borough':'Borough', 'assesstot':'Assess Total',
               'dist_diner_rad':'Distance (rad)', 'dist_diner_ft':'Distance (ft)',
               'dist_diner_m':'Distance (m)', 'dist_diner_km':'Distance (km)',
               'ddist_min_ft':'Min Distance (ft)', 'ddist_max_ft':'Max Distance (ft)',
               'ddist_min_m':'Min Distance (m)', 'ddist_max_m':'Max Distance (m)',
               'ddist_min_km':'Min Distance (km)', 'ddist_max_km':'Max Distance (km)'}

## load geojson map
with open(PLUTO_GEOJSON) as f:
    mnhttn_map = json.load(f)

## DINERS
# load diner data
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

# query existing tree of diner locs with lot locs to get radian coord distances
lot_locs = df[['lat','lon']].to_numpy()
dist_diner_rad, xxx = tree.query(lot_locs, k=1)
df['dist_diner_rad'] = dist_diner_rad
# multiply by radius of earth (6371000 m = 6371 km = 20902464 ft = 3,958.8 miles)
df['dist_diner_ft'] = df['dist_diner_rad'].apply(lambda x: x*20902464)
df['dist_diner_m'] = df['dist_diner_rad'].apply(lambda x: x*6371000)
df['dist_diner_km'] = df['dist_diner_rad'].apply(lambda x: x*6371)


# sort ranges/colors/datapoints by units for interactive graphing
# get range for proper colorization
ddist_diner = {'ft':'dist_diner_ft', 'm':'dist_diner_m', 'km':'dist_diner_km'}
ddist_min = {'ft': np.percentile(df['dist_diner_ft'], 20),
             'm':  np.percentile(df['dist_diner_m'],  20),
             'km': np.percentile(df['dist_diner_km'], 20)}
ddist_max = {'ft': np.percentile(df['dist_diner_ft'], 80),
             'm':  np.percentile(df['dist_diner_m'],  80),
             'km': np.percentile(df['dist_diner_km'], 80)}
cscheme = {'ft': px.colors.sequential.Viridis_r,
           'm': px.colors.sequential.thermal_r,
           'km': px.colors.sequential.YlOrRd}
units = {'ft':'Feet', 'm':'Meters', 'km':'Kilometers'}


# use Plotly express function to create a choropleth map (start with ft)
#print("Generating Fig...")






fig = px.choropleth_mapbox(df,
                           geojson=mnhttn_map,
                           locations='bbl',
                           featureidkey='properties.bbl',
                           color=ddist_diner['ft'],
                           color_continuous_scale=cscheme['ft'],
                           range_color=(ddist_min['ft'], ddist_min['ft']),
                           mapbox_style='carto-positron',
                           zoom=13, center={'lat': 40.7831, 'lon': -73.9712},
                           hover_name='ownername',
                           hover_data=['bldgarea', 'lotarea'],
                           labels=var_renames,
                           title=f'Distance to the Nearest Diner',
                           )
print(f"ft layout: {fig.layout}\n")
#fig.show()

fig1 = px.choropleth_mapbox(df,
                           geojson=mnhttn_map,
                           locations='bbl',
                           featureidkey='properties.bbl',
                           color=ddist_diner['m'],
                           color_continuous_scale=cscheme['m'],
                           range_color=(ddist_min['m'], ddist_min['m']),
                           mapbox_style='carto-positron',
                           zoom=13, center={'lat': 40.7831, 'lon': -73.9712},
                           hover_name='ownername',
                           hover_data=['bldgarea', 'lotarea'],
                           labels=var_renames,
                           title=f'Distance to the Nearest Diner',
                           )
#print("Fig 1 generated.")
#print("Generating Fig...")
print(f"m layout: {fig1.layout}\n")

fig2 = px.choropleth_mapbox(df,
                           geojson=mnhttn_map,
                           locations='bbl',
                           featureidkey='properties.bbl',
                           color=ddist_diner['km'],
                           color_continuous_scale=cscheme['km'],
                           range_color=(ddist_min['km'], ddist_min['km']),
                           mapbox_style='carto-positron',
                           zoom=13, center={'lat': 40.7831, 'lon': -73.9712},
                           hover_name='ownername',
                           hover_data=['bldgarea', 'lotarea'],
                           labels=var_renames,
                           title=f'Distance to the Nearest Diner',
                           )
#print("Fig 1 generated.")
print(f"km layout: {fig2.layout}\n")
exit()

fig.update_coloraxes()

# scales = scales[10:13]
buttons = []

ddist_min
ddist_max
cscheme



# buttons, temporary figures and colorscales
for i, unit in enumerate(list(units.keys())):
    #colors.append(go.Figure(data=go.Heatmap(z=z,colorscale = scale)).data[0].colorscale)
    buttons.append(dict(method='restyle',
                        label=units[i],
                        visible=True,
                        args=[{'colorscale':[colors[i]],},],
                        ))
fig.color
"""
({
'coloraxis': {'colorbar': {'title': {'text': 'Distance (ft)'}},
              'colorscale': [[0.0, '#fde725'], [0.1111111111111111,
                             '#b5de2b'], [0.2222222222222222, '#6ece58'],
                             [0.3333333333333333, '#35b779'],
                             [0.4444444444444444, '#1f9e89'],
                             [0.5555555555555556, '#26828e'],
                             [0.6666666666666666, '#31688e'],
                             [0.7777777777777778, '#3e4989'],
                             [0.8888888888888888, '#482878'], [1.0, '#440154']]},
})

({
    'coloraxis': {'colorbar': {'title': {'text': 'Distance (m)'}},
                  'colorscale': [[0.0, 'rgb(231, 250, 90)'], [0.09090909090909091,
                                 'rgb(246, 211, 70)'], [0.18181818181818182,
                                 'rgb(251, 173, 60)'], [0.2727272727272727,
                                 'rgb(246, 139, 69)'], [0.36363636363636365,
                                 'rgb(225, 113, 97)'], [0.45454545454545453,
                                 'rgb(193, 100, 121)'], [0.5454545454545454,
                                 'rgb(158, 89, 135)'], [0.6363636363636364,
                                 'rgb(126, 77, 143)'], [0.7272727272727273,
                                 'rgb(93, 62, 153)'], [0.8181818181818182, 'rgb(53,
                                 50, 155)'], [0.9090909090909091, 'rgb(13, 48,
                                 100)'], [1.0, 'rgb(3, 35, 51)']]},
    'legend': {'tracegroupgap': 0},
    'mapbox': {'center': {'lat': 40.7831, 'lon': -73.9712},
               'domain': {'x': [0.0, 1.0], 'y': [0.0, 1.0]},
               'style': 'carto-positron',
               'zoom': 13},
    'template': '...',
    'title': {'text': 'Distance to the Nearest Diner'}
})

({
    'coloraxis': {'colorbar': {'title': {'text': 'Distance (km)'}},
                  'colorscale': [[0.0, 'rgb(255,255,204)'], [0.125,
                                 'rgb(255,237,160)'], [0.25, 'rgb(254,217,118)'],
                                 [0.375, 'rgb(254,178,76)'], [0.5,
                                 'rgb(253,141,60)'], [0.625, 'rgb(252,78,42)'],
                                 [0.75, 'rgb(227,26,28)'], [0.875,
                                 'rgb(189,0,38)'], [1.0, 'rgb(128,0,38)']]},
})
"""

for idx, x in enumerate():
    print(f"Generating Fig {idx}...")








"""
for idx, x in enumerate(['ft','m','km']):
    print(f"Generating Fig {idx}...")
    figX = px.choropleth_mapbox(df,
                                geojson=mnhttn_map,
                                locations='bbl',
                                featureidkey='properties.bbl',
                                color=ddist_diner[x],
                                color_continuous_scale=cscheme[x],
                                range_color=(ddist_min[x], ddist_min[x]),
                                mapbox_style='carto-positron',
                                zoom=13, center={'lat': 40.7831, 'lon': -73.9712},
                                hover_name='ownername',
                                hover_data=['bldgarea', 'lotarea'],
                                labels=var_renames,
                                title=f'Distance to the Nearest Diner ({x})'
                                )
    fig.add_trace(figX.data)
    print(f"Fig {idx} generated + appended.")
"""




"""
print("Generating Fig 2...")
fig1 = px.choropleth_mapbox(df,
                           geojson=mnhttn_map,
                           locations='bbl',
                           featureidkey='properties.bbl',
                           color='dist_diner_km',
                           color_continuous_scale=px.colors.sequential.YlOrRd,
                           range_color=(ddist_min_km, ddist_max_km),
                           mapbox_style='carto-positron',
                           zoom=13, center={'lat': 40.7831, 'lon': -73.9712},
                           hover_name='ownername',
                           hover_data=['bldgarea', 'lotarea'],
                           labels=var_renames,
                           title='Distance to the Nearest Diner (km)',
                           )
print("Fig 2 generated.")
"""


# Add dropdown
fig0.update_layout(
    updatemenus=[
        dict(
            type = "buttons",
            direction = "left",
            buttons=list([
                dict(
                    args=["type", "surface"],
                    label="3D Surface",
                    method="restyle"
                ),
                dict(
                    args=["type", "heatmap"],
                    label="Heatmap",
                    method="restyle"
                )
            ]),
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.11,
            xanchor="left",
            y=1.1,
            yanchor="top"
        ),
    ]
)


#print(fig0)
#with open("./figurefile.json", 'w') as f:
#    x = print(fig0)
#    f.write(x)



#new_var_names.setdefault(None,"variable")
#fig0.for_each_trace(lambda t: t
#                   .update(name = new_var_names[t.name] or 'variable',
#                           legendgroup = new_var_names[t.name] or 'variable',
#                           hovertemplate = t.hovertemplate.replace(t.name, new_var_names[t.name])))

#print(f"fig0.layout = ", fig0.layout, '\n')
#print(f"fig0.frames = ", fig0.frames, '\n')

#fig0.update_mapboxes()
#fig0.update()

fig0.show()


#NYC_NEIGHBORHOODS

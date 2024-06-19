#!/Users/g_joss/anaconda3/envs/geo_realm/bin/python

import sys
import geopandas as gp
import folium as fol
from branca.colormap import linear
import pandas as pd
from geopy.geocoders import Nominatim
import numpy as np

# Check for command line argument
if len(sys.argv) != 2:
    print("Usage: script.py <N>")
    sys.exit(1)

N = int(sys.argv[1])

# Read the shapefile
gdf = gp.read_file('il_counties_shp/il_by_county.shp')

gdf['COUNTYFP'] = gdf['COUNTYFP'].map(lambda x: int(x))
# Trim unused attributes
gdf = gdf[['NAME', 'COUNTYFP', 'STATEFP', 'geometry']]
gdf.to_file("IL_county.geojson", driver='GeoJSON')

# Read the population data
pop = pd.read_csv('tidied_data.txt')
pop = pop[pop['state_no'] == 17]

# Merge the GeoDataFrame with the population data
d = gdf.merge(pop, how='left', left_on='COUNTYFP', right_on='County_no')
d = d[['NAME', 'COUNTYFP', 'Population', 'geometry']]

# Identify the top N counties by population
top_n_counties = d.nlargest(N, 'Population')

# Exclude the top N counties from the Choropleth data
choropleth_data = d[~d['COUNTYFP'].isin(top_n_counties['COUNTYFP'])]

# Geocode Bloomington, IL
gc = Nominatim(user_agent="my-app")
b = gc.geocode('Bloomington, IL')
x, y = b.latitude, b.longitude

# Create the map
m = fol.Map(location=[x, y], zoom_start=6.25)

# Add different tile layers
tiles = ['stamenwatercolor', 'cartodbpositron', 'openstreetmap', 'stamenterrain']
for tile in tiles:
    fol.TileLayer(tile).add_to(m)

# Add the Choropleth layer for counties excluding top N
fol.Choropleth(
    geo_data=choropleth_data,
    data=choropleth_data,
    columns=["COUNTYFP", "Population"],
    key_on="feature.properties.COUNTYFP",
    legend_name="Population",
    name='Population',
    fill_color='RdYlBu',
    nan_fill_opacity=0.9,
    nan_fill_color='#ffffff',
).add_to(m)

# Add tooltips
tt_count = fol.GeoJsonTooltip(fields=['NAME', 'Population'])

# Add GeoJson layer for all counties to enable tooltips
fol.GeoJson(
    data=d,
    tooltip=tt_count,
    name="IL Counties",
    style_function=lambda feature: {
        'fillOpacity': 0.2,
        'weight': 0.5,
    }
).add_to(m)

# Add black color and blue border for top N counties with tooltips
fol.GeoJson(
    data=top_n_counties,
    tooltip=tt_count,
    name="Top N Counties",
    style_function=lambda feature: {
        'fillColor': 'black',
        'color': 'blue',
        'weight': 1.5,
        'fillOpacity': 1
    }
).add_to(m)

# Add LayerControl so that you can turn on/off layers
fol.LayerControl().add_to(m)

# Save the map to an HTML file
m.save(f"top_{N}.html")

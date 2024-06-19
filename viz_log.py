#!/Users/g_joss/anaconda3/envs/geo_realm/bin/python

import geopandas as gp
import folium as fol
from branca.colormap import linear
import pandas as pd
from geopy.geocoders import Nominatim
import numpy as np

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

# Add a column with the log of the population
d['log_population'] = np.log(d['Population'] + 1)  # Adding 1 to avoid log(0)

d.to_file('county_with_pop.geojson', driver='GeoJSON')

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

# Add the Choropleth layer with log population
fol.Choropleth(
    geo_data=d,
    data=d,
    columns=["COUNTYFP", "log_population"],
    key_on="feature.properties.COUNTYFP",
    legend_name="Log of Population",
    name='Log Population',
    fill_color='RdYlBu',
    nan_fill_opacity=0.9,
    nan_fill_color='#ffffff',
).add_to(m)

# Add tooltips
tt_count = fol.GeoJsonTooltip(fields=['NAME','log_population', 'Population'])
fol.GeoJson(
    data=d,
    tooltip=tt_count,
    name="IL Counties",
    style_function=lambda feature: {
        'fillOpacity': .001,
        'weight': .5,
    }
).add_to(m)

# Add LayerControl so that you can turn on/off layers
fol.LayerControl().add_to(m)

# Save the map to an HTML file
m.save("index_log.html")


#!/Users/g_joss/anaconda3/envs/geo_realm/bin/python

import geopandas as gp
import folium as fol
from branca.colormap import linear
import pandas as pd
from geopy.geocoders import Nominatim
import geopy
#from geopy.geocoders import options
#from geopy import geocoder
import numpy as np

gdf = gp.read_file('il_counties_shp/il_by_county.shp')

gdf['COUNTYFP'] = gdf['COUNTYFP'].map( lambda x : int(x)) 
# trim un used attrs
gdf = gdf[['NAME','COUNTYFP','STATEFP','geometry']]
gdf.to_file("IL_county.geojson", driver='GeoJSON');

pop = pd.read_csv('tidied_data.txt')
pop =pop[pop['state_no']==17]

d=gdf.merge(pop, how='left', left_on='COUNTYFP',right_on='County_no')

d=d[['NAME','COUNTYFP','Population','geometry']]
d.to_file('county_with_pop.geojson', driver='GeoJSON')

geopy.geocoders.options.default_user_agent = "my-application"
gc=Nominatim(user_agent="my-app")
b=gc.geocode('Bloomington,IL')
x,y=b.latitude,b.longitude

m = fol.Map(location=[x,y], zoom_start=6.25)

tiles = ['stamenwatercolor', 'cartodbpositron', 'openstreetmap', 'stamenterrain']
for tile in tiles:
    fol.TileLayer(tile).add_to(m)
    
fol.Choropleth(
    geo_data=d,
    data=d,
    columns=["COUNTYFP","Population"],
    key_on="feature.properties.COUNTYFP",
    legend_name="Counties in ACS1",
    name='Population',
    fill_color='RdYlBu',
    nan_fill_opacity=0.9, 
    nan_fill_color='#ffffff',
).add_to(m)

tt_count = fol.GeoJsonTooltip(fields=['NAME','Population'])
fol.GeoJson(data=d, 
            tooltip=tt_count, 
            name="IL Counties",
            style_function=lambda feature: {
                'fillOpacity' : .001,
                'weight':.5,
                }
           ).add_to(m)

# add LayerControl so that you can turn on/off layers
fol.LayerControl().add_to(m)

m.save("index.html")

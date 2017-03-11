"""
Names: Yuval Shavit, David Barda, Aviv Yaish
Filename: viz.py
Description: Prepares the maps for the heatmap visualization.
Usage: python viz.py
"""

from data.folium.build.lib.folium import folium
import pandas as pd
import math
import project_commons

print("--- Start loading data... ---")

GEO_PATH = r'./data/Community_Areas.json'
crime_data = pd.read_csv(project_commons.PROCESSED_CRIME_DATA)

print("--- Finish load data ---")

html = "["

# Create a map for each temperature
for temp, crime_data_temp in crime_data.groupby('Temp'):
    print("------ Creating map for temp: " + str(temp))

    # Group data according to community area
    crime_data_temp = crime_data_temp['Community Area'].dropna()
    crime_data_temp = pd.to_numeric(crime_data_temp, errors='coerce', downcast='integer')
    crime_data_temp = crime_data_temp.apply(str)
    crime_data_temp = crime_data_temp.value_counts()

    # Create the scale for the map
    step = math.ceil(max(list(crime_data_temp)) / 6)
    scale = list(range(0, 6 * step, step))

    # Further work on the data
    crime_data_temp = pd.DataFrame(crime_data_temp)
    crime_data_temp['c'] = crime_data_temp.index
    crime_data_temp.columns = ['Count', 'Community Area']
    crime_data = crime_data[['Primary Type', 'Description', 'Latitude', 'Longitude']].dropna()

    # Create map
    map_osm = folium.Map(location=[41.8333925, -87.4519716,10], tiles='CartoDB positron', zoom_start=10)
    map_osm.choropleth(geo_path=GEO_PATH, data=crime_data_temp,
                       columns=['Community Area', 'Count'],
                       key_on='feature.properties.area_numbe',
                       threshold_scale=scale,
                       line_color='black',
                       fill_color='YlOrRd', fill_opacity=0.7, line_opacity=0.3,
                       legend_name='Crime count for ' + str(temp) + ' C',
                       highlight=True)

    # Save in file
    html += "'" + str(temp) + "', "
    map_osm.save('static/maps/temp_' + str(temp) + '.html')

html += "]"

print("--- Finish Process! ---")


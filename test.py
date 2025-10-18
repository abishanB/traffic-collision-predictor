import folium
from folium.plugins import HeatMap
import pandas as pd
df = pd.read_csv("traffic_collisions.csv")
location_counts = df.groupby(['LAT', 'LONG']).size().reset_index(name='count')

# Convert to a list of [lat, lon, weight]
heat_data = [[row['LAT'], row['LONG'], row['count']]
             for _, row in location_counts.iterrows()]
gradient = {
    0.05: 'darkblue',
    0.3: 'blue',
    0.4: 'cyan',
    0.5: 'yellow',
    0.75: 'orange',
    1.0: 'red'
}
m = folium.Map(location=[43.7, -79.4], zoom_start=11, tiles='cartodbpositron')
HeatMap(heat_data, radius=14, blur=14,
        min_opacity=0.3, gradient=gradient).add_to(m)
m.save('weighted_collision_heatmap.html')

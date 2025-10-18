import folium
from folium.plugins import HeatMap
import pandas as pd

df = pd.read_csv("traffic_collisions.csv")
injury_fatal_df = df[(df['FATALITIES'] > 0) | (df['INJURY'] == "YES")]

gradient = {
    0.1: "#0000FF",  # Deep Blue
    0.2: "#0033FF",  # Bright Blue
    0.3: "#0066FF",  # Sky Blue
    0.4: "#0099FF",  # Cyan-Blue
    0.5: "#00CCFF",  # Light Cyan
    0.6: "#66FF66",  # Green-Yellow Transition
    0.7: "#FFFF00",  # Yellow
    0.8: "#FF9900",  # Orange
    0.9: "#FF3300",  # Bright Red-Orange
    1.0: "#FF0000"  # Deep Red
}


def createCollisionHeatMap(data, file_name):
  location_counts = data.groupby(
    ['LAT', 'LONG']).size().reset_index(name='count')

  heat_data = [[row['LAT'], row['LONG'], row['count']]
               for _, row in location_counts.iterrows()]
  m = folium.Map(location=[43.7, -79.4],
                 zoom_start=11, tiles='cartodbpositron')
  HeatMap(heat_data, radius=14, blur=14,
          min_opacity=0.2, gradient=gradient).add_to(m)
  m.save(f'./heatmaps/{file_name}.html')


createCollisionHeatMap(df, "collisions_heatmap")
createCollisionHeatMap(injury_fatal_df, "injury_fatal_heatmap")

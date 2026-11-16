import folium
import pandas as pd
import os

def generate_mobility_map(df, lat_col='latitude', lon_col='longitude', output_dir="reports/maps"):
    """
    Generates an interactive HTML map plotting retail mobility coordinates.
    Requires validated latitude and longitude columns to visualize footfall density.
    """
    if df.empty:
        print("Dataset is empty. Cannot generate map.")
        return

    os.makedirs(output_dir, exist_ok=True)
    
    # Center map on the mean coordinates of the dataset
    center_lat = df[lat_col].mean()
    center_lon = df[lon_col].mean()
    mobility_map = folium.Map(location=[center_lat, center_lon], zoom_start=13, tiles='CartoDB positron')
    
    # Plot mobility data points
    for idx, row in df.iterrows():
        folium.CircleMarker(
            location=[row[lat_col], row[lon_col]],
            radius=4,
            color='darkorange',
            fill=True,
            fill_color='darkorange',
            fill_opacity=0.7
        ).add_to(mobility_map)
        
    filepath = os.path.join(output_dir, 'retail_mobility_map.html')
    mobility_map.save(filepath)
    print(f"Interactive mobility map saved successfully to {filepath}")

if __name__ == "__main__":
    print("GeoPulse Geospatial Mapping Module initialized.")

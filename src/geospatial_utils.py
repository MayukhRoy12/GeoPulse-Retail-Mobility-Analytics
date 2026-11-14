import pandas as pd

def validate_coordinates(df, lat_col='latitude', lon_col='longitude'):
    """
    Validates geospatial coordinates in the mobility dataset.
    Ensures latitudes are between -90 and 90, and longitudes between -180 and 180.
    """
    if lat_col not in df.columns or lon_col not in df.columns:
        raise ValueError("Latitude or Longitude columns missing from dataset.")
        
    valid_lat = df[lat_col].between(-90, 90)
    valid_lon = df[lon_col].between(-180, 180)
    
    valid_df = df[valid_lat & valid_lon]
    invalid_count = len(df) - len(valid_df)
    
    print(f"Coordinate validation complete. Dropped {invalid_count} invalid records.")
    return valid_df

if __name__ == "__main__":
    print("Geospatial validation utility initialized.")

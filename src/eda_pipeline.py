import pandas as pd
import os
from eda_visualizations import plot_missing_values, plot_mobility_distribution
from geospatial_mapping import generate_mobility_map
from time_series_analysis import analyze_temporal_trends
from pipeline import run_preprocessing_pipeline

def run_exploratory_data_analysis(filepath):
    """
    Executes the complete Exploratory Data Analysis (EDA) workflow.
    Generates visualizations, maps, and temporal trends for GeoPulse.
    """
    print("Starting Automated EDA Pipeline...")
    
    # Ensure report directories exist
    os.makedirs("reports/figures", exist_ok=True)
    os.makedirs("reports/maps", exist_ok=True)
    
    # Load and clean data using the Week 1 pipeline
    df = run_preprocessing_pipeline(filepath, date_columns=['timestamp'])
    
    if df.empty:
        print("Dataset is empty after cleaning. Aborting EDA.")
        return
        
    print("Generating Missing Values Heatmap...")
    plot_missing_values(df)
    
    # Assuming 'dwell_time_minutes' is a metric in the mock data
    print("Plotting Mobility Distributions...")
    plot_mobility_distribution(df, 'dwell_time_minutes')
    
    print("Generating Temporal Trends...")
    analyze_temporal_trends(df, 'timestamp')
    
    print("Generating Interactive Mobility Map...")
    generate_mobility_map(df, lat_col='latitude', lon_col='longitude')
    
    print("EDA Pipeline Complete. Check the 'reports/' directory for outputs.")

if __name__ == "__main__":
    print("EDA Pipeline module ready for execution.")

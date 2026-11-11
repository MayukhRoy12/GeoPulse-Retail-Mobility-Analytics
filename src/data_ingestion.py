import pandas as pd
import os

def load_retail_data(filepath):
    """
    Loads retail mobility data from a CSV file for the GeoPulse project.
    Ensures the file exists and performs preliminary data validation.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Data file not found at: {filepath}")
    
    print(f"Loading data from {filepath}...")
    df = pd.read_csv(filepath)
    
    # Initial data validation and profiling checks
    print(f"Dataset Shape: {df.shape}")
    print("Missing Values Summary:")
    print(df.isnull().sum())
    
    return df

if __name__ == "__main__":
    print("GeoPulse Data Ingestion Module Initialized.")
    print("Ready to ingest and validate retail mobility datasets.")

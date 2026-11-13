import os
import pandas as pd
from data_ingestion import load_retail_data
from data_cleaning import handle_missing_values, standardize_date_columns

def run_preprocessing_pipeline(filepath, date_columns=None):
    """
    Executes the end-to-end data preprocessing pipeline for GeoPulse.
    Combines data ingestion and cleaning modules.
    """
    print("Starting GeoPulse Preprocessing Pipeline...")
    
    # 1. Ingest Data
    df = load_retail_data(filepath)
    
    # 2. Clean Data (Drop missing for baseline)
    df_cleaned = handle_missing_values(df, strategy='drop')
    
    # 3. Standardize Dates
    if date_columns:
        df_cleaned = standardize_date_columns(df_cleaned, date_columns)
        
    print(f"Pipeline complete. Final Dataset Shape: {df_cleaned.shape}")
    return df_cleaned

if __name__ == "__main__":
    print("Pipeline module ready. Awaiting data execution.")

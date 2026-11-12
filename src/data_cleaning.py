import pandas as pd
import numpy as np

def handle_missing_values(df, strategy='drop', fill_value=None):
    """
    Handles missing values in the retail mobility dataset.
    Strategies: 'drop', 'fill_mean', 'fill_constant'
    """
    if strategy == 'drop':
        return df.dropna()
    elif strategy == 'fill_mean':
        return df.fillna(df.mean(numeric_only=True))
    elif strategy == 'fill_constant':
        if fill_value is None:
            raise ValueError("fill_value must be provided for 'fill_constant' strategy.")
        return df.fillna(fill_value)
    else:
        raise ValueError("Invalid strategy provided.")

def standardize_date_columns(df, date_columns):
    """
    Converts specified columns to datetime format for time-series analysis.
    """
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

if __name__ == "__main__":
    print("GeoPulse Data Cleaning Module Initialized.")
    print("Ready to process and sanitize datasets.")

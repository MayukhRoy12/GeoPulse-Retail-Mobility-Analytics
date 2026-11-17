import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def analyze_temporal_trends(df, datetime_col='timestamp', output_dir="reports/figures"):
    """
    Analyzes temporal mobility trends by extracting hour and day of week.
    Generates time-series visualizations for retail footfall.
    """
    if datetime_col not in df.columns:
        print(f"Datetime column '{datetime_col}' not found.")
        return df

    # Ensure datetime type and drop invalid timestamps
    df[datetime_col] = pd.to_datetime(df[datetime_col], errors='coerce')
    df_valid = df.dropna(subset=[datetime_col]).copy()
    
    # Extract temporal features
    df_valid['hour'] = df_valid[datetime_col].dt.hour
    df_valid['day_of_week'] = df_valid[datetime_col].dt.day_name()
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Hourly Trend Plot
    plt.figure(figsize=(10, 5))
    hourly_counts = df_valid.groupby('hour').size()
    sns.lineplot(x=hourly_counts.index, y=hourly_counts.values, marker='o', color='crimson')
    plt.title('Hourly Retail Mobility Trend - GeoPulse')
    plt.xlabel('Hour of Day')
    plt.ylabel('Mobility Events / Footfall')
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'hourly_trend.png'))
    plt.close()
    
    print("Temporal analysis complete. Hourly trend plot saved successfully.")
    return df_valid

if __name__ == "__main__":
    print("GeoPulse Time-Series Analysis Module initialized.")

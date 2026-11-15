import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_missing_values(df, output_dir="reports/figures"):
    """
    Generates and saves a heatmap of missing values in the retail dataset.
    Helps identify gaps in location or timestamp tracking.
    """
    os.makedirs(output_dir, exist_ok=True)
    plt.figure(figsize=(10, 6))
    sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
    plt.title('Missing Values Heatmap - GeoPulse')
    plt.tight_layout()
    
    filepath = os.path.join(output_dir, 'missing_values_heatmap.png')
    plt.savefig(filepath)
    plt.close()
    print(f"Missing values heatmap saved to {filepath}")

def plot_mobility_distribution(df, column_name, output_dir="reports/figures"):
    """
    Plots the statistical distribution of a specified mobility metric.
    Useful for visualizing footfall or dwell time distributions.
    """
    if column_name not in df.columns:
        print(f"Column '{column_name}' not found in dataset.")
        return
        
    os.makedirs(output_dir, exist_ok=True)
    plt.figure(figsize=(10, 6))
    sns.histplot(df[column_name], kde=True, bins=30, color='royalblue')
    plt.title(f'Distribution of {column_name}')
    plt.xlabel(column_name)
    plt.ylabel('Frequency')
    
    filepath = os.path.join(output_dir, f'{column_name}_distribution.png')
    plt.savefig(filepath)
    plt.close()
    print(f"Distribution plot for {column_name} saved to {filepath}")

if __name__ == "__main__":
    print("GeoPulse EDA Visualization module initialized.")

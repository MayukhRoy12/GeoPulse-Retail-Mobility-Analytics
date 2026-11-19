import os
import sys
import pandas as pd
import streamlit as st

# Allow importing preprocessing utilities from src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from data_cleaning import handle_missing_values, standardize_date_columns
from geospatial_utils import validate_coordinates

st.set_page_config(
    page_title="GeoPulse | Hyper-Local Retail Mobility Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_and_prepare_data(uploaded_file):
    df = pd.read_csv(uploaded_file)
    df = handle_missing_values(df, strategy="drop")
    if "timestamp" in df.columns:
        df = standardize_date_columns(df, ["timestamp"])
    if {"latitude", "longitude"}.issubset(df.columns):
        df = validate_coordinates(df)
    return df

def main():
    st.title("GeoPulse: Hyper-Local Retail Mobility Analytics")
    st.caption("Interactive dashboard for analyzing footfall density, dwell times, and temporal retail trends.")

    st.sidebar.header("Data & Filters")
    uploaded_file = st.sidebar.file_uploader("Upload Retail Mobility CSV", type=["csv"])

    if uploaded_file is None:
        st.info("Upload a retail mobility CSV file from the sidebar to populate the analytics dashboard.")
        return

    df = load_and_prepare_data(uploaded_file)

    if "retail_zone" in df.columns:
        zones = sorted(df["retail_zone"].dropna().unique().tolist())
        selected_zones = st.sidebar.multiselect("Select Retail Zones", zones, default=zones)
        df = df[df["retail_zone"].isin(selected_zones)]

    # Top-level KPI summary cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Footfall Events", f"{len(df):,}")

    avg_dwell = df["dwell_time_minutes"].mean() if "dwell_time_minutes" in df.columns else 0.0
    col2.metric("Avg Dwell Time (min)", f"{avg_dwell:.1f}")

    unique_zones = df["retail_zone"].nunique() if "retail_zone" in df.columns else 0
    col3.metric("Active Retail Zones", f"{unique_zones}")

    if "timestamp" in df.columns and not df["timestamp"].isna().all():
        peak_hour = int(df["timestamp"].dt.hour.mode()[0])
        col4.metric("Peak Activity Hour", f"{peak_hour:02d}:00")
    else:
        col4.metric("Peak Activity Hour", "N/A")

    st.divider()
    st.subheader("Validated Mobility Dataset Preview")
    st.dataframe(df.head(50), use_container_width=True)

if __name__ == "__main__":
    main()

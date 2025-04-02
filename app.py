import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Set Streamlit page configuration
st.set_page_config(page_title="Real-Time AQI Monitoring", layout="wide")

# Title
st.title("🌍 Real-Time Air Quality Monitoring Dashboard")

# Sidebar
st.sidebar.header("📅 Select Date Range")
date_range = st.sidebar.date_input("Choose a date range", [])

# Function to load AQI data
def load_data():
    try:
        file_path = "aqi_data.csv"  # Update this path based on your data file location
        df = pd.read_csv(file_path, parse_dates=["Time"])
        return df
    except FileNotFoundError:
        st.error("⚠️ AQI data file not found! Make sure the data is uploaded.")
        return None

# Load Data
st.write("### 📊 AQI Data Overview")
df = load_data()

if df is not None:
    if date_range:
        start_date, end_date = date_range
        df = df[(df["Time"] >= pd.to_datetime(start_date)) & (df["Time"] <= pd.to_datetime(end_date))]
        
        if df.empty:
            st.warning("⚠️ No data available for the selected date range!")
    
    # Plot AQI Levels
    fig = px.line(df, x="Time", y="NO Conc", title="Nitric Oxide (NO) Concentration Over Time")
    st.plotly_chart(fig, use_container_width=True)

    # Show Data Table
    st.dataframe(df)

else:
    st.warning("⚠️ No AQI data available! Upload a valid dataset.")

# Footer
st.write("---")
st.write("📌 **Note:** Data updates every minute based on sensor readings.")

import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Set Streamlit page configuration
st.set_page_config(page_title="Air Quality Dashboard", layout="wide")

# Title for the dashboard
st.title("🌍 Air Quality Monitoring Dashboard")

# Function to load data from Excel
@st.cache(allow_output_mutation=True)
def load_data():
    # The Excel file is located in the repository root
    data_file = "January 2025 data.xlsx"
    df = pd.read_excel(data_file, engine="openpyxl")
    # Convert the 'time' column to datetime
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    # Set 'time' as the DataFrame index for resampling
    df.set_index('time', inplace=True)
    df.sort_index(inplace=True)
    return df

# Load the data
df = load_data()

# Sidebar Filters
st.sidebar.header("🔍 Filter Data")

# Date range filter; default values set from the data's min and max dates
start_date = st.sidebar.date_input("Start Date", df.index.min().date())
end_date = st.sidebar.date_input("End Date", df.index.max().date())

# Aggregation selection
aggregation = st.sidebar.selectbox(
    "Aggregation Level", 
    options=["raw", "minutely", "hourly", "daily", "weekly", "monthly"],
    index=3  # Default: daily
)

# Pollutant selection; default: all three pollutants
pollutants = st.sidebar.multiselect(
    "Select Pollutants", 
    options=["NOX Conc", "NO Conc", "NO2 Conc"],
    default=["NOX Conc", "NO Conc", "NO2 Conc"]
)

# Validate the date selection
if start_date > end_date:
    st.sidebar.error("Start date must be before end date.")
else:
    # Filter data based on the selected date range
    filtered_df = df.loc[str(start_date):str(end_date)]
    
    if filtered_df.empty:
        st.error("⚠️ No data available for the selected date range.")
    else:
        # Apply aggregation if needed
        if aggregation == "raw":
            agg_df = filtered_df.copy()
        elif aggregation == "minutely":
            agg_df = filtered_df.resample('T').mean()
        elif aggregation == "hourly":
            agg_df = filtered_df.resample('H').mean()
        elif aggregation == "daily":
            agg_df = filtered_df.resample('D').mean()
        elif aggregation == "weekly":
            agg_df = filtered_df.resample('W').mean()
        elif aggregation == "monthly":
            agg_df = filtered_df.resample('M').mean()
        else:
            agg_df = filtered_df.copy()
        
        # Keep only the selected pollutant columns
        agg_df = agg_df[pollutants]
        
        # If aggregation yields an empty DataFrame, show a message
        if agg_df.empty:
            st.error("⚠️ No data available after applying aggregation. Please adjust your filters.")
        else:
            # Display the aggregated data table
            st.subheader("Aggregated Data")
            st.dataframe(agg_df.reset_index())

            # Prepare data for plotting using Plotly Express
            plot_df = agg_df.reset_index().melt(id_vars="time", value_vars=pollutants, 
                                                  var_name="Pollutant", value_name="Concentration")
            fig = px.line(plot_df, x="time", y="Concentration", color="Pollutant",
                          title="Air Quality Trends")
            st.plotly_chart(fig, use_container_width=True)

            # Compute and display statistics
            st.subheader("Statistics")
            stats = agg_df.agg(['min', 'max', 'mean'])
            st.dataframe(stats)

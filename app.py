import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load AQI data
@st.cache_data
def load_data():
    df = pd.read_excel("January 2025 data.xlsx", engine="openpyxl")
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    df.set_index('time', inplace=True)
    df.sort_index(inplace=True)
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filters")
aggregation = st.sidebar.selectbox("Select Aggregation Level", ["Raw", "Hourly", "Daily", "Weekly"], index=2)
start_date = st.sidebar.date_input("Start Date", df.index.min())
end_date = st.sidebar.date_input("End Date", df.index.max())

# Pollutant selection
pollutants = ["NOX Conc", "NO Conc", "NO2 Conc"]
selected_pollutants = st.sidebar.multiselect("Select Pollutants", pollutants, default=pollutants)

# Data Processing
filtered_df = df.loc[start_date:end_date]

if aggregation == "Hourly":
    filtered_df = filtered_df.resample("H").mean()
elif aggregation == "Weekly":
    filtered_df = filtered_df.resample("W").mean()
elif aggregation == "Daily":
    filtered_df = filtered_df.resample("D").mean()

# Plot Data
st.title("Real-Time Air Quality Monitoring Dashboard")

fig, ax = plt.subplots(figsize=(10, 5))
for pollutant in selected_pollutants:
    ax.plot(filtered_df.index, filtered_df[pollutant], label=pollutant)

ax.set_xlabel("Time")
ax.set_ylabel("Concentration")
ax.legend()
st.pyplot(fig)

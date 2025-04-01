from flask import Flask, render_template, jsonify, request
import pandas as pd

app = Flask(__name__)

# Load the Excel file (ensure the file is in the same folder or adjust the path)
df = pd.read_excel("January 2025 data.xlsx", engine="openpyxl")

# Convert the 'time' column to datetime
df['time'] = pd.to_datetime(df['time'], errors='coerce')

# Set 'time' as the index to enable resampling
df.set_index('time', inplace=True)
df.sort_index(inplace=True)  # Ensure data is sorted

# Only work with the three pollutants of interest.
# (Even if the DataFrame has other columns, we will only return these later.)
pollutant_cols = ["NOX Conc", "NO Conc", "NO2 Conc"]

@app.route("/")
def home():
    # Render our main dashboard page
    return render_template("index.html")

@app.route("/api/data/aggregated")
def get_aggregated_data():
    # Get query parameters for aggregation type and date filtering
    agg = request.args.get("agg", "daily")  # Options: raw, hourly, daily, weekly. Default: daily.
    start_date = request.args.get("start")
    end_date = request.args.get("end")
    
    # Filter the DataFrame (assuming your data is only January 2025, but users might choose a subset)
    data_filtered = df.copy()
    if start_date and end_date:
        try:
            data_filtered = data_filtered.loc[start_date:end_date]
        except Exception as e:
            return jsonify({"error": f"Invalid date range: {str(e)}"}), 400
    
    # Apply resampling only if aggregation is not "raw"
    if agg == "raw":
        aggregated = data_filtered
    elif agg == "hourly":
        aggregated = data_filtered.resample('H').mean()
    elif agg == "weekly":
        aggregated = data_filtered.resample('W').mean()
    else:  # Default daily
        aggregated = data_filtered.resample('D').mean()
    
    # Keep only the selected pollutant columns
    aggregated = aggregated[pollutant_cols]
    
    # Return JSON (reset the index so 'time' is a column)
    data_json = aggregated.reset_index().to_dict(orient="records")
    return jsonify(data_json)

#if __name__ == "__main__":
 #   app.run(host="0.0.0.0", debug=False, use_reloader=False)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use environment variable if available
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)


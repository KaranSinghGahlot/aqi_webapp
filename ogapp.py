from flask import Flask, render_template, jsonify, request
import pandas as pd

app = Flask(__name__)

# Load your Excel data
df = pd.read_excel("January 2025 data.xlsx", engine="openpyxl")
df['time'] = pd.to_datetime(df['time'], errors='coerce')
df.set_index('time', inplace=True)

@app.route("/")
def home():
    # Generate an HTML table (only first 5 rows)
    table_html = df.head().to_html()  
    return render_template("index.html", table=table_html)

@app.route("/api/data")
def get_data():
    # Return entire data as JSON, or you can filter if needed
    data_json = df.reset_index().to_dict(orient='records')
    return jsonify(data_json)

if __name__ == "__main__":
    app.run(debug=True)

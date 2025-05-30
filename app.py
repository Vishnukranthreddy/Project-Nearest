from flask import Flask, render_template, request
import math
import pandas as pd

app = Flask(__name__)

# Haversine formula to calculate the distance between two lat/lon points
def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    r = 6371  # Radius of Earth in kilometers
    return r * c  # Distance in kilometers

# Function to get the top N nearest points based on the city
def get_nearest_points(reference_lat, reference_lon, data, n):
    distances = []
    for _, row in data.iterrows():
        lat, lon = row['Lat'], row['Long']
        dist = haversine(reference_lat, reference_lon, lat, lon)
        distances.append((row['City'], dist))  # Store city and distance
    distances.sort(key=lambda x: x[1])  # Sort by the distance value
    return distances[:n]

# Load dataset from CSV (ensure it's in the same directory or adjust path)
csv_file = r'Indian Cities Database.csv'
data = pd.read_csv(csv_file)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        lat = float(request.form['latitude'])
        lon = float(request.form['longitude'])
        n = int(request.form['n'])
        nearest_points = get_nearest_points(lat, lon, data, n)
        return render_template('index.html', points=nearest_points, lat=lat, lon=lon)
    return render_template('index.html', points=None)

if __name__ == '__main__':
    app.run(debug=True)

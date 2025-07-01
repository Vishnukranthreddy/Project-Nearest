from flask import Flask, render_template, request
import math
import pandas as pd
import os

app = Flask(__name__, template_folder='../templates')

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
csv_file = os.path.join(os.path.dirname(__file__), '..', 'Indian Cities Database.csv')
data = pd.read_csv(csv_file)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        n = int(request.form['n'])
        
        # Get the number of coordinate pairs (default to 1 if not provided)
        coordinate_count = int(request.form.get('coordinate-count', 1))
        
        all_results = []
        
        # Process each coordinate pair
        for i in range(coordinate_count):
            lat_key = f'latitude-{i}'
            lon_key = f'longitude-{i}'
                
            # Skip if this pair doesn't exist in the form
            if lat_key not in request.form or lon_key not in request.form:
                continue
                
            try:
                lat = float(request.form[lat_key])
                lon = float(request.form[lon_key])
                nearest_points = get_nearest_points(lat, lon, data, n)
                
                all_results.append({
                    'lat': lat,
                    'lon': lon,
                    'points': nearest_points
                })
            except ValueError:
                # Skip invalid coordinates
                continue
        
        return render_template('index.html', all_results=all_results)
    
    return render_template('index.html')

# Export the app for Vercel
if __name__ != '__main__':
    # For Vercel deployment
    application = app
else:
    # For local development
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
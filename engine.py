import ee
import numpy as np
from functools import lru_cache

# --- 1. AUTHENTICATION ---
PROJECT_ID = 'global-sun-484918-f5'  # Your specific Project ID

try:
    ee.Initialize(project=PROJECT_ID)
except:
    ee.Authenticate()
    ee.Initialize(project=PROJECT_ID)

# --- 2. HELPER FUNCTION (The Single Point Logic) ---
def get_ndvi(lat, lon):
    """Fetches a single point's NDVI from GEE."""
    try:
        point = ee.Geometry.Point([lon, lat])
        
        # Fetch Sentinel-2 Data
        s2 = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")\
            .filterBounds(point)\
            .filterDate('2024-01-01', '2024-02-01')\
            .sort('CLOUDY_PIXEL_PERCENTAGE')\
            .first()
            
        # Calculate NDVI
        ndvi = s2.normalizedDifference(['B8', 'B4'])
        
        # Reduce to a specific number
        value = ndvi.reduceRegion(
            reducer=ee.Reducer.mean(), 
            geometry=point, 
            scale=30
        ).getInfo().get('nd', 0)
        
        return value if value is not None else 0
    except:
        return 0

# --- 3. MAIN FUNCTION (The Grid Generator) ---
@lru_cache(maxsize=100) # Caches the last 100 requests in RAM
def generate_heatmap_grid(center_lat: float, center_lon: float, grid_size: int = 3):
    """
    Generates a grid of points around the center.
    Returns GeoJSON format for the Frontend.
    """
    # Offset controls how far apart points are (0.005 is approx 500m)
    offset = 0.005 
    
    # Calculate the list of coordinates
    lats = np.linspace(center_lat - (grid_size*offset), center_lat + (grid_size*offset), grid_size)
    lons = np.linspace(center_lon - (grid_size*offset), center_lon + (grid_size*offset), grid_size)
    
    features = []
    
    print(f"🛰️ Scanning {grid_size}x{grid_size} grid for Lat:{center_lat}, Lon:{center_lon}...")

    for lat in lats:
        for lon in lons:
            # Get the real satellite data
            ndvi_val = get_ndvi(lat, lon)
            
            # Estimate Temp based on Veg (Inverse relationship)
            # This is a placeholder formula until Devaang gives the real LST script
            estimated_temp = 35.0 - (ndvi_val * 5) 

            # Build the GeoJSON Feature
            features.append({
                "type": "Feature",
                "geometry": { 
                    "type": "Point", 
                    "coordinates": [lon, lat] 
                },
                "properties": {
                    "ndvi": round(ndvi_val, 3),
                    "temp": round(estimated_temp, 1),
                    # Logic: If NDVI < 0.2 (Concrete), color is Red. Else Green.
                    "risk_color": [255, 0, 0] if ndvi_val < 0.2 else [0, 255, 0]
                }
            })
            
    return {
        "type": "FeatureCollection",
        "city_center": [center_lon, center_lat],
        "features": features
    }
    


def get_city_stats(lat: float, lon: float):
    """
    Calculates aggregate stats for the Dashboard Sidebar.
    """
    # 1. Reuse the grid generator to get raw data
    # We use a 5x5 grid for a quick statistical sample
    grid_data = generate_heatmap_grid(lat, lon, grid_size=5)
    
    features = grid_data['features']
    total_points = len(features)
    
    if total_points == 0:
        return {"avg_temp": 0, "green_cover": 0}

    # 2. Calculate Averages
    total_temp = sum([f['properties']['temp'] for f in features])
    total_ndvi = sum([f['properties']['ndvi'] for f in features])
    
    avg_temp = total_temp / total_points
    avg_ndvi = total_ndvi / total_points
    
    # 3. Return clean stats for the UI
    return {
        "city_center": {"lat": lat, "lon": lon},
        "stats": {
            "avg_temp_celsius": round(avg_temp, 1),
            "avg_ndvi_index": round(avg_ndvi, 3),
            # Logic: If NDVI > 0.3, we consider it "Green Cover"
            "green_cover_percent": f"{int(avg_ndvi * 100)}%",
            "risk_level": "High" if avg_temp > 35 else "Moderate"
        }
    }
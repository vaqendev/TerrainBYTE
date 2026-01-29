import ee
import numpy as np
from functools import lru_cache

# --- 1. AUTHENTICATION ---
PROJECT_ID = 'global-sun-484918-f5' 

try:
    ee.Initialize(project=PROJECT_ID)
except:
    ee.Authenticate()
    ee.Initialize(project=PROJECT_ID)

# --- 2. OPTIMIZED BATCH FUNCTION ---
@lru_cache(maxsize=100)
def generate_heatmap_grid(center_lat: float, center_lon: float, grid_size: int = 10):
    """
    OPTIMIZED: Fetches all data in ONE single request to Google.
    """
    offset = 0.005
    
    # 1. Generate all the coordinates in Python first
    lats = np.linspace(center_lat - (grid_size*offset), center_lat + (grid_size*offset), grid_size)
    lons = np.linspace(center_lon - (grid_size*offset), center_lon + (grid_size*offset), grid_size)
    
    # 2. Create a list of GEE Features (The "Box" of points)
    ee_points = []
    for lat in lats:
        for lon in lons:
            f = ee.Feature(ee.Geometry.Point([lon, lat]), {'lat': lat, 'lon': lon})
            ee_points.append(f)
            
    # Convert to a GEE Collection (The "Manifest")
    feature_collection = ee.FeatureCollection(ee_points)

    # 3. Fetch the Image ONCE (Not 100 times)
    image = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")\
        .filterBounds(ee.Geometry.Point([center_lon, center_lat]))\
        .filterDate('2024-01-01', '2024-02-01')\
        .sort('CLOUDY_PIXEL_PERCENTAGE')\
        .first()
        
    # Calculate NDVI once
    ndvi = image.normalizedDifference(['B8', 'B4']).rename('ndvi')
    
    # 4. The Magic Trick: reduceRegions (Ask for all points at once)
    # This is the ONLY network call in this entire function.
    sampled_data = ndvi.reduceRegions(
        collection=feature_collection,
        reducer=ee.Reducer.mean(),
        scale=30
    ).getInfo() # <--- Triggers the download

    # 5. Process the result locally (Instant)
    output_features = []
    
    for item in sampled_data['features']:
        # Extract the values Google sent back
        props = item['properties']
        ndvi_val = props.get('mean', 0) # 'mean' is the result of the reducer
        
        # Avoid None types
        if ndvi_val is None: ndvi_val = 0
            
        estimated_temp = 35.0 - (ndvi_val * 5)
        
        output_features.append({
            "type": "Feature",
            "geometry": { 
                "type": "Point", 
                "coordinates": [props['lon'], props['lat']] 
            },
            "properties": {
                "ndvi": round(ndvi_val, 3),
                "temp": round(estimated_temp, 1),
                "risk_color": [255, 0, 0] if ndvi_val < 0.2 else [0, 255, 0]
            }
        })

    return {
        "type": "FeatureCollection",
        "city_center": [center_lon, center_lat],
        "features": output_features
    }

# --- 3. STATS FUNCTION (Reuse the fast grid) ---
def get_city_stats(lat: float, lon: float):
    # This now runs super fast too
    grid_data = generate_heatmap_grid(lat, lon, grid_size=10)
    
    features = grid_data['features']
    total_points = len(features)
    
    if total_points == 0: return {"avg_temp": 0, "green_cover": 0}

    total_temp = sum([f['properties']['temp'] for f in features])
    total_ndvi = sum([f['properties']['ndvi'] for f in features])
    
    avg_temp = total_temp / total_points
    avg_ndvi = total_ndvi / total_points
    
    return {
        "city_center": {"lat": lat, "lon": lon},
        "stats": {
            "avg_temp_celsius": round(avg_temp, 1),
            "avg_ndvi_index": round(avg_ndvi, 3),
            "green_cover_percent": f"{int(avg_ndvi * 100)}%",
            "risk_score": "High" if avg_temp > 38 else "Moderate"
        }
    }
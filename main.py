from fastapi import FastAPI
from engine import generate_heatmap_grid, get_city_stats

app = FastAPI()

@app.get("/")
def home():
    return {"message": "SkyShadow Grid Engine Online 🛰️"}

@app.get("/analyze")
def analyze_area(lat: float, lon: float):
    """
    URL: /analyze?lat=28.61&lon=77.20
    scans a 3x3 grid around the coordinate.
    """
    try:
        # We start with a small 10x10 grid (100 points) for speed testing
        data = generate_heatmap_grid(lat, lon, grid_size=10)
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/stats")
def get_stats(lat: float, lon: float):
    """
    URL: /stats?lat=28.61&lon=77.20
    Returns summary for the sidebar charts.
    """
    try:
        data = get_city_stats(lat, lon)
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}
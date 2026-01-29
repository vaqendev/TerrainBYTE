from fastapi import FastAPI
from engine import generate_heatmap_grid

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
        # We start with a small 3x3 grid (9 points) for speed testing
        data = generate_heatmap_grid(lat, lon, grid_size=10)
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}
from fastapi import APIRouter

router = APIRouter()

CITIES = {
    "delhi": {"name": "Delhi", "center": [28.6139, 77.2090], "bbox": [28.4, 76.8, 28.8, 77.5]},
    "mumbai": {"name": "Mumbai", "center": [19.0760, 72.8777], "bbox": [18.8, 72.7, 19.3, 73.0]},
    "bangalore": {"name": "Bangalore", "center": [12.9716, 77.5946], "bbox": [12.8, 77.4, 13.1, 77.8]},
}


@router.get("/cities")
async def get_cities():
    return list(CITIES.values())

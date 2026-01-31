from fastapi import APIRouter, HTTPException

router = APIRouter()

DISTRICTS = {
    "delhi": [
        {"name": "Central Delhi", "avg_lst": 38.5,
            "avg_ndvi": 0.12, "zone": "red", "area_hectares": 120},
        {"name": "South Delhi", "avg_lst": 35.2, "avg_ndvi": 0.28,
            "zone": "amber", "area_hectares": 180},
        {"name": "North Delhi", "avg_lst": 36.8, "avg_ndvi": 0.18,
            "zone": "red", "area_hectares": 150},
        {"name": "East Delhi", "avg_lst": 34.1, "avg_ndvi": 0.32,
            "zone": "amber", "area_hectares": 140},
        {"name": "West Delhi", "avg_lst": 30.5, "avg_ndvi": 0.45,
            "zone": "green", "area_hectares": 160},
    ],
    "mumbai": [
        {"name": "South Mumbai", "avg_lst": 37.9,
            "avg_ndvi": 0.10, "zone": "red", "area_hectares": 95},
        {"name": "Central Mumbai", "avg_lst": 35.6,
            "avg_ndvi": 0.22, "zone": "amber", "area_hectares": 110},
        {"name": "North Mumbai", "avg_lst": 32.4, "avg_ndvi": 0.38,
            "zone": "green", "area_hectares": 200},
    ],
    "bangalore": [
        {"name": "Mahadevapura", "avg_lst": 33.2, "avg_ndvi": 0.40,
            "zone": "green", "area_hectares": 175},
        {"name": "Whitefield", "avg_lst": 35.8, "avg_ndvi": 0.25,
            "zone": "amber", "area_hectares": 130},
        {"name": "Jayanagar", "avg_lst": 31.5, "avg_ndvi": 0.48,
            "zone": "green", "area_hectares": 145},
    ],
}


@router.get("/districts/{city}")
async def get_districts(city: str):
    city = city.lower()
    if city not in DISTRICTS:
        raise HTTPException(status_code=404, detail=f"City '{city}' not found")
    return DISTRICTS[city]

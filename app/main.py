from .api import cities
from .api import cities, tiles, districts, simulation
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .ee_client import initialize_ee
app = FastAPI(title="SkyShadow API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

initialize_ee()

app.include_router(districts.router)
app.include_router(cities.router)

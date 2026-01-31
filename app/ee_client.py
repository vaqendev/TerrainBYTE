import ee
import json
import os
from app.config import settings


def initialize_ee():
    try:
        key_path = settings.EE_KEY_FILE

        with open(key_path, 'r') as f:
            key_data = json.load(f)

        credentials = ee.ServiceAccountCredentials(
            key_data['client_email'],
            key_file=key_path
        )

        ee.Initialize(credentials, project=settings.EE_PROJECT)

    except Exception as e:
        print(f"Failed to initialize Earth Engine: {e}")


def get_landsat(bbox, date_start, date_end):
    """Fetch Landsat 8/9 thermal band for a bounding box."""
    region = ee.Geometry.Rectangle(bbox)  # [west, south, east, north]

    landsat = (
        ee.ImageCollection("LANDSAT/LC08_L2SP_30")
        .filterBounds(region)
        .filterDate(date_start, date_end)
        .sort("CLOUD_COVER")
        .first()
    )

    # Band 10 = thermal infrared
    thermal = landsat.select("ST_B10")
    return thermal.clip(region)


def get_sentinel(bbox, date_start, date_end):
    """Fetch Sentinel-2 optical bands for NDVI calculation."""
    region = ee.Geometry.Rectangle(bbox)

    sentinel = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(region)
        .filterDate(date_start, date_end)
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 10))
        .sort("CLOUDY_PIXEL_PERCENTAGE")
        .first()
    )

    # Band 4 = Red, Band 8 = NIR
    optical = sentinel.select(["B4", "B8"])
    return optical.clip(region)


def export_image(image, description, bbox, scale=30):
    """Export an EE image to a GeoTIFF and return the download URL."""
    region = ee.Geometry.Rectangle(bbox)

    task = ee.Image.getDownloadURL(
        image,
        scale=scale,
        region=region,
        fileFormat="GeoTIFF",
    )
    return task

from fastapi import FastAPI
from pydantic import BaseModel
import time

app = FastAPI()

gps_data = {}   # { device_id: {lat, lon, timestamp} }
gps_history = {}  

# Model for POST body
class GPSModel(BaseModel):
    device_id: str
    latitude: float
    longitude: float

# Home
@app.get("/")
def home():
    return {"message": "GPS Tracking API Running!"}

# Send GPS location (POST)
@app.post("/location")
def update_location(data: GPSModel):
    gps_data[data.device_id] = {
        "latitude": data.latitude,
        "longitude": data.longitude,
        "timestamp": int(time.time())
    }

    # store history
    if data.device_id not in gps_history:
        gps_history[data.device_id] = []
    gps_history[data.device_id].append(gps_data[data.device_id])

    return {"status": "success", "data": gps_data[data.device_id]}

# Get latest location of a device
@app.get("/location/{device_id}")
def get_latest_location(device_id: str):
    if device_id not in gps_data:
        return {"error": "Device not found"}
    return gps_data[device_id]

# Get full history of a device
@app.get("/history/{device_id}")
def get_history(device_id: str):
    if device_id not in gps_history:
        return {"error": "No history found"}
    return gps_history[device_id]

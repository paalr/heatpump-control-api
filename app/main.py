from fastapi import FastAPI, HTTPException
from .tinytuya_handler import TinyTuyaHandler
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

device_id = os.getenv("DEVICE_ID")
ip_address = os.getenv("IP_ADDRESS")
local_key = os.getenv("LOCAL_KEY")
version = os.getenv("VERSION")
print(f"DEVICE_ID: {device_id}, IP_ADDRESS: {ip_address}, LOCAL_KEY: {local_key}, VERSION: {version}")
if not all([device_id, ip_address, local_key, version]):
    raise HTTPException(status_code=500, detail="Environment variables not set. Please run setup.")

handler = TinyTuyaHandler(device_id, ip_address, local_key, version)

@app.get("/status")
async def get_status():
    return handler.get_status()

@app.post("/turn_on")
async def turn_on():
    return handler.turn_on()

@app.post("/turn_off")
async def turn_off():
    return handler.turn_off()

@app.get("/temperature")
async def get_temperature():
    temperatures = handler.get_temperature()
    if temperatures['current_temperature'] is None or temperatures['water_tank_temperature'] is None:
        raise HTTPException(status_code=404, detail="Temperature data not available")
    return temperatures

@app.post("/set_water_temperature/{temperature}")
async def set_water_temperature(temperature: int):
    if temperature < -100000 or temperature > 100000:
        raise HTTPException(status_code=400, detail="Temperature out of range")
    return handler.set_water_temperature(temperature)

@app.post("/set_cold_temperature/{temperature}")
async def set_cold_temperature(temperature: int):
    if temperature < -100000 or temperature > 100000:
        raise HTTPException(status_code=400, detail="Temperature out of range")
    return handler.set_cold_temperature(temperature)

@app.post("/set_heat_temperature/{temperature}")
async def set_heat_temperature(temperature: int):
    if temperature < -100000 or temperature > 100000:
        raise HTTPException(status_code=400, detail="Temperature out of range")
    return handler.set_heat_temperature(temperature)

@app.post("/set_auto_temperature/{temperature}")
async def set_auto_temperature(temperature: int):
    if temperature < -100000 or temperature > 100000:
        raise HTTPException(status_code=400, detail="Temperature out of range")
    return handler.set_auto_temperature(temperature)

@app.get("/mode")
async def get_mode():
    mode = handler.get_mode()
    if mode is None:
        raise HTTPException(status_code=404, detail="Mode data not available")
    return {"mode": mode}

@app.post("/set_mode/{mode}")
async def set_mode(mode: str):
    try:
        return handler.set_mode(mode)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/error")
async def get_error():
    error_code = handler.get_error_code()
    if not error_code:
        return {"error": "No errors reported"}
    return {"error_code": error_code}
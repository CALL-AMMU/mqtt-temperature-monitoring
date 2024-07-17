from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import time

app = FastAPI()

temperature_data = []

class Temperature(BaseModel):
    temperature: float

@app.get("/temperature")
def get_temperature():
    if temperature_data:
        latest_data = temperature_data[-1]
        return latest_data
    else:
        return {"message": "No temperature data available"}

@app.post("/temperature")
def store_temperature(temperature: Temperature):
    temperature_data.append({"timestamp": time.time(), "temperature": temperature.temperature})
    return {"message": "Temperature data stored successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

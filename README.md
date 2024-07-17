# mqtt-temperature-monitoring
Consider an IoT device that reads data from the southbound sensors, and publishes them to the cloud.
# Temperature Sensor Alarm System

This repository implements a Python-based IoT system for monitoring room temperature and raising alarms when it exceeds a threshold for a continuous duration.

## Functionality

- The `publisher.py` script simulates (or reads from an actual sensor) temperature data every minute and publishes it to an MQTT broker.
- The `subscriber.py` script subscribes to the same MQTT topic, checks for temperature breaches, and raises alarms if the threshold is exceeded for a set duration (5 minutes in this example). It also stores the data locally.
- The `server.py` script (using Flask) provides an API endpoint to retrieve the latest temperature value.
  Implementation with Python Programs
This project consists of three Python programs:

1. Publisher Program (publisher.py)

Reads temperature data (simulated or from a real sensor) every 60 seconds.
Publishes the data to a specific topic on the MQTT broker.

2. Subscriber Program (subscriber.py)

Subscribes to the same topic used by the publisher.
Continuously receives temperature data.
Compares the data with a predefined threshold.
Raises an alarm (via email, SMS, or a visual/audio alert) if the threshold is exceeded for 5 consecutive data points (representing 5 minutes).
Saves the received data locally with timestamps for historical reference.

3. Server Program (server.py)

Uses a web framework like Flask to create a simple API.
Exposes an endpoint that returns the latest temperature value upon receiving an HTTP request.


## Prerequisites

- Python 3.x
- Paho MQTT client library (`pip install paho-mqtt`)
- Flask web framework (`pip install Flask`)

## Running the System

1. Install the required libraries: `pip install -r requirements.txt`
2. Start the MQTT broker (e.g., Mosquitto).
3. Run the publisher: `python publisher.py` in a separate terminal.
4. Run the subscriber: `python subscriber.py`
5. Optionally, run the server: `python server.py` (access API at http://localhost:5000/api/temperature)

## Customization

- Modify the `publisher.py` script to connect to your real sensor or adjust the simulated temperature range.
- Change the `threshold` and `duration` variables in `subscriber.py` to suit your needs.
- Replace the local data storage with a preferred database solution.
- Implement the alarm notification logic (e.g., email, SMS, light, sound) in `subscriber.py`.

## Notes

- This is a basic implementation and can be further extended for features like data visualization, historical data storage, etc.
- 
##Additional Information
A requirements.txt file specifies the necessary Python libraries (e.g., paho-mqtt, Flask).
The code includes comments and explanations for better understanding.
The README file (not provided here) should contain detailed instructions on setting up and running the system.
This is a basic implementation and can be extended for features like data visualization, historical data storage, etc.

1. Publisher Program (publisher.py):
   
import paho.mqtt.client as mqtt
import time
from random import randint  # Simulate sensor data (if no real sensor)

# MQTT Broker Configuration
broker_address = "localhost"
broker_port = 1883
topic = "hotel/room/temperature"

# Simulated Sensor Data Generation (if no real sensor)
def generate_temperature():
    return randint(18, 28)  # Adjust temperature range as needed

# MQTT Client Callback
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code", rc)

# Main Program
def main():
    client = mqtt.Client()
    client.on_connect = on_connect

    client.connect(broker_address, broker_port)

    while True:
        # Read temperature (replace with actual sensor reading)
        temperature = generate_temperature()  # Simulated data
        # temperature = read_from_sensor()  # Replace with your sensor code

        # Publish temperature data
        client.publish(topic, temperature)
        print(f"Published temperature: {temperature}°C")

        time.sleep(60)

if __name__ == "__main__":
    main()
    
2. Subscriber Program (subscriber.py):
   
import paho.mqtt.client as mqtt
import time
import datetime
import json

# MQTT Broker Configuration
broker_address = "localhost"
broker_port = 1883
topic = "hotel/room/temperature"

# Alarm Threshold and Duration
threshold = 25  # °C
duration = 5  # Minutes (5 data points)

# Data Storage (replace with preferred persistence method)
data_file = "temperature_data.json"

# Alarm Flag and Last Alarm Time
alarm_raised = False
last_alarm_time = None

# MQTT Client Callback
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(topic)
    else:
        print("Failed to connect, return code", rc)

def on_message(client, userdata, msg):
    global alarm_raised, last_alarm_time

    temperature = float(msg.payload.decode())
    timestamp = datetime.datetime.now()

    # Save data locally (replace with database if needed)
    with open(data_file, "a") as f:
        data = {"timestamp": timestamp.isoformat(), "temperature": temperature}
        json.dump(data, f, indent=4)

    # Check for threshold breach and continuous duration
    if temperature > threshold:
        if not alarm_raised or (timestamp - last_alarm_time).total_seconds() > duration * 60:
            alarm_raised = True
            last_alarm_time = timestamp
            print(f"ALARM! Temperature exceeded {threshold}°C for {duration} minutes.")
            # Implement alarm notification logic (e.g., send email, SMS, or trigger light/sound)

# Main Program
def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker_address, broker_port)
    client.loop_forever()

if __name__ == "__main__":
    main()
    
3. Server Program (server.py):

from flask import Flask, jsonify

# Data Storage (replace with preferred persistence method)
data_file = "temperature_data.json"

app = Flask(__name__)

@app.route("/api/temperature", methods=["GET"])
def get_latest_temperature():
    try:
        # Read last temperature data from file
        with open(data_file, "r") as f:
            data = json.load(f)
        return jsonify({"temperature": data["temperature"]})
    except FileNotFoundError:
        return jsonify({"error": "No temperature data found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Bind to all interfaces




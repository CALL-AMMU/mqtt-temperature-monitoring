import time
import json
import paho.mqtt.client as mqtt

# MQTT Broker (same as in publisher.py)
broker_address = "mqtt.example.com"
broker_port = 1883
topic = "hotel/temperature"
threshold = 25.0  # Example threshold temperature in Celsius
alarm_duration = 5 * 60  # 5 minutes in seconds

# Local storage for temperature data
temperature_data = []

def on_message(client, userdata, message):
    payload = json.loads(message.payload)
    temperature = payload["temperature"]
    temperature_data.append({"timestamp": time.time(), "temperature": temperature})
    print(f"Received: {temperature}")

    # Check if temperature exceeds threshold continuously for alarm_duration
    if len(temperature_data) >= 5:
        temperatures = [data["temperature"] for data in temperature_data[-5:]]
        if all(temp > threshold for temp in temperatures):
            print(f"ALARM: Temperature threshold ({threshold} C) exceeded for 5 minutes!")
            # Here you can implement logic to notify the manager
            # For now, print a message as an example
            temperature_data.clear()  # Clear data after raising alarm

def subscribe_temperature():
    client = mqtt.Client("Subscriber")
    client.connect(broker_address, broker_port)

    client.subscribe(topic)
    client.on_message = on_message

    client.loop_forever()


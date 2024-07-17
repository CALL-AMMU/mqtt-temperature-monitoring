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

import os
from confluent_kafka import SerializingProducer
import simplejson as json
import pyspark
from datetime import datetime
import random
import uuid
from datetime import timedelta

CDMX_COORDS = {
    "latitude": 19.365713,
    "longitude": -99.031171
}

SAN_JUAN_TABLAS_COORDS = {
    "latitude": 19.672527,
    "longitude": -99.422665
}

# Calculate movement increment
LATITUDE_INCREMENT = (
    SAN_JUAN_TABLAS_COORDS["latitude"] - CDMX_COORDS["latitude"]) / 100
LONGITUDE_INCREMENT = (
    SAN_JUAN_TABLAS_COORDS["longitude"] - CDMX_COORDS["longitude"]) / 100


# Environment configuration
KAFKA_BOOTSTRAP_SERVER = os.getenv('KAFKA_BOOTSTRAP_SERVER', 'localhost:9092')
VEHICLE_TOPIC = os.getenv('VEHICLE_TOPIC', 'vehicle_data')
GPS_TOPIC = os.getenv('GPS_TOPIC', 'gps_data')
TRAFFIC_TOPIC = os.getenv('TRAFFIC_TOPIC', 'traffic_data')
WEATHER_TOPIC = os.getenv('WEATHER_TOPIC', 'weather_data')
EMERGENCY_TOPIC = os.getenv('EMERGENCY_TOPIC', 'emergency_data')

start_time = datetime.now()
start_location = CDMX_COORDS.copy()


def get_next_time():
    global start_time
    # update frequency
    start_time += timedelta(seconds=random.randint(a=30, b=60))
    return start_time


def simulate_vehicle_movement():
    global start_location
    # move towards san juan tablas
    start_location['latitude'] += LATITUDE_INCREMENT
    start_location['longitude'] += LONGITUDE_INCREMENT

    # Add some randomness
    start_location['latitude'] += random.uniform(-0.0005, 0.0005)
    start_location['longitude'] += random.uniform(-0.0005, 0.0005)

    return start_location


def generate_vehicle_data(device_id):
    location = simulate_vehicle_movement()
    return {
        'id': uuid.uuid4(),
        'device_id': device_id,
        'timestamp': get_next_time().isoformat(),
        'location': (location['latitude'], location['longitude']),
        'speed': random.uniform(a=10, b=40),
        'direction': 'South-East',
        'model': 'BMW',
        'make': 'C500',
        'year': 2024,
        'fuelType':'Hybrid'
    }


def simulate_journey(producer, device_id):
    while True:
        vehicle_data = generate_vehicle_data(device_id=device_id)
        print(vehicle_data)
        break


if __name__ == "__main__":
    producer_config = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVER,
        'error_cb': lambda err: print(f'Kafka error >: {err}')
    }

    producer = SerializingProducer(producer_config)
    try:
        simulate_journey(producer, 'vehicle-data-123')
    except KeyboardInterrupt:
        print('Simulation ended by the user')
    except Exception as e:
        print(f'Error >: {e}')

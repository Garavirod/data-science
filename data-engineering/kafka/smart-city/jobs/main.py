import os
from confluent_kafka import SerializingProducer, Producer
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

random.seed(42)

start_time = datetime.now()
start_location = CDMX_COORDS.copy()


def generate_weather_data(device_id, timestamp, location):
    return {
        'id': uuid.uuid4(),
        'deviceId': device_id,
        'timestamp': timestamp,
        'temperature': random.uniform(-5, 26),
        'weatherCondition': random.choice(['Sunny', 'Cloudy', 'Rain', 'Snow']),
        'precipitation': random.uniform(a=0, b=25),
        'windSpeed': random.uniform(a=0, b=100),
        'humidity': random.uniform(a=0, b=100),
        'airQualityIndex': random.uniform(a=0, b=500)
    }


def generate_gps_data(device_id, timestamp, vehicle_type='Private'):
    return {
        'id': uuid.uuid4(),
        'deviceId': device_id,
        'timestamp': timestamp,
        'speed': random.uniform(a=0, b=40),  # km/h
        'direction': 'South-East',
        'vehicleType': vehicle_type
    }


def generate_traffic_camera_data(device_id, timestamp, location, camera_id):
    return {
        'id': uuid.uuid4(),
        'deviceId': device_id,
        'cameraId': camera_id,
        'timestamp': timestamp,
        'location': location,
        'snapshot': 'Base64EncodedString'
    }


def generate_emergency_incident_data(device_id, timestamp, location):
    return {
        'id': uuid.uuid4(),
        'deviceId': device_id,
        'timestamp': timestamp,
        'location': location,
        'incidentId': uuid.uuid4(),
        'type': random.choice(['Accident', 'Fire', 'Medical', 'Police', 'None']),
        'status': random.choice(['Active', 'Resolve']),
        'description': 'Description of the incident'
    }


def verify_data_serialized(obj):
    if isinstance(obj, uuid.UUID):
        return str(obj)
    raise TypeError(
        f'Object of type {obj.__class__.__name__} is not serializable')


def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed {err}')
    else:
        print(f'Message delivered to {msg.topic()}[{msg.partition()}]')


def produce_data_to_kafka(producer: Producer, topic, data):
    producer.produce(
        topic,
        key=str(data['id']),
        value=json.dumps(data, default=verify_data_serialized).encode('utf-8'),
        on_delivery=delivery_report
    )


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
        'fuelType': 'Hybrid'
    }


def simulate_journey(producer, device_id):
    while True:
        vehicle_data = generate_vehicle_data(device_id=device_id)
        gps_data = generate_gps_data(
            device_id=device_id, timestamp=vehicle_data['timestamp'])
        traffic_camera_data = generate_traffic_camera_data(
            device_id=device_id, timestamp=vehicle_data['timestamp'], camera_id='Nikon-Camera-123', location=vehicle_data['location'])
        weather_data = generate_weather_data(
            device_id, vehicle_data['timestamp'], vehicle_data['location'])
        emergency_incident_data = generate_emergency_incident_data(
            device_id=device_id, timestamp=vehicle_data['timestamp'], location=vehicle_data['location'])

        # Send data to kafka topics

        produce_data_to_kafka(
            producer=producer, topic=VEHICLE_TOPIC, data=vehicle_data)
        produce_data_to_kafka(
            producer=producer, topic=GPS_TOPIC, data=gps_data)
        produce_data_to_kafka(
            producer=producer, topic=TRAFFIC_TOPIC, data=traffic_camera_data)
        produce_data_to_kafka(
            producer=producer, topic=WEATHER_TOPIC, data=weather_data)
        produce_data_to_kafka(
            producer=producer, topic=EMERGENCY_TOPIC, data=emergency_incident_data)

        print(vehicle_data)
        print(gps_data)
        print(traffic_camera_data)
        print(weather_data)
        print(emergency_incident_data)
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

import os
from confluent_kafka import SerializingProducer
import simplejson as json
import pyspark
from datetime import datetime
CDMX_COORDS = {
    "latitude":19.365713, 
    "longitude":-99.031171
}

SAN_JUAN_TABLAS_COORDS = {
    "latitude":19.672527, 
    "longitude":-99.422665
}

# Calculate movement increment
LATITUDE_INCREMENT = (SAN_JUAN_TABLAS_COORDS["latitude"] - CDMX_COORDS["latitude"]) / 100
LONGITUDE_INCREMENT = (SAN_JUAN_TABLAS_COORDS["longitude"] - CDMX_COORDS["longitude"]) / 100


# Environment configuration
KAFKA_BOOTSTRAP_SERVER = os.getenv('KAFKA_BOOTSTRAP_SERVER','localhost:9092')
VEHICLE_TOPIC= os.getenv('VEHICLE_TOPIC','vehicle_data')
GPS_TOPIC= os.getenv('GPS_TOPIC','gps_data')
TRAFFIC_TOPIC= os.getenv('TRAFFIC_TOPIC','traffic_data')
WEATHER_TOPIC= os.getenv('WEATHER_TOPIC','weather_data')
EMERGENCY_TOPIC= os.getenv('EMERGENCY_TOPIC','emergency_data')

start_time = datetime.now()
start_location = CDMX_COORDS.copy()

if __name__ == "__main__":
    producer_config = {
        'bootstrap.servers':KAFKA_BOOTSTRAP_SERVER,
        'error_cb': lambda err: print(f'Kafka error >: {err}')
    }

import configparser
import os

parser = configparser.ConfigParser()
parser.read(os.path.join(os.path.dirname(__file__), '../config/config.conf'))


# ENVIRONMENT
ENV_MODE = parser.get('environment','env')


def select_topic_by_env():
    if ENV_MODE == 'dev':
        return parser.get('kafka_topics','bookpurchasing_kafka_topic_dev')
    else:
        return parser.get('kafka_topics','bookpurchasing_kafka_topic_prod')
    
def select_broker_server_by_env():
    if ENV_MODE == 'dev':
        return parser.get('kafka_server','server_kafka_broker_1_dev')
    else:
        return parser.get('kafka_server','server_kafka_broker_1_prod')


# API'S CONSUMING KEYS
BANXICO_TOKEN = parser.get('api_keys','banxico_api_token')

# KAFKA TOPICS
BOOKPURCHASING_KAFKA_TOPIC = select_topic_by_env()

# KAFKA BROKERS 
BROKER_SERVER_1 = select_broker_server_by_env()
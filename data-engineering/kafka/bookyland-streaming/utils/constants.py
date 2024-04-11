import configparser
import os

parser = configparser.ConfigParser()
parser.read(os.path.join(os.path.dirname(__file__), '../config/config.conf'))

# API'S CONSUMING KEYS
BANXICO_TOKEN = parser.get('api_keys','banxico_api_token')
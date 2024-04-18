import json
import os
def load_data_from_file(file_name:str):
    path_file = os.path.join(os.path.dirname(__file__), f'../../data/{file_name}.json')
    with open(path_file,'r', encoding='utf-8') as f:
        users = json.load(f)
    return users

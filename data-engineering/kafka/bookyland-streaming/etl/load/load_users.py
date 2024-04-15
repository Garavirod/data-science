import json
import os
def load_users():
    path_file = os.path.join(os.path.dirname(__file__), '../../data/users.json')
    with open(path_file,'r', encoding='utf-8') as f:
        users = json.load(f)
    return users

from utils.utils import save_as_json_file
from etl.extract.data_extraction import fetch_random_user
import json

def generate_users(num_users):
    """
        Creates the file users.json
    """
    users = {}
    for _ in range(num_users):
        user = fetch_random_user()
        if not user['user_id'] in user:
            users[user['user_id']] = user
    users_list = list(users.values())
    save_as_json_file(
        file_name='users',
        data=users_list
    )
    
if __name__ == '__main__':
    generate_users(num_users=100)
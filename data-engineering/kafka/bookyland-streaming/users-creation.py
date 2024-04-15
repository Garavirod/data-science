import json
from etl.extract.data_extraction import fetch_random_user
import click
from tqdm import tqdm
import json


@click.command()
@click.option('--count', default=30, help='Num of users to create')
def generate_users(count):
    users = {}
    pbar = tqdm(total=100)
    for _ in range(count):
        user = fetch_random_user()
        if not user['user_id'] in user:
            users[user['user_id']] = user
            pbar.update(10)
    pbar.close()
    users_list = list(users.values())

    with open('data/users.json', 'w', encoding='utf-8') as f:
        json.dump(users_list, f, ensure_ascii=False, indent=3)


if __name__ == '__main__':
    generate_users()
from datalake.users_creation import generate_users
from datalake.purchases_creation import simulate_book_purchases

def generate_fake_data_lake():
    generate_users()
    simulate_book_purchases()
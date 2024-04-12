from simulator import simulate_book_purchases
from etl.load.load_users import load_users_to_system


if __name__ == '__main__':
    users = load_users_to_system(limit=10)
    purchases = simulate_book_purchases(num_simulations=10, users_list=users)

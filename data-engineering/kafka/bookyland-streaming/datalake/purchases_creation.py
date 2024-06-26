from utils.utils import set_random_date, save_as_json_file
import random
from etl.extract.data_extraction import fetch_random_book
from etl.transform.transformations import set_exchange_usd_to_mxn
import uuid
import logging
from etl.load.load_data import load_data_from_file
import time


def simulate_book_purchases():
    """  
    Simulates the fake user books purchasing like if the users did from its device (IOS, Android or Web) app.
    Data purchase is sent into a kafka topic by a producer.
    """
    end_time = time.time() + 60
    users = load_data_from_file(file_name='users')
    purchases = []
    while True:

        if time.time() > end_time: # run for 1 minute
            break

        try:
            user = random.choice(users)
            book_id, book_title, book_price, book_editorial, book_genre, book_author, book_isbn, book_page_length, book_language, book_mode = fetch_random_book()
            purchase_source = random.choice(['IOS', 'Android', 'Website'])
            purchase_date = set_random_date(year_start=2019, year_end=2024)
            payment_type = random.choice(
                ['DEBIT', 'CREDIT', 'BOOK_CARD_CREDIT'])
            payment_status = random.choice(
                ['FAILED', 'SUCCESS', 'FRAUD', 'PENDING', 'NO_FUNDS', 'SUCCESS', 'SUCCESS', 'SUCCESS'])
            purchase_id = str(uuid.uuid4())
            money_currency = random.choice(['USD', 'MXN'])
            purchase_revenue = book_price

            if money_currency == 'USD':
                purchase_revenue = set_exchange_usd_to_mxn(book_price)

            purchase = {
                'purchase_id': purchase_id,
                'user_id': user['user_id'],
                'user_name': user['user_name'],
                'user_lastname': user['user_lastname'],
                'book_id': book_id,
                'book_title': book_title,
                'book_price': book_price,
                'user_country': user['user_country'],
                'book_editorial': book_editorial,
                'user_city': user['user_city'],
                'user_age': user['user_age'],
                'purchase_source': purchase_source,
                'book_genre': book_genre,
                'book_author': book_author,
                'book_isbn': book_isbn,
                'purchase_date': purchase_date,
                'payment_type': payment_type,
                'payment_status': payment_status,
                'purchase_revenue': purchase_revenue,
                'money_currency': money_currency,
                'book_page_length': book_page_length,
                'book_language': book_language,
                'book_mode': book_mode,
            }
            purchases.append(purchase)
        except Exception as e:
            logging.error(f'An error ocurred >: {e}')
            continue

    save_as_json_file(
        file_name='purchases',
        data=purchases
    )

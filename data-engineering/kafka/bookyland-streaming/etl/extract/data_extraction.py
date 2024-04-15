
import requests
import time
from utils.utils import set_random_date
import random
import datetime
from utils.constants import BANXICO_TOKEN
def fetch_random_user():
    """ 
    Fetch a fake data user from API Random User 
    """

    api_base = 'https://randomuser.me/api/'
    time.sleep(1)  # Simulate delay
    response = requests.get(api_base)
    data = response.json()['results'][0]
    user_id = data['login']['uuid']
    user_name = data['name']['first']
    user_lastname = data['name']['last']
    user_country = data['location']['country']
    user_age = data['dob']['age']
    user_city = data['location']['city']
    user_registration_date = set_random_date(year_start=2019, year_end=2025)
    return {
        'user_id': user_id,
        'user_name': user_name,
        'user_lastname': user_lastname,
        'user_country': user_country,
        'user_age': user_age,
        'user_city': user_city,
        'user_registration_date': user_registration_date
    }


def fetch_random_book():
    """ 
    Fetch a random book from Google books API  
    """
    time.sleep(1)  # Simulate delay
    categories = ['Horror', 'comedy', 'Mystery', 'Films', 'Healthy', 'Sports', 'Business', 'History',
                  'Fiction', 'Science', 'Maths', 'Science Fiction', 'Novels', 'Erotic', 'Drama', 'Comic']
    book_modes = ['PDF', 'EBOOK', 'EPUB', 'PHYSICAL', 'AUDIO_BOOK']
    category_query = random.choice(categories)
    url_api_base = f'https://www.googleapis.com/books/v1/volumes?q={category_query}'
    response = requests.get(url_api_base)
    data = response.json()
    book = random.choice(data['items'])
    book_id = book['id']
    book_title = book['volumeInfo']['title']
    book_price = random.uniform(5, 50)
    book_editorial = book['volumeInfo'].get('publisher', 'Unknown')
    book_page_length = book['volumeInfo'].get('pageCount', 'Unknown')
    book_genre = book['volumeInfo'].get('categories', 'Unknown')[0]
    book_language = book['volumeInfo'].get('language', 'Unknown')
    book_mode = random.choice(book_modes)
    book_author = book['volumeInfo'].get('authors', 'Unknown')[0]
    book_isbn = book['volumeInfo'].get(
        'industryIdentifiers', [{'identifier': 'Unknown'}])[0]['identifier']
    return book_id, book_title, book_price, book_editorial, book_genre, book_author, book_isbn, book_page_length, book_language, book_mode,


def fetch_exchange_rate():
    """
    Fetch the current USD value in MXN from Banxico API
    """
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    start_date, end_date = today_date, today_date
    token = BANXICO_TOKEN
    id_serie = 'SF43718'
    api_url = f'https://www.banxico.org.mx/SieAPIRest/service/v1/series/{id_serie}/datos/{start_date}/{end_date}'
    response = requests.get(api_url, headers={
        'Bmx-Token': token
    })
    data = response.json()
    exchange = data['bmx']['series'][0].get('datos','Unknown')[0]['dato']
    return exchange

from etl.extract.data_extraction import fetch_exchange_rate

def set_exchange_usd_to_mxn(book_price):
    """ 
    Convert the USD books_price to MXN
    """
    exchange_rate = fetch_exchange_rate()
    if exchange_rate != 'N/E':
        dollar_price = float(exchange_rate)
        return round(float(book_price) * dollar_price, 2)
    return exchange_rate
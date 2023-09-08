
import pandas as pd
from twilio.rest import Client
from datetime import datetime
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


def get_date():

    input_date = datetime.now()
    input_date = input_date.strftime("%Y-%m-%d")
    return input_date


def build_template_message_body(date, country, forecast_data):
    return f"Morning! \n\n\n The weather forecast today {date} in {country} is : \n\n\n {str(forecast_data)}"


def request_weather_api(api_key, query):

    url_clima = 'http://api.weatherapi.com/v1/forecast.json?key=' + \
        api_key+'&q='+query+'&days=1&aqi=no&alerts=no'

    try:
        response = requests.get(url_clima).json()
    except ConnectionError as e:
        print(f'Error on api request >: ', e)
        pass
    except Timeout as e:
        print(f'Error on api request >: ', e)
        pass
    except TooManyRedirects as e:
        print(f'Error on api request >: ', e)
        pass
    except Exception as e:
        print(f'Error on api request >: ', e)

    return response


def get_forecast(api_response, iterator):

    date = api_response['forecast']['forecastday'][0]['hour'][iterator]['time'].split()[
        0]
    hour = int(api_response['forecast']['forecastday'][0]
               ['hour'][iterator]['time'].split()[1].split(':')[0])
    condition = api_response['forecast']['forecastday'][0]['hour'][iterator]['condition']['text']
    temperature = api_response['forecast']['forecastday'][0]['hour'][iterator]['temp_c']
    will_rain = api_response['forecast']['forecastday'][0]['hour'][iterator]['will_it_rain']
    chance_rain = api_response['forecast']['forecastday'][0]['hour'][iterator]['chance_of_rain']

    return date, hour, condition, temperature, will_rain, chance_rain


def create_dataframe(data):

    cols = ['Date', 'Hour', 'Condition',
            'Temperature', 'Rain', 'Probability of rain']
    df = pd.DataFrame(data, columns=cols)

    """ 
    Filter records that only contain information where it is mentioned that it will be a rainy day 
    within a schedule of 6 to 22
    """
    df_rainy_only = df[
        (df['Rain'] == 1) &
        (df['Hour'] > 6) &
        (df['Hour'] < 22)
    ]

    df_rainy_only = df_rainy_only[['Hour', 'Condition']]
    df_rainy_only.set_index('Hour', inplace=True)
    return df_rainy_only


def send_message(twilio_account_sid, twilio_token, body_template, recipient_phone, sender_pohne):
    # Prepare twilio client
    client = Client(twilio_account_sid, twilio_token)
    # Sending message
    try:
        message = client.messages.create(
            body=body_template,
            from_=sender_pohne,
            to=recipient_phone
        )
        return message.sid
    except Exception as e:
        print(f'Error on sending message >: ', e)
        return None

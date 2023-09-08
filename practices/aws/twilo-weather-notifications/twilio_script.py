"""
************************************************************************
* Author = @Garavirod Rodrigo Garcia Avila                             *
* Date = '07/09/2023'                                                  *
* Description = Send twilio message with python 3                      *
************************************************************************
"""

import twilio_config
from tqdm import tqdm
import utils


def get_daily_forecast():
    # Prepare weather APi request
    country = 'Mexico'
    api_key = twilio_config.API_KEY_WAPI
    input_date = utils.get_date()
    response = utils.request_weather_api(api_key, country)

    # Build forecast dataframe
    data = []
    for i in tqdm(range(24), colour='green'):
        forecast_data = utils.get_forecast(response, i)
        data.append(forecast_data)

    df_rain_forecast = utils.create_dataframe(data)

    # Send Message
    template = utils.build_template_message_body(
        input_date, country, df_rain_forecast)
    message_id = utils.send_message(
        twilio_config.TWILIO_ACCOUNT_SID,
        twilio_config.TWILIO_AUTH_TOKEN,
        template,
        twilio_config.PHONE_NUMBER_RECIPIENT,
        twilio_config.PHONE_NUMBER
    )


if __name__ == '__main__':
    get_daily_forecast()

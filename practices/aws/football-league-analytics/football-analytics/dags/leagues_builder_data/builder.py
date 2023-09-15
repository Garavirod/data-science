
import pandas as pd
import time
import random
from datetime import datetime


def get_data(url, league):
    # web scripting, simlutae human interaction in random time
    random_time = [1, 3, 2]
    time.sleep(random.choice(random_time))
    df = pd.read_html(url)
    # Build dataframe
    df = pd.concat([df[0], df[1]], ignore_index=True, axis=1)
    df = df.rename(columns={
        0: 'team',
        1: 'played',
        2: 'won',
        3: 'tied',
        4: 'lost',
        5: 'goals_favor',
        6: 'goals_against',
        7: 'diff',
        8: 'scores'})

    df['team'] = df['team'].apply(
        lambda x: x[5:] if x[:2].isnumeric() == True else x[4:])
    df['league'] = league

    run_date = datetime.now()
    run_date = run_date.strftime("%Y-%m-%d")
    df['created_at'] = run_date

    return df


def data_processing(df):

    df_spain = get_data(df['URL'][0], df['LEAGUE'][0])
    df_premier = get_data(df['URL'][1], df['LEAGUE'][1])
    df_italy = get_data(df['URL'][2], df['LEAGUE'][2])
    df_french = get_data(df['URL'][4], df['LEAGUE'][4])
    df_portugal = get_data(df['URL'][5], df['LEAGUE'][5])
    df_holland = get_data(df['URL'][6], df['LEAGUE'][6])

    df_final = pd.concat([df_spain, df_premier, df_italy,
                         df_french, df_portugal, df_holland], ignore_index=False)

    return df_final

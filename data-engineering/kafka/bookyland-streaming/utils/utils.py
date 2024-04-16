import datetime
import random
import json

def set_random_date(year_start: int, year_end: int):
    """
        Generates a random date between the range of to dates 
        that start by year_start and year_End "
    """
    start = datetime.datetime(year_start, 1, 1)
    end = datetime.datetime(year_end, 1, 1)

    return (start + datetime.timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())))).isoformat()


def save_as_json_file(file_name:str, data):
    try:
        with open(f'../data/{file_name}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=3)
    except Exception as e:
        raise('Error on saving json file :> {e}')
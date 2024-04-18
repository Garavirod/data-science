
from etl.extract.data_extraction import fetch_candidates_for_discount, get_criteria_discount
from utils.utils import save_as_json_file
def extract_purchases_from_data_lake():
    pass

def call_api_for_candidates():
    result = fetch_candidates_for_discount()
    save_as_json_file(
        file_name='candiates_api_result',
        data=result
    )

def call_api_for_getting_discount():
    result = get_criteria_discount()
    save_as_json_file(
        file_name='criteria',
        data=result
    )
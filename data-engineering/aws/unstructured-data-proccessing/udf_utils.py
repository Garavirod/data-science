import re
from datetime import datetime


def extract_file_name(file_content: str):
    file_content = file_content.strip()  # trim the line
    position = file_content.split('\n')[0]
    return position


def extract_position(file_content: str):
    file_content = file_content.strip()  # trim the line
    position = file_content.split('\n')[0]
    return position


def extract_class_code(file_content: str):
    try:
        class_code_match = re.search(r'(Class code:)\s+(\d+)', file_content)
        class_code = class_code_match.group(2) if class_code_match else None
        return class_code
    except Exception as e:
        raise ValueError(f'Error extracting class node: {e}')


def extract_start_date(file_content: str):
    try:
        open_date_match = re.search(
            r'(Open [Dd]ate:)\s+(\d\d-\d\d-\d\d)', file_content)
        open_date = datetime.strptime(open_date_match.group(
            2), '%m-%d-%y') if open_date_match else None
        return open_date
    except Exception as e:
        raise ValueError(f'Error extracting start date: {e}')


def extract_end_date(file_content: str):
    end_date_match = re.search(
        r'(JANUARY | FEBRUARY | MARCH | APRIL | MAY | JUNE | JULY | AUGUST | SEPTEMBER | OCTOBER | NOVEMBER | DECEMBER)\s(\d{1,2},\s\d{4})',
        file_content
    )

    end_date = end_date_match.group() if end_date_match else None
    end_date = datetime.strptime(end_date_match.group(
            2), '%B %d, %Y') if end_date_match else None
    
    return end_date

def extract_salary(file_content: str):
    try:
        salary_pattern = r'(\$[0-9,]+ to \$[0-9,]+)(?:;|$)'
        salary_matches = re.findall(salary_pattern, file_content)

        if len(salary_matches)  > 0:
            salary_start = float(salary_matches[0].replace(',','').replace('$','').split('to')[0])
            salary_end = float(salary_matches[-1].replace(',','').replace('$','').split('to')[0])
        else:
            salary_start, salary_end = None, None
        
        return salary_start, salary_end
    except Exception as e:
        raise ValueError(f'Error extracting salary: {str(e)}')


def extract_requirements(file_Content: str):
    pass


def extract_notes(file_content: str):
    pass


def extract_duties(file_content: str):
    pass


def extract_selection(file_content: str):
    pass


def extract_experience_length(file_length: int):
    pass


def extract_eduction_length(file_content: str):
    pass


def extract_application_location(file_content: str):
    pass

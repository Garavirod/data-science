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
        class_code_match = re.search(r'(Class [Cc]ode:)\s+(\d+)', file_content)
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

        if len(salary_matches) > 0:
            salary_start = float(salary_matches[0].replace(
                ',', '').replace('$', '').split('to')[0])
            if len(salary_matches) == 1:
                salary_end = float(
                    salary_matches[-1].replace(',', '').replace('$', '').split('to')[1])
            else:
                salary_end = float(
                    salary_matches[-1].replace(',', '').replace('$', '').split('to')[0])
        else:
            salary_start, salary_end = None, None

        return salary_start, salary_end
    except Exception as e:
        raise ValueError(f'Error extracting salary: {str(e)}')


def extract_requirements(file_Content: str):
    try:
        requirements_match = re.search(
            r'(REQUIREMENT?\s?MINIMUM QUALIFICATIONS?)(.*)(PROCESS NOTES?)',
            file_Content,
            re.DOTALL
        )
        req = requirements_match.group(
            2).strip() if requirements_match else None
        return req
    except Exception as e:
        raise ValueError(f'Error extracting requirements: {str(e)}')


def extract_notes(file_content: str):
    try:
        notes_match = re.search(
            r'(NOTES?):(.*?)(?=DUTIES)',
            file_content,
            re.DOTALL | re.IGNORECASE
        )
        notes = notes_match.group(2).strip() if notes_match else None
        return notes
    except Exception as e:
        raise ValueError(f'Error extracting notes: {str(e)}')


def extract_duties(file_content: str):
    try:
        duties_match = re.search(
            r'(DUTIES?):(.*?)(REQ[A-Z])',
            file_content,
            re.DOTALL
        )
        duties = duties_match.group(2).strip() if duties_match else None
        return duties
    except Exception as e:
        raise ValueError(f'Error extracting duties: {str(e)}')


def extract_selection(file_content: str):
    try:
        selection_match = re.findall(
            r'([A-Z][a-z]+)(\s\.\s)+',
            file_content,
        )
        selection = [z[0]
                     for z in selection_match] if selection_match else None
        return selection
    except Exception as e:
        raise ValueError(f'Error extracting duties: {str(e)}')


def extract_experience_length(file_content: int):
    try:
        experience_match = re.search(
            r'(One|Two|Three|Four|Five|Six|Seven|Eight|Nine|TenOne|Two|Three|Four|Five)\s(years?)\s(of\sfull(-|\s)time)',
            file_content,
        )
        experience_length = experience_match.group(
            1).strip() if experience_match else None
        return experience_length
    except Exception as e:
        raise ValueError(f'Error extracting experience length: {str(e)}')


def extract_eduction_length(file_content: str):
    try:
        education_match = re.search(
            r'(One|Two|Three|Four|Five|Six|Seven|Eight|Nine|TenOne|Two|Three|Four|Five)(\s|-)(years?)\s(collage|university)',
            file_content,
        )
        education_length = education_match.group(
            1).strip() if education_match else None
        return education_length
    except Exception as e:
        raise ValueError(f'Error extracting education length: {str(e)}')


def extract_application_location(file_content: str):
    try:
        application_loc_match = re.search(
            r'(Applications? will only be accepted on-?line)',
            file_content,
            re.IGNORECASE
        )
        application_location = 'Online' if application_loc_match else 'Mail or In Person'
        return application_location
    except Exception as e:
        raise ValueError(f'Error extracting application location: {str(e)}')

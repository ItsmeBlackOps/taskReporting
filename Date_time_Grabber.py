import re
from dateutil import parser
from datetime import datetime, timedelta



def extract_date(input_string):
    # Define date patterns
    date_pattern_1 = re.compile(r'\b\d{1,2}[-/]\d{1,2}(?:[-/]\d{2,4})?\b')
    date_pattern_2 = re.compile(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s*(?:\d{0,4})?\b')
    date_pattern_3 = re.compile(r'\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(?:\d{2,4})?\b')
    date_pattern_4 = re.compile(r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s*(?:\d{0,4})?\b')
    date_pattern_5 = re.compile(r'\b\d{1,2}(?:th|nd|st)?\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s*(?:\d{0,4})?\b')

    # Find all matches in the input string
    date_matches = date_pattern_1.findall(input_string) + \
    date_pattern_2.findall(input_string) + \
    date_pattern_3.findall(input_string) + \
    date_pattern_4.findall(input_string) + \
    date_pattern_5.findall(input_string)
    # Check for "today" or "tomorrow" in the string
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    if 'today' in input_string.lower():
        date_matches.append(today.strftime('%m-%d-%Y'))
    elif 'tomorrow' in input_string.lower():
        date_matches.append(tomorrow.strftime('%m-%d-%Y'))

    # Parse each matched date using dateutil.parser
    parsed_dates = []

    for date_str in date_matches:
        try:
            parsed_date = parser.parse(date_str, fuzzy=True)
            parsed_dates.append(parsed_date)
        except ValueError:
            pass
    parsed_date = parsed_dates[-1].strftime('%Y-%m-%d')
    
    
    return parsed_date if parsed_dates else None

def add_minutes_default00_format(input_string):
    # Define a regex pattern for matching hours followed by 'am' or 'pm'
    pattern = re.compile(r'(\d{1,2})([APMapm]{2})')
    
    if ":" not in input_string:
        # Replace the matched pattern with 'n:00am' or 'n:00pm'
        replaced_string = pattern.sub(lambda match: f"{match.group(1)}:00{match.group(2).lower()}", input_string)
        return replaced_string
    else:
        return input_string

def nospaceAMPM(input_string):
    input_string = input_string.lower() 
    if ' pm' in input_string:
        input_string = input_string.replace(' pm','pm')
        
    if ' am' in input_string:
        input_string = input_string.replace(' am','am')
    return input_string

def reduce_spaces(input_string):
    # Replace 2 or more spaces with a single space
    reduced_string = re.sub(r'\s{2,}', ' ', input_string)
    return reduced_string

def convert_to_military_time(time_str):
    try:
        # Parse the input time string
        parsed_time = datetime.strptime(time_str, "%I:%M%p")

        # Convert to military time format
        military_time = parsed_time.strftime("%H:%M")

        return military_time
    except ValueError:
        return None

def daylight_EST(input_string,time_string):
    if 'EST' in input_string.upper() or \
       'EDT' in input_string.upper():
        # Time is already in EST
        est_offset = 0
    elif 'CST' in input_string.upper() or \
         'CDT' in input_string.upper(): 
        # Convert from CST to EST
        est_offset = 1
    elif 'MST' in input_string.upper() or \
         'MDT' in input_string.upper():
        # Convert from MST to EST
        est_offset = 2
    elif 'PST' in input_string.upper() or \
         'PDT' in input_string.upper():
        # Convert from PST to EST
        est_offset = 3
    else:
        # Assume the time is already in EST
        est_offset = 0
    time_string = datetime.strptime(time_string,'%H:%M')+timedelta(hours = est_offset)
    return time_string

def extract_time(input_string):
    try:
        input_string = reduce_spaces(input_string)
        input_string = nospaceAMPM(input_string)

        found = re.compile(r'(\d{1,2})(:\d{2})?([APMapm]{2})?').findall(input_string)

        s = []
        for i in found:
            if i[-1]!='':
                s.append(i)

        d = []
        for i in s:
            raw = ""
            for j in i:
                raw = raw+j
            d.append(raw)

        d = [add_minutes_default00_format(i) for i in d]

        d = [convert_to_military_time(i) for i in d]

        d = [daylight_EST(input_string,i).strftime('%H:%M') for i in d]
        return d
    except:
        return None

def get_formatted_date_time(input_string):
    try:
        date = extract_date(input_string)
        if not date:
            return None
        times = extract_time(input_string)
        if times:
            final = f"{date} {times[0]}:00"
            print(f"Date Formatted Successfully {final}")
            return final
        else:
            return None

    except Exception as e:
        print(e)
        return None

# Example usage:
input_string = '''1 Nov 2023 3pm – 3:30pm EST'''
if __name__ == '__main__':
    dt = get_formatted_date_time(input_string)
    print(dt)
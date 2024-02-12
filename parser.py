import requests
import json
from datetime import datetime, timedelta
import pytz
from Date_time_Grabber import get_formatted_date_time as dfm
from Task_Selector import determine_task_type
from Insert_Candidate_data import insert_candidate_data
import pymysql
from Insert_Task_Data import insert_task_data
from Subject_entry import subject_entry
import logging
from flask import Flask, request, jsonify
import re
from fuzzywuzzy import process
from flask_cors import CORS
from EmailTransformation import EmailTransformation
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')



timeout = 10
db_config = {
    "charset": "utf8mb4",
    "connect_timeout": timeout,
    "cursorclass": pymysql.cursors.DictCursor,
    "db": "defaultdb",
    "host": "mysql-286ab86e-harshp-c41f.aivencloud.com",
    "password": "AVNS_s3Ckp3dyXV0bg4aXK0A",
    "read_timeout": timeout,
    "port": 13002,
    "user": "avnadmin",
    "write_timeout": timeout,
}

def normalize_keys(dictionary):
    """
    Normalize dictionary keys by removing consecutive whitespace characters.
    """
    normalized_dict = {}
    for key, value in dictionary.items():
        normalized_key = ' '.join(key.split())  # Split and rejoin with single space
        normalized_dict[normalized_key] = value
    return normalized_dict

def extract_number(text):
    number_words = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
    }
    text = text.lower()
    numeric_value = re.findall(r'\b(?:[1-9]|one|two|three|four|five|six|seven|eight|nine)\b', text)
    if numeric_value:
        extracted_value = numeric_value[0]
        if extracted_value.isdigit():
            return int(extracted_value)
        elif extracted_value in number_words:
            return number_words[extracted_value]

    words = text.split()
    for word in words:
        match = process.extractOne(word, number_words.keys())
        print(match)
        if match and match[1] >= 90:
            print(f"Extract_Number {number_words[match[0]]}")
            return number_words[match[0]]

    return 3

REQUESTBIN_URL = 'https://enm2qf5kijfx.x.pipedream.net/'


@app.route('/process_data', methods=['POST'])
def process_data():
    try:

        data = request.json

        
        data_entry = data['extracted_data']
        data_entry = normalize_keys(data_entry)
        Subject = data_entry['Subject']['value']
        subject_entry(Subject, db_config)
        candidate_name = data_entry['Candidate Name']['value']
        birth_date = data_entry['Birth date']['value']
        gender = data_entry['Gender']['value']
        education = data_entry['Education']['value']
        university = data_entry.get("University", {}).get('value')
        experience = data_entry.get("Total Experience in Years", {}).get('value')
        experience = str(experience)
        experience = extract_number(experience)
        if len(str(experience))>1:
            experience = extract_number(experience)
        state = data_entry.get("State", {}).get('value')
        technology = data_entry.get("Technology", {}).get('value')
        end_client = data_entry.get("End Client", {}).get('value')
        round = data_entry.get("Interview Round 1st 2nd 3rd or Final round", {}).get('value')
        job_title = data_entry.get("Job Title in JD", {}).get('value')
        email = data_entry.get("Email ID", {}).get('value')
        email_sent_by = EmailTransformation(data_entry.get("Sent By", {}).get('value'))
        contact_number = data_entry.get("Personal Contact Number", {}).get('value')
        interview_datetime = data_entry.get("Date and Time of Interview (Mention time zone)", {}).get('value')
        formatted_datetime = dfm(interview_datetime)
        duration = data_entry.get("Duration", {}).get('value', 60)  # Default to 60 if not present
        Task_type = determine_task_type(Subject)

        post_data = {
            "Subject": Subject,
            "candidate_name": candidate_name,
            "birth_date": birth_date,
            "gender": gender,
            "education": education,
            "university": university,
            "experience": experience,
            "state": state,
            "technology": technology,
            "end_client": end_client,
            "round": round,
            "job_title": job_title,
            "email": email,
            "email_sent_byy": email_sent_by,
            "contact_number": contact_number,
            "interview_datetime": interview_datetime,
            "formatted_datetime": formatted_datetime,
            "duration": duration,
            "Task_type": Task_type
        }
        response = requests.post(REQUESTBIN_URL, json=post_data)
        logging.info("Response from REQUESTBIN_URL: %s", response.text)

        
        candidate_data = {
            "Candidate_Name": candidate_name,
            "Birth_Date": birth_date,
            "Gender": gender,
            "Education": education,
            "University": university,
            "Total_Experience": int(experience),
            "State": state,
            "Technology": technology,
            
            "Email_ID": email,
            "Contact_Number": contact_number,
        }

        candidate_id = insert_candidate_data(candidate_data, db_config)

        task_data = {
            "Task_Type": Task_type,
            "Support_Subject": Subject,
            "End_Client": end_client,
            "Job_Title": job_title,
            "Duration": duration,
            "Interview_Round": round,
            "Interview_Datetime": formatted_datetime
        }

        x = insert_task_data(candidate_id, task_data, db_config)

        response_data = {
                "First_Model_Output": data,
                "Interview_Datetime": interview_datetime,
                "Candidate_Data": candidate_data,
                "Task_Data": task_data
            }
        return json.dumps(response_data, default=str), 200
    except Exception as e:
        logging.error("An error occurred while processing data: %s", e)
        return jsonify({"error": "An error occurred while processing data"}), 500


if __name__ == '__main__':
    app.run()
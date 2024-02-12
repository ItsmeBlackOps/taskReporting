import pymysql


def insert_candidate_data(candidate_data, db_config):
    try:
        # Connect to the database
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()

        # Check if the candidate already exists
        cursor.execute("SELECT Candidate_ID FROM Candidates WHERE Candidate_Name = %s", (candidate_data["Candidate_Name"],))
        existing_candidate = cursor.fetchone()

        if existing_candidate:
            print(f"Duplicate candidate found with Candidate_ID: {existing_candidate['Candidate_ID']}")
            return existing_candidate['Candidate_ID']
        else:
            # Insert candidate data into Candidates table
            insert_candidate_query = """
            INSERT INTO Candidates (Candidate_Name, Birth_Date, Gender, Education, University,
            Total_Experience, State, Technology, Email_ID, Contact_Number)
            VALUES (%(Candidate_Name)s, %(Birth_Date)s, %(Gender)s, %(Education)s, %(University)s,
            %(Total_Experience)s, %(State)s, %(Technology)s, %(Email_ID)s, %(Contact_Number)s)
            """
            cursor.execute(insert_candidate_query, candidate_data)

            # Commit the changes to the database
            connection.commit()

            # Retrieve the auto-generated Candidate_ID
            cursor.execute("SELECT LAST_INSERT_ID()")
            candidate_id = cursor.fetchone()['LAST_INSERT_ID()']

            print(f"Candidate data inserted successfully with Candidate_ID: {candidate_id}")
            return candidate_id

    finally:
        connection.close()

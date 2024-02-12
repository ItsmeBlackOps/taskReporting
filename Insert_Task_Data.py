import pymysql
def insert_task_data(candidate_id, task_data, db_config):
    try:
        # Connect to the database
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()

        check_duplicate_query = """
        SELECT Task_ID FROM Task2 
        WHERE Support_Subject = %(Support_Subject)s
        """
        cursor.execute(check_duplicate_query, task_data)
        duplicate_task = cursor.fetchone()
        
        if duplicate_task:
            print(f"Duplicate task found. Skipping insertion. {duplicate_task}")
            return "Duplicate task found. Skipping insertion."
        
        # Insert task data into Tasks table
        task_data["Candidate_ID"] = candidate_id
        insert_task_query = """
        INSERT INTO Task2 (Candidate_ID, Task_Type, Support_Subject, End_Client, Job_Title, Duration, Interview_Round, Interview_Datetime)
        VALUES (%(Candidate_ID)s, %(Task_Type)s, %(Support_Subject)s, %(End_Client)s, %(Job_Title)s, %(Duration)s, %(Interview_Round)s, %(Interview_Datetime)s)
        """
        cursor.execute(insert_task_query, task_data)
        
        # Get the auto-generated Task_ID
        task_id = cursor.lastrowid

        # Insert Task_ID into Task_Completion_Details table
        insert_completion_query = """
        INSERT INTO Task_Completion_Details (Task_ID, Completion_Status)
        VALUES (%s, %s)

        """
        completion_status = 'Pending'  # Set your default completion status here
        # Adjust the completion date based on your requirements or set it to NULL if it's not available at this stage
        completion_date = None
        cursor.execute(insert_completion_query, (task_id, completion_status))

        # Commit the changes to the database
        connection.commit()

        print(f"Task data inserted successfully. {task_id}")
        return f"Task data inserted successfully. {task_id}"
    except pymysql.Error as e:
        print(f"An error occurred: {e}")

    finally:
        connection.close()
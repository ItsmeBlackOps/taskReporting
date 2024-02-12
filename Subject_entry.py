import pymysql

def subject_entry(text, db_config):
    try:
        # Connect to the database
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()

        query = """
Insert into Debugg (Support_Subject) values (%s);"""
        cursor.execute(query, text)
        connection.commit()
        print("Sub Entered Successfully")
    except pymysql.Error as e:
        print(f"Error {e}")
    finally:
        connection.close()
import psycopg3
import os

# connect to the database using env args
env_database=os.getenv('DB_NAME')
env_user=os.getenv('DB_USER')
env_password=os.getenv('DB_PASSWORD')
env_host=os.getenv('DB_HOST')
env_port=os.getenv('DB_PORT')

### Database fundamentals
conn = psycopg3.connect(database=env_database, 
                        user=env_user, 
                        password=env_password, 
                        host=env_host, 
                        port=env_port)

def query_row(query):
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()
            return row
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def query_all(query):
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def query_execute(query):
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            conn.commit()
            print("Query executed successfully")
    except Exception as e:
        print(f"An error occurred: {e}")
    
def close_connection():
    try:
        if conn:
            conn.close()
            print("Database connection closed.")
    except Exception as e:
        print(f"An error occurred while closing the connection: {e}")

# Ensure the connection is closed if the application crashes
import atexit
atexit.register(close_connection)
### End of Database fundamentals

### Sailor CRUD operations
def get_sailors():
    query = "SELECT * FROM sailor"
    return query_all(query)





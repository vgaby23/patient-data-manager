from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os 

load_dotenv()

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

def create_connection():
    # Establish connection to database
    try:
        db_url = f"mysql+mysqlconnector://{username}:{password}@localhost/"
        
        engine = create_engine(db_url)
        
        conn = engine.connect()
        return conn
        
    except SQLAlchemyError as e:
        print(f"Error while connecting to Database: {e}")
        return None


def close_connection(conn):
    if conn is not None and not conn.closed:
        conn.close()
        print("Connection is Closed")
import mysql.connector
from mysql.connector import Error


def create_connection():

    try:
        # Establish connection session
        conn = mysql.connector.connect(
            host = "localhost",
            user = "vanessagabriela",
            password = "Moch1998",
            database = "patient"
        )

        if conn.is_connected():
            print("Successfully connected to Database")

            # Create cursor to execute SQL statement
            cursor = conn.cursor()
        
        return conn, cursor
    
    except Error as e:
        print(f"Error while connectin to Database: {e}")

        return None, None


def close_connection(conn, cursor):
    # Close existing connection
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("Connection is Closed")


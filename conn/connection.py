import mysql.connector
from mysql.connector import Error


def create_connection():

    try:
        # Establish connection session
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "vgaby_VG23",
            use_pure = True
        )

        if conn.is_connected():
        #     cursor = conn.cursor()
            return conn
    
    except Error as e:
        print(f"Error while connectin to Database: {e}")

        return None


def close_connection(conn, cursor):
    # Close existing connection
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("Connection is Closed")

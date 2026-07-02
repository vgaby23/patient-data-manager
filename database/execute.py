from conn import connection
import database.query as q
import sys
from sqlalchemy import text

class Database:
    @staticmethod
    def execute_sql_script(cursor, query_string, success_message):
        try:
            statements = [s.strip() for s in query_string.split(';') if s.strip()]
            for statement in statements:
                cursor.execute(text(statement))
            print(success_message)
        except Exception as e:
            print(f'Error: {e}')
            sys.exit(1)

    @classmethod
    def execute_create_all(cls):

        conn = connection.create_connection()

        try:
            cls.execute_sql_script(
                conn,
                q.create_database_query,
                'Database successfully created...'
            )
            
            conn.execute(text("USE hospital_manager"))
            
            cls.execute_sql_script(conn, q.create_insert_patient_query, 'Patients table successfully created...')
            cls.execute_sql_script(conn, q.create_insert_doctor_query, 'Doctors table successfully created...')
            cls.execute_sql_script(conn, q.create_insert_treatment_query, 'Treatments table successfully created...')
            cls.execute_sql_script(conn, q.create_insert_appointment_query, 'Appointments table successfully created...') 
            cls.execute_sql_script(conn, q.create_insert_bill_query, 'Bills table successfully created...')      

            conn.commit()
            print("All tables created and data successfully committed!")
        except Exception as e:
            print(f'Transaction failed, rolling back: {e}')
            conn.rollback()
        finally:
            connection.close_connection(conn)
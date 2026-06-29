from conn import connection
import database.query as q
import sys

class Database:
    @staticmethod
    def execute_sql_script(cursor, query_string, success_message):
        try:
            statements = [s.strip() for s in query_string.split(';') if s.strip()]
            for statement in statements:
                cursor.execute(statement)
            print(success_message)
        except Exception as e:
            print(f'Error: {e}')
            sys.exit(1)

    # class create:
    #     # Create Database
    #     def create_database(cursor):
    #         try:
    #             for statement in q.create_database_query.split(';'):
    #                 if statement.strip(): 
    #                     cursor.execute(statement.strip()) 
    #             print('Database successfully created...')
    #         except Exception as e:
    #             print(e)

    #     def create_patients(cursor):
    #         try:
    #             for statement in q.create_insert_patient_query.split(';'):
    #                 if statement.strip(): 
    #                     cursor.execute(statement.strip()) 
    #             print('Patients table successfully created...')
    #         except Exception as e:
    #             print(e)
    #             sys.exit(1)

    #     def create_appointments(cursor):
    #         try:
    #             for statement in q.create_insert_appointment_query.split(';'):
    #                 if statement.strip(): 
    #                     cursor.execute(statement.strip())
    #             print('Appointments table successfully created...')
    #         except Exception as e:
    #             print(e)
    #             sys.exit(1)

    #     def create_doctors(cursor):
    #         try:
    #             for statement in q.create_insert_doctor_query.split(';'):
    #                 if statement.strip(): 
    #                     cursor.execute(statement.strip())
    #             print('Doctors table successfully created...')
    #         except Exception as e:
    #             print(e)
    #             sys.exit(1)

    #     def create_treatments(cursor):
    #         try:
    #             for statement in q.create_insert_treatment_query.split(';'):
    #                 if statement.strip(): 
    #                     cursor.execute(statement.strip())
    #             print('Treatments table successfully created...')
    #         except Exception as e:
    #             print(e)
    #             sys.exit(1)

    #     def create_bills(cursor):
    #         try:
    #             for statement in q.create_insert_bill_query.split(';'):
    #                 if statement.strip(): 
    #                     cursor.execute(statement.strip())
    #             print('Bills table successfully created...')
    #         except Exception as e:
    #             print(e)
    #             sys.exit(1)

    @classmethod
    def execute_create_all(cls):

        conn = connection.create_connection()
        cursor = conn.cursor(buffered = True)

        try:
            cls.execute_sql_script(
                cursor,
                q.create_database_query,
                'Database successfully created...'
            )
            
            cursor.execute("USE hospital_manager")
            
            cls.execute_sql_script(cursor, q.create_insert_patient_query, 'Patients table successfully created...')
            cls.execute_sql_script(cursor, q.create_insert_doctor_query, 'Doctors table successfully created...')
            cls.execute_sql_script(cursor, q.create_insert_treatment_query, 'Treatments table successfully created...')
            cls.execute_sql_script(cursor, q.create_insert_appointment_query, 'Appointments table successfully created...') 
            cls.execute_sql_script(cursor, q.create_insert_bill_query, 'Bills table successfully created...')      

            conn.commit()
            print("All tables created and data successfully committed!")
        except Exception as e:
            print(f'Transaction failed, rolling back: {e}')
            conn.rollback()
        finally:
            connection.close_connection(conn, cursor)
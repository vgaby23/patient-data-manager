from conn import connection
import database.query as q
import sys

# Create Database
def create_database(cursor):
    try:
        for statement in q.create_database_query.split(';'):
            if statement.strip(): 
                cursor.execute(statement.strip()) 
        print('Database successfully created...')
    except Exception as e:
        print(e)

def create_patients(cursor):
    try:
        for statement in q.create_insert_patient_query.split(';'):
            if statement.strip(): 
                cursor.execute(statement.strip()) 
        print('Patients table successfully created...')
    except Exception as e:
        print(e)
        sys.exit(1)

def create_appointments(cursor):
    try:
        for statement in q.create_insert_appointment_query.split(';'):
            if statement.strip(): 
                cursor.execute(statement.strip())
        print('Appointments table successfully created...')
    except Exception as e:
        print(e)
        sys.exit(1)

def create_doctors(cursor):
    try:
        for statement in q.create_insert_doctor_query.split(';'):
            if statement.strip(): 
                cursor.execute(statement.strip())
        print('Doctors table successfully created...')
    except Exception as e:
        print(e)
        sys.exit(1)

def create_treatments(cursor):
    try:
        for statement in q.create_insert_treatment_query.split(';'):
            if statement.strip(): 
                cursor.execute(statement.strip())
        print('Treatments table successfully created...')
    except Exception as e:
        print(e)
        sys.exit(1)

def create_bills(cursor):
    try:
        for statement in q.create_insert_bill_query.split(';'):
            if statement.strip(): 
                cursor.execute(statement.strip())
        print('Bills table successfully created...')
    except Exception as e:
        print(e)
        sys.exit(1)
    

def execute_all():
    conn = connection.create_connection()
    cursor = conn.cursor(buffered = True)

    create_database(cursor)
    cursor.execute("USE hospital_manager")
    
    create_patients(cursor)
    create_doctors(cursor)
    create_treatments(cursor)
    create_appointments(cursor) 
    create_bills(cursor)       

    conn.commit()
    print("All tables created and data successfully committed!")

    connection.close_connection(conn, cursor)
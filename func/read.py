from conn.connection import create_connection
from func.field import ask_data
from basic_func import main_menu
from tabulate import tabulate
import config

conn = create_connection()
cursor = conn.cursor()

def connect(query, cursor):
    cursor.execute(query)

    rows = cursor.fetchall()
    headers = cursor.column_names
    
    return rows, headers

class read_actions:

    def retrieve_data(cursor, mandatory_data, limit):
        
        where_mandatory_string = f"(last_name like '%{mandatory_data['patient_last_name']}%' or first_name like '%{mandatory_data['patient_first_name']}%')' "

        if limit == 'all':
            limit_string = ''
        else:
            limit_string = f'LIMIT{int(limit)}'
        query = f'''
                SELECT *
                FROM patients
                WHERE {where_mandatory_string}
                {limit_string}
                '''

        rows, headers = connect(query, cursor)

        return rows, headers

def print_menu(staff_name):
    menu_lines = [
        f"Hello {staff_name.upper()}!",
        "=" * config.MENU_WIDTH,
        " ",
        "Welcome to Patient Data Manager",
        " ",
        "=" * config.MENU_WIDTH,
        " ",
        "How would you like to proceed?",
        " ",
        "=" * config.MENU_WIDTH,
        " ",
        "1 - Check another patient data",
        "2 - Back to main menu",
        " "
    ]

    return main_menu(menu_lines)
    


def process(staff_name):
    cursor.execute("USE hospital_manager")
    
    mandatory_data, limit = ask_data('read')

    rows, headers = retrieve_data(cursor, mandatory_data, limit)

    print("PATIENT'S DATA SEARCH RESULT\n")

    print(tabulate(rows, headers=headers, tablefmt="grid"))

    option = print_menu(staff_name)

    if option == '1':
        process()

def access_appointments(patient_id):
    query = f'''
    SELECT appointment_date, appointment_time, (d.first_name + ' ' + df.last_name) as doctor_name, specialization, reason_for_visit, hospital, branch, status
    from appointments a
    join doctors d on a.doctor_id = d.doctor_id
    where patient_id = {patient_id}
    '''
    rows, headers = connect(query, cursor)
    print(tabulate(rows, headers=headers, tablefmt="grid"))
    
def data_to_check():
    option_ = None
    while option_ != 'n':
        patient_id = input("Which patient_id would you like to check? Type 'n' if you want to go back to the main menu")
        print('Patient Menu:')
        print('1. Appointments')
        print('2. Bills')
        option_ = int(input('Which data would you like to access?(Type number only)'))
        
        if option_ == 1:
            access_appointments(patient_id)
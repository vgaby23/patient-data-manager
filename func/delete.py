from conn.connection import create_connection
from func.field import ask_data
from func.read import retrieve_data
from basic_func import main_menu
import config

conn = create_connection()
cursor = conn.cursor()

def delete_data(cursor, mandatory_data):

    where_mandatory_string = f"patient_name like '%{mandatory_data['patient_last_name']}%' and gender == {mandatory_data['gender']} and '%{mandatory_data['patient_first_name']}%'"

    query = f'''
            DELETE p
            FROM patient p
            WHERE {where_mandatory_string}
            '''

    cursor.execute(query)

    rows_deleted = cursor.rowcount

    return rows_deleted

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
        "1 - Proceed with another deletion",
        "2 - Back to main menu",
        " "
    ]

    main_menu(menu_lines)


def process(staff_name):
    cursor.execute("USE hospital_manager")

    confirmation = 'n'
    while confirmation != 'Y':

        mandatory_data, limit = ask_data('delete')
        data_rows = retrieve_data(cursor, mandatory_data, limit)

        for row in data_rows:
            print(row)
        
        confirmation = input('Would you like to delete all of this patient data? Note: This action is irreversible (Y/n)')

        print('Proceed with deletion...')
        print()
        print('Deletion completed!')

    print_menu(staff_name)
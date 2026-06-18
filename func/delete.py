from conn.connection import create_connection
from field import ask_data
from read import retrieve_data

conn, cursor = create_connection()

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

def process():

    confirmation = 'n'
    while confirmation != 'Y':

        mandatory_data, limit = ask_data('delete')
        data_rows = retrieve_data(cursor, mandatory_data, limit)

        for row in data_rows:
            print(row)
        
        confirmation = input('Would you like to delete all of this patient data? Note: This action is irreversible (Y/n)')
    



    
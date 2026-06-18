from conn.connection import create_connection
from field import ask_data
import os

conn, cursor = create_connection()

def retrieve_data(cursor, mandatory_data, limit):
    
    where_mandatory_string = f"patient_name like '%{mandatory_data['patient_last_name']}%' and gender == {mandatory_data['gender']} and '%{mandatory_data['patient_first_name']}%'"

    if limit == 'all':
        limit_string = ''
    else:
        limit_string = f'LIMIT{int(limit)}'
    query = f'''
            SELECT *
            FROM patient 
            WHERE {where_mandatory_string}
            {limit_string}
            '''

    cursor.execute(query)

    rows = cursor.fetchall()

    return rows


def process():
    mandatory_data, limit = ask_data('read')

    data_rows = retrieve_data(cursor, mandatory_data, limit)

    print("PATIENT'S DATA SEARCH RESULT\n")

    for row in data_rows:
        print(row)

    retry = input("Would you like to search for another patient's data?(Y/n): ")

    if retry == 'Y':
        process()
    

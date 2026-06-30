
from tabulate import tabulate
import subprocess
from crud.patient_module.input import mandatory_field
from crud import menu_details
from datetime import datetime
import re


def execute_db_action(cursor, query, params=None, action='read'):
    """Handles all database execution safely using parameterized queries."""
    cursor.execute("USE hospital_manager")
    
    cursor.execute(query, params or ())

    if action == 'read':
        rows = cursor.fetchall()
        headers = cursor.column_names
        return rows, headers
        
    elif action == 'create':
        new_id = cursor.lastrowid
        print(f'\nSuccess! Created patient record with generated ID: {new_id}')
        return new_id
        
    elif action in ('update', 'delete'):
        if cursor.rowcount == 0:
            print("\nWarning: No patient data was modified. Check your criteria.")
        else:
            print(f"\nSuccess! Modified {cursor.rowcount} patient record(s).")
        return cursor.rowcount

class CRUDPatient:

    @staticmethod
    def get_profile(cursor):

        subprocess.run(["clear"])

        print("\033[3mFill in patient's data below\033[0m")
        print()
        patient_first_name = mandatory_field("First name: ")
        patient_last_name = mandatory_field("Last name: ")

        query = '''
                SELECT *
                FROM patients
                WHERE last_name like %s and first_name like %s
                ORDER BY registration_date desc, last_name desc
                '''
        params = (f"%{patient_last_name}%", f"%{patient_first_name}%")

        rows, headers = execute_db_action(cursor, query, params, 'read')

        print("\nPATIENT'S DATA SEARCH RESULT\n")
        if rows:
            print(tabulate(rows, headers=headers, tablefmt="grid"))
        else:
            print("No matching patients found.")

        return rows
    
    @staticmethod
    def create_profile(cursor):
        subprocess.run(["clear"])

        print("\033[1;33m=== REGISTER NEW PATIENT PROFILE ===\033[0m\n")
        
        first_name = mandatory_field("First name").strip().title()
        last_name = mandatory_field("Last name").strip().title()
        
        # Gender validation
        while True:
            gender = mandatory_field("Gender(F/M)").strip().upper()
            if gender in ('M', 'F'):
                break
            print("\033[31m❌ Invalid input. Please enter exactly 'M' for Male or 'F' for Female.\033[0m")
        
        # DOB validation
        while True:
            dob_input = mandatory_field("Date of Birth (yyyy-mm-dd): ").strip()
            try:
                # This forces Python to check if the user typed a valid date
                dob_input = datetime.strptime(dob_input, "%Y-%m-%d").date()
                if dob_input > datetime.today().date():
                    print("\033[31m❌ Date of Birth cannot be in the future.\033[0m")
                    continue
                break
            except ValueError:
                print("\033[31mInvalid date format! Please use YYYY-MM-DD (e.g., 1995-05-12).\033[0m")
        
        # Email validation
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        while True:
            email = mandatory_field("Email").strip().lower()
            if re.match(email_regex, email):
                break
            print("\033[31m❌ Invalid email format (e.g., patient@example.com).\033[0m")

        # Contact number validation, numbers only
        while True:
            contact_number = mandatory_field("Contact Number").strip()
            clean_phone = contact_number.replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
            if clean_phone.isdigit() and len(clean_phone) >= 7:
                break
            print("\033[31m❌ Invalid phone number. Please enter digits only.\033[0m")

        insurance_provider = mandatory_field("Insurance Provider").strip().title()
        insurance_number = mandatory_field("Insurance Number").strip()
        address = mandatory_field("Address").strip()
        
        query = """ 
            INSERT INTO patients (
                first_name, last_name, gender, date_of_birth, 
                contact_number, address, insurance_provider, insurance_number, email
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (first_name, last_name, gender, dob_input, contact_number, address, insurance_provider, insurance_number, email)

        execute_db_action(cursor, query, params, 'create')
        
    @staticmethod
    def update_profile(cursor):
        map_ = {'1': 'contact_number', '2': 'address', '3': 'email', '4': 'insurance_number', '5': 'insurance_provider'}
        
        patients = CRUDPatient.get_profile(cursor)

        if not patients:
            print('\nNo patients were found to update.')
            return

        valid_ids = [str(patient[0]) for patient in patients]

        while True:
            update_id = mandatory_field('patient ID to update (or type "q" to cancel): ').strip()
            
            if update_id.lower() == 'q':
                print("Update cancelled.")
                return
                
            if update_id not in valid_ids:
                print(f"\033[31m❌ Error: ID {update_id} is not in the search results above. Please choose a visible ID.\033[0m")
                continue
                
            print(f"✅ ID {update_id} selected for update.")
            break
        
        while True:
            option = menu_details.main_menu(menu_details.patient_data_update_lines)
            opt_list = [val.strip() for val in option.split(',') if val.strip()]
            update_dict = dict()
            
            if '6' in opt_list:
                print('\nReturning to the previous menu..')
                return
            is_valid = all(val in map_ for val in opt_list)
            if not is_valid or not opt_list:
                print('Wrong Number provided, please re-enter')
                continue
        
            for val in opt_list:
                val_to_update = mandatory_field(f'new {map_[val].replace('_',' ').capitalize()}: ')
                update_dict[map_[val]] = val_to_update
            
            break
        if not update_dict:
            print("No changes were made.")
            return
        
        set_clauses = [f"{column} = %s" for column in update_dict.keys()]
        dynamic_set_string = ", ".join(set_clauses)
        
        query = f'''
            UPDATE patients
            SET {dynamic_set_string}
            WHERE patient_id = %s
            '''
        
        params = tuple(update_dict.values()) + (update_id,)

        execute_db_action(cursor, query, params, 'update')
    
    @staticmethod
    def delete_profile(cursor):
        patients = CRUDPatient.get_profile(cursor)

        if not patients:
            print('\nNo patients were found to delete.')
            return

        valid_ids = [str(patient[0]) for patient in patients]

        while True:
            patient_id = mandatory_field('patient ID to delete (or type "q" to cancel): ').strip()
            
            if patient_id.lower() == 'q':
                print("Update cancelled.")
                return
                
            if patient_id not in valid_ids:
                print(f"\033[31m❌ Error: ID {patient_id} is not in the search results above. Please choose a visible ID.\033[0m")
                continue
                
            print(f"✅ ID {patient_id} selected for deletion.")
            break

        while True:
            print(f'Are you sure, you want to delete data of patient ID {patient_id}?')
            print('This action is irreversible')
            option = mandatory_field('(Yes/No):')
            
            if option.lower() in ('no','n'):
                print('\nReturning to the previous menu..')
                return
            elif option.lower() in ('yes', 'y'):
                break
            else:
                print("\033[31m❌Invalid input. Please type 'Yes' or 'No'\033[0m")
            

        query = '''
            DELETE FROM patients
            WHERE patient_id = %s
            '''
        params = (patient_id,)

        execute_db_action(cursor, query, params, 'delete')
    


def main(conn):

    cursor = conn.cursor()

    while True:
        option = menu_details.main_menu(menu_details.patient_menu_lines)
        try:
            if option == '1': #Create
                CRUDPatient.create_profile(cursor)
                conn.commit()
            elif option == '2': #Read
                CRUDPatient.get_profile(cursor)
            elif option == '3': #Update
                CRUDPatient.update_profile(cursor)
                conn.commit()
            elif option == '4': #Delete
                CRUDPatient.delete_profile(cursor)
                conn.commit()
            elif option == '5': #Back to main menu
                print('Returning to the main menu...')
                break
            else:
                print("Invalid option. Please choose 1-5.")
            
            input("\nPress Enter to continue...")
        except Exception as e:
            print(f"An error occurred: {e}")
            if conn.is_connected():
                conn.rollback()
            input("\nPress Enter to continue...")
        
    # cursor.close()
    # conn.close()



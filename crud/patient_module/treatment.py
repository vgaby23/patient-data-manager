from tabulate import tabulate
import subprocess
from crud.patient_module.input import mandatory_field
from crud.patient_module import appointment
from crud import menu_details
from datetime import datetime
from sqlalchemy import text
import re

def execute_db_action(conn, query, params=None, action='read'):

    # Establish connection
    result = conn.execute(text(query), params or {})

    # Breakdown how to fetch the data based on the type of action
    if action == 'read':
        rows = result.fetchall()
        headers = list(result.keys())
        return rows, headers
        
    elif action == 'create':
        new_id = result.lastrowid
        print(f'\nSuccess! Created treatment record with generated ID: {new_id}')
        return new_id
        
    elif action in ('update', 'delete'):
        if result.rowcount == 0:
            print("\nWarning: No treatment data was modified. Check your criteria.")
        else:
            print(f"\nSuccess! Modified {result.rowcount} treatment record(s).")
        return result.rowcount

class CRUDTreatment:

    @staticmethod
    def get_treatment(conn):
        subprocess.run(["clear"])

        print("\033[3mFill in patient's data below\033[0m\n")
        
        patient_first_name = mandatory_field("First name: ")
        patient_last_name = mandatory_field("Last name: ")

        query = '''
                SELECT 
                p.patient_id, concat(p.first_name,' ',p.last_name) as patient_name, treatment_date,
                treatment_id, treatment_type, t.description, status
                FROM patients p
                left join appointments a on p.patient_id = a.patient_id
                left join treatments t on a.appointment_id = t.appointment_id
                where a.status in ('Scheduled') and last_name like :last_name and first_name like :first_name
                ORDER BY patient_id, appointment_date;
                '''
        
        params = {
            "last_name": f"%{patient_last_name}%",
            "first_name": f"%{patient_first_name}%"
        }

        rows, headers = execute_db_action(conn, query, params, 'read')

        print("\nTREATMENT'S DATA SEARCH RESULT\n")
        if rows:
            print(tabulate(rows, headers=headers, tablefmt="grid"))
        else:
            print("No matching treatment found.")

        return rows
    
    @staticmethod
    def create_treatment(conn):
        subprocess.run(["clear"])

        # Patient validation (Pass conn instead of cursor)
        patients = appointment.CRUDAppointments.get_appointment(conn)

        if not patients:
            print('\nNo patients were found.')
            return

        valid_ids = [str(patient[1]) for patient in patients]

        while True:
            appoint_id = input('\nEnter appointment ID for treatment (or type "q" to cancel): ').strip()
            
            if appoint_id.lower() == 'q':
                print("Update cancelled.")
                return
                
            if appoint_id not in valid_ids:
                print(f"\033[31m❌ Error: ID {appoint_id} is not in the search results above. Please choose a visible ID.\033[0m")
                continue
                
            print(f"✅ ID {appoint_id} selected for creating new treatment.")
            break

        query_get_treatment = """
                            SELECT treatment_id, treatment_type, description, cost, treatment_date 
                            from treatments
                            where appointment_id = :appoint_id """
        
        param = {"appoint_id": int(appoint_id)}
        
        rows, headers = execute_db_action(conn, query_get_treatment, param, 'read')
        
        opt = 'Y' # Default to Yes
        if rows:
            print('Treatment is already scheduled on this appointment.')
            print(tabulate(rows, headers=headers, tablefmt="grid"))
            opt = input('Would you like to schedule another one? (Y/N): ').strip().upper()
        
        if opt == 'N':
            return
        else: 
            print("\033[1;33m=== SCHEDULE A TREATMENT ===\033[0m\n")

            # Treatment type
            opt_list = {'1': 'Chemotherapy' , '2': 'MRI', '3': 'ECG', '4': 'Physiotherapy', '5': 'X-Ray'}

            while True:
                print('Treatment List:')
                for key, value in opt_list.items():
                    print(f'{key}: {value}')
                
                treatment_type_opt = mandatory_field("Choose treatment type (1-5): ").strip()
                if treatment_type_opt not in ('1', '2', '3', '4', '5'):
                    print("\033[31m❌ Value is invalid! Choose value between 1 to 5\033[0m")
                    continue
                else:
                    break

            # Description
            description = mandatory_field("Type details of the treatment: ").strip()

            # Cost
            while True:
                cost = mandatory_field("Treatment cost: ").strip()
                try:
                    cost_value = int(cost)
                    if cost_value < 0:
                        print("\033[31m❌ Please enter a correct, positive value\033[0m")
                        continue
                    break
                except ValueError:
                    print("\033[31m❌ Invalid input! Please enter a valid whole number.\033[0m")

            # Treatment Date
            while True:
                dot_input = mandatory_field("Date of Treatment (yyyy-mm-dd): ").strip()
                try:
                    dot_input = datetime.strptime(dot_input, "%Y-%m-%d").date()
                    if dot_input < datetime.today().date():
                        print("\033[31m❌ Date of Treatment cannot be in the past.\033[0m")
                        continue
                    break
                except ValueError:
                    print("\033[31mInvalid date format! Please use YYYY-MM-DD (e.g., 1995-05-12).\033[0m")

            query = """ 
                INSERT INTO treatments (
                    appointment_id, treatment_type, description, cost, treatment_date
                ) VALUES (
                    :appoint_id, :treatment_type, :description, :cost, :dot_input
                )
            """
            
            params = {
                "appoint_id": appoint_id,
                "treatment_type": opt_list[treatment_type_opt],
                "description": description,
                "cost": cost,
                "dot_input": dot_input
            }

            execute_db_action(conn, query, params, 'create')
        
    @staticmethod
    def delete_treatment(conn):
        patients = CRUDTreatment.get_treatment(conn)

        if not patients:
            print('\nNo treatments were found to delete.')
            return

        valid_ids = [str(patient[3]) for patient in patients]

        #Treatment ID validation
        while True:
            treatment_id = mandatory_field('\nEnter treatment ID to delete (or type "q" to cancel): ').strip()
            
            if treatment_id.lower() == 'q':
                print("Deletion cancelled.")
                return
                
            if treatment_id not in valid_ids:
                print(f"\033[31m❌ Error: ID {treatment_id} is not in the search results above. Please choose a visible ID.\033[0m")
                continue
                
            print(f"✅ ID {treatment_id} selected for deletion.")
            break
        
        # Delete action re-confirmation
        while True:
            print(f'Are you sure you want to delete data of treatment ID {treatment_id}?')
            print('This action is irreversible')
            option = mandatory_field('(Yes/No): ').strip()
            
            if option.lower() in ('no', 'n'):
                print('\nReturning to the previous menu..')
                return
            elif option.lower() in ('yes', 'y'):
                break
            else:
                print("\033[31m❌ Invalid input. Please type 'Yes' or 'No'\033[0m")
            
        query = '''
            DELETE FROM treatments
            WHERE treatment_id = :treatment_id
            '''
        params = {"treatment_id": treatment_id}

        execute_db_action(conn, query, params, 'delete')
    

def main(conn):
    
    while True:
        subprocess.run(["clear"])
        option = menu_details.main_menu(menu_details.treatment_menu_lines)
        try:
            if option == '1': #Create
                CRUDTreatment.create_treatment(conn)
                conn.commit()
            elif option == '2': #Read
                CRUDTreatment.get_treatment(conn)
            elif option == '3': #Delete
                CRUDTreatment.delete_treatment(conn)
                conn.commit()
            elif option == '4': #Back to main menu
                print('Returning to the main menu...')
                break
            else:
                print("Invalid option. Please choose 1-4.")
            
            input("\nPress Enter to continue...")
        except Exception as e:
            print(f"An error occurred: {e}")
        
            if not conn.closed:
                conn.rollback()
            input("\nPress Enter to continue...")
from crud.patient_module.patient import CRUDPatient
from tabulate import tabulate
import subprocess
from crud.patient_module.input import mandatory_field
from crud import menu_details
from datetime import datetime
from sqlalchemy import text

def execute_db_action(conn, query, params=None, action='read'):
    
    # Establish connection with database
    conn.execute(text("USE hospital_manager"))
    result = conn.execute(text(query), params or {})

    # Breakdown how to fetch the data based on the type of action
    if action == 'read':
        rows = result.fetchall()
        headers = list(result.keys())
        return rows, headers
        
    elif action == 'create':
        new_id = result.lastrowid
        print(f'\nSuccess! Created new appointment record with generated ID: {new_id}')
        return new_id
        
    elif action in ('update', 'delete'):
        if result.rowcount == 0:
            print("\nWarning: No appointment data was modified. Check your criteria.")
        else:
            print(f"\nSuccess! Modified {result.rowcount} appointment record(s).")
        return result.rowcount

class CRUDAppointments:

    @staticmethod
    def get_doctor(conn):

        # Return list of doctor names
        query = '''
                SELECT doctor_id, concat(first_name,' ',last_name) as doctor_name,
                        specialization, hospital_branch
                FROM doctors
                '''
        rows, headers = execute_db_action(conn, query)

        print("\nDOCTORS'S DATA\n")
        print(tabulate(rows, headers=headers, tablefmt="grid"))

        return rows

    @staticmethod
    def get_appointment(conn):
        subprocess.run(["clear"])

        print("\033[3mFill in patient's data below\033[0m\n")

        # Get patient data based on first name and last name
        patient_first_name = mandatory_field("First name: ")
        patient_last_name = mandatory_field("Last name: ")

        query = '''
                SELECT a.patient_id, appointment_id, concat(p.first_name,' ',p.last_name) as patient_name, 
                        appointment_date, concat(d.first_name,' ',d.last_name) as doctor_name, 
                        specialization, appointment_time, a.reason_for_visit, a.status
                FROM appointments a
                LEFT JOIN doctors d on a.doctor_id = d.doctor_id
                LEFT JOIN patients p on a.patient_id = p.patient_id
                WHERE (p.last_name like :last_name and p.first_name like :first_name) and status = 'Scheduled'
                ORDER BY patient_id, appointment_date, appointment_time
                '''
        
        params = {
            "last_name": f"%{patient_last_name}%", 
            "first_name": f"%{patient_first_name}%"
        }

        rows, headers = execute_db_action(conn, query, params, 'read')

        print("\nAPPOINTMENT DATA SEARCH RESULT\n")
        if rows:
            print(tabulate(rows, headers=headers, tablefmt="grid"))
        else:
            print("No matching appointment found.")

        return rows
    
    @staticmethod
    def create_appointment(conn):
        subprocess.run(["clear"])

        # Patient validation
        patients = CRUDPatient.get_profile(conn)

        if not patients:
            print('\nNo patients were found.')
            return

        valid_ids = [str(patient[0]) for patient in patients]

        while True:
            patient_id = mandatory_field('\nEnter patient ID (or type "q" to cancel): ').strip()
            
            if patient_id.lower() == 'q':
                print("Update cancelled.")
                return
                
            if patient_id not in valid_ids:
                print(f"\033[31m❌ Error: ID {patient_id} is not in the search results above. Please choose a visible ID.\033[0m")
                continue
                
            print(f"✅ ID {patient_id} selected for creating new appointments.")
            break

        print("\033[1;33m=== ADD NEW APPOINTMENT ===\033[0m\n")

        # Doctor Validation
        doctor_rows = CRUDAppointments.get_doctor(conn) 

        valid_doctor_ids = [str(doctor[0]) for doctor in doctor_rows]       
        while True:
            doctor_id = mandatory_field('\nEnter doctor ID for the appointment (or type "q" to cancel): ').strip()
            
            if doctor_id.lower() == 'q':
                print("Add new appointment cancelled.")
                return
                
            if doctor_id not in valid_doctor_ids:
                print(f"\033[31m❌ Error: ID {doctor_id} is not in the search results above. Please choose a visible ID.\033[0m")
                continue
            break

        # Appointment Date validation
        while True:
            appoint_date = mandatory_field("Appointment Date (yyyy-mm-dd): ").strip()
            try:
                appoint_date = datetime.strptime(appoint_date, "%Y-%m-%d").date()
                if appoint_date < datetime.today().date():
                    print("\033[31m❌ Appointment date cannot be in the past.\033[0m")
                    continue
                break
            except ValueError:
                print("\033[31mInvalid date format! Please use YYYY-MM-DD (e.g., 1995-05-12).\033[0m")

        opt_list = {'1': '10:15', '2': '11:15', '3': '13:00', '4': '14:15', '5': '15:15', '6': '16:15'}

        while True:
            print('Appointment Time List:')
            for key, value in opt_list.items():
                print(f'{key}: {value}')
            
            appoint_time_opt = mandatory_field("Choose appointment time (1-6): ").strip()
            if appoint_time_opt not in ('1', '2', '3', '4', '5', '6'):
                print("\033[31m❌ Value is invalid! Choose value between 1 to 6\033[0m")
                continue
            else:
                break
        
        # Reason for visit
        visit_reason = mandatory_field('Reason for visit: ') 

        query = """ 
            INSERT INTO appointments (
                patient_id, doctor_id, appointment_date, appointment_time, 
                reason_for_visit, status
            ) VALUES (
                :patient_id, :doctor_id, :appoint_date, :appoint_time, 
                :visit_reason, :status
            )
        """
        
        params = {
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appoint_date": appoint_date,
            "appoint_time": opt_list[appoint_time_opt],
            "visit_reason": visit_reason,
            "status": "Scheduled"
        }

        execute_db_action(conn, query, params, 'create')
        
    @staticmethod
    def update_appointment(conn):
        map_ = {'1': 'appointment_date', '2': 'appointment_time', '3': 'status'}
        
        appoint = CRUDAppointments.get_appointment(conn)

        # Check whether expected appointment exist or not
        if not appoint:
            print('\nNo appointment found.')
            return

        valid_ids = [str(val[1]) for val in appoint]

        # Start process of updating the appointment
        while True:
            update_id = mandatory_field('\nEnter appointment ID to update (or type "q" to cancel): ').strip()
            
            if update_id.lower() == 'q':
                print("Update cancelled.")
                return
                
            if update_id not in valid_ids:
                print(f"\033[31m❌ Error: ID {update_id} is not in the search results above. Please choose a visible ID.\033[0m")
                continue
                
            print(f"✅ ID {update_id} selected for update.")
            break
        
        # Choosing which field to update
        while True:
            option = menu_details.main_menu(menu_details.appointment_data_update_lines)
            opt_list = [val.strip() for val in option.split(',') if val.strip()]
            update_dict = dict()
            
            if '4' in opt_list:
                print('\nReturning to the previous menu..')
                return
            
            is_valid = all(val in map_ for val in opt_list)
            
            if not is_valid or not opt_list:
                print('Wrong Number provided, please re-enter')
                continue
            
            # Appointment time validation
            for val in opt_list:
                if val == '2':
                    time_opts = {'1': '10:15', '2': '11:15', '3': '13:00', '4': '14:15', '5': '15:15', '6': '16:15'}
                    while True:
                        print('Appointment Time List:')
                        for key, value in time_opts.items():
                            print(f'{key}: {value}')
                        
                        appoint_time_opt = mandatory_field("Choose new appointment time (1-6): ").strip()
                        if appoint_time_opt not in ('1', '2', '3', '4', '5', '6'):
                            print("\033[31m❌ Value is invalid! Choose value between 1 to 6\033[0m")
                            continue
                        else:
                            break
                    val_to_update = time_opts[appoint_time_opt]
                elif val == '3':
                    print('\033[1;32mAvailable Status: No-Show / Cancelled\033[0m')
                    val_to_update = mandatory_field(f'Enter new {map_[val].replace("_", " ").capitalize()}: ')
                else:
                    val_to_update = mandatory_field(f'Enter new {map_[val].replace("_", " ").capitalize()}: ')
                
                update_dict[map_[val]] = val_to_update
            
            break
            
        if not update_dict:
            print("No changes were made.")
            return
        
        # Update appointment values
        set_clauses = [f"{column} = :{column}" for column in update_dict.keys()]
        dynamic_set_string = ", ".join(set_clauses)
        
        query = f'''
            UPDATE appointments
            SET {dynamic_set_string}
            WHERE appointment_id = :appointment_id
            '''
        
        params = update_dict.copy()
        params["appointment_id"] = update_id

        execute_db_action(conn, query, params, 'update')

def main(conn):
    
    while True:
        subprocess.run(["clear"])
        option = menu_details.main_menu(menu_details.appointment_menu_lines)
        try:
            if option == '1': #Create
                CRUDAppointments.create_appointment(conn)
                conn.commit()
            elif option == '2': #Read
                CRUDAppointments.get_appointment(conn)
            elif option == '3': #Update
                CRUDAppointments.update_appointment(conn)
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
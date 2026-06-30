from conn.connection import create_connection
import subprocess
import sys
from crud.patient_module import patient, appointment, treatment, bill
from dotenv import load_dotenv, set_key
from crud import menu_details
from database.execute import Database

load_dotenv()

def main():

    #  Initiate database and table creation
    Database.execute_create_all()

    conn = create_connection()
    # Start Menu
    staff_name = input("Hello, Welcome to Patient Data Manager! \nPlease input your name before proceeding: ")      
    set_key(".env", "STAFF_NAME", staff_name)
    user_choice = None

    # subprocess.run(["clear"])

  
    while True:
        user_choice = menu_details.main_menu(menu_details.main_menu_lines)
        try:
            if user_choice == '1':
                patient.main(conn)
            elif user_choice == '2':
                appointment.main(conn)
            elif user_choice == '3': 
                treatment.main(conn)
            elif user_choice == '4':
                bill.main(conn)
            # elif user_choice == 5:
            #     menu_details.main_menu(menu_details.analytics_menu_lines)
            elif user_choice == '6':
                print('Goodbye!')
                conn.close()
                sys.exit(0)
                exit
                
        except ValueError as ve:
            print(f'⚠️ Input Error: {ve}')
        except KeyError as ke:
            print(ke)
        except Exception as e:
            raise e
            # print(f'An unexpected error occured: {e}')

if __name__ == '__main__':
    main()
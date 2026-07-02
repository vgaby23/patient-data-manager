from conn.connection import create_connection
import sys
import subprocess
from crud.patient_module import patient, appointment, treatment, bill, analytics
from dotenv import load_dotenv, set_key
from crud import menu_details
from database.execute import Database

load_dotenv()

def main():

    #  Initiate database and table creation
    Database.execute_create_all()
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during installation: {e}")
        
    subprocess.run(["clear"])

    conn = create_connection()
    # Start Menu
    staff_name = input("Hello, Welcome to Patient Data Manager! \nPlease input your name before proceeding: ")      
    set_key(".env", "STAFF_NAME", staff_name)
    user_choice = None
  
    while True:
        subprocess.run(["clear"])
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
            elif user_choice == '5':
                analytics.main(conn)
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

if __name__ == '__main__':
    main()
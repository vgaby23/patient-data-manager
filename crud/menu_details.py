import subprocess
from dotenv import load_dotenv, set_key
import os

load_dotenv()

staff_name = os.getenv('STAFF_NAME', 'Guest')
menu_width = int(os.getenv('MENU_WIDTH'))

main_menu_lines = [
    f"Hello {staff_name.upper()}!",
    "=" * menu_width,
    " ",
    "Welcome to Patient Data Manager",
    " ",
    "=" * menu_width,
    " ",
    "MAIN MENU",
    " ",
    "=" * menu_width,
    " ",
    "1 - Patient Data",
    "2 - Appointments",
    "3 - Bill",
    "4 - Treatments",
    "5 - Analytics",
    "6 - Exit",
    " "
]

patient_menu_lines = [
        f"Hello {staff_name.upper()}!",
        "=" * menu_width,
        " ",
        "Welcome to Patient Data Manager",
        " ",
        "=" * menu_width,
        " ",
        "PATIENT'S DATA MENU",
        " ",
        "=" * menu_width,
        " ",
        "1 - Create patient's data",
        "2 - Check patient's data",
        "3 - Update patient's data",
        "4 - Delete patient's data",
        "5 - Back to main menu",
        " "
    ]

patient_data_update_lines = [
    "Which data would you like to update?",
    " ",
    "=" * menu_width,
    "Note: If there are multiple values,", 
    "separate it by ','. Ex: 1,2,3,4 ",
    "=" * menu_width,
    '1. Contact Number',
    '2. Address',
    '3. Email',
    '4. Insurance Number',
    '5. Insurance Provider',
    '6. Cancel Update'
]

appointment_menu_lines = [
        f"Hello {staff_name.upper()}!",
        "=" * menu_width,
        " ",
        "Welcome to Patient Data Manager",
        " ",
        "=" * menu_width,
        " ",
        "APPOINTMENT MENU",
        " ",
        "=" * menu_width,
        " ",
        "1 - Create new appointment",
        "2 - Check appointment",
        "3 - Update appointment",
        "4 - Back to main menu",
        " "
    ]

appointment_data_update_lines = [
    "Which appointment data would you",
    "like to update?",
    " ",
    "=" * menu_width,
    "Note: If there are multiple values,", 
    "separate it by ','. Ex: 1,2,3,4 ",
    "=" * menu_width,
    '1. Appointment Date',
    '2. Appointment Time',
    '3. Appointment Status',
    '4. Cancel update'
]

bill_menu_lines = [
        f"Hello {staff_name.upper()}!",
        "=" * menu_width,
        " ",
        "Welcome to Patient Data Manager",
        " ",
        "=" * menu_width,
        " ",
        "BILL MENU",
        " ",
        "=" * menu_width,
        " ",
        "1 - Create bill",
        "2 - Check bill",
        "3 - Delete bill",
        "4 - Back to main menu",
        " "
    ]
treatment_menu_lines = [
        f"Hello {staff_name.upper()}!",
        "=" * menu_width,
        " ",
        "Welcome to Patient Data Manager",
        " ",
        "=" * menu_width,
        " ",
        "TREATMENT MENU",
        " ",
        "=" * menu_width,
        " ",
        "1 - Create new treatment",
        "2 - Check patient's treatment",
        "3 - Update patient's treatment",
        "4 - Delete patient's treatment",
        "5 - Back to main menu",
        " "
    ]
analytics_menu_lines = [
        f"Hello {staff_name.upper()}!",
        "=" * menu_width,
        " ",
        "Welcome to Patient Data Manager",
        " ",
        "=" * menu_width,
        " ",
        "ANALYTICS MENU",
        " ",
        "=" * menu_width,
        " ",
        "1 - Patient Demography",
        "2 - Bill & Payments",
        "3 - Appointments Statistics",
        "4 - Overview",
        "5 - Back to main menu",
        " "
    ]



def print_menu_line(sentence):
    print(f"║{sentence:^{menu_width}}║")

def main_menu(list_menu):

    menu_lines = list_menu

    # subprocess.run(["clear"])

    # Print the top border
    print("╔" + "═" * menu_width + "╗")
    
    for line in menu_lines:
        print_menu_line(line)
        
    print("╚" + "═" * menu_width + "╝")
    
    option = input("\nEnter your choice: ")
    return option
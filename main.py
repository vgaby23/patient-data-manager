# import conn.connection as connection
import subprocess

from config_dir import state
import func.analytics as an
import func.create as cr
import func.delete as de
import func.read as re
import func.update as up
from basic_func import main_menu
from database.execute import execute_all

MENU_WIDTH = 40

def print_menu_line(sentence):
    print(f"║{sentence:^{MENU_WIDTH}}║")

# Initiate database and table creation
# execute_all()

# Start Menu
staff_name = input("Hello, Welcome to Patient Data Manager! \nPlease input your name before proceeding: ")      

menu_lines = [
    f"Hello {staff_name.upper()}!",
    "=" * MENU_WIDTH,
    " ",
    "Welcome to Patient Data Manager",
    " ",
    "=" * MENU_WIDTH,
    " ",
    "Main Menu",
    " ",
    "=" * MENU_WIDTH,
    " ",
    "1 - Create new patient data",
    "2 - Find patient data",
    "3 - Update patient data",
    "4 - Delete patient data",
    "5 - Analytics",
    "6 - Exit",
    " "
]

user_choice = None
subprocess.run(["clear"])

user_choice = main_menu(menu_lines)

try:
    if user_choice == '1':
        first_name = input('Enter first name: ')
        last_name = input('Enter last name: ')
        gender = input('Enter gender (F/M): ')

    elif user_choice == '2':
        re.process()
    elif user_choice == 3:
        pass
    elif user_choice == 4:
        de.process(staff_name)
    elif user_choice == 5:
        pass
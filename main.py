import conn.connection as connection
import sys
import os

from config_dir import state
import func.analytics as an
import func.create as cr
import func.delete as de
import func.read as re
import func.update as up


MENU_WIDTH = 40

def print_menu_line(sentence):
    print(f"║{sentence:^{MENU_WIDTH}}║")

def main_menu(staff_name):

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
    os.system('clear')

    # 3. Print the top border
    print("╔" + "═" * MENU_WIDTH + "╗")
    
    # 4. Use a loop to print all the lines automatically
    for line in menu_lines:
        print_menu_line(line)
        
    # 5. Print the bottom border (Note: I removed an accidental extra ')' you had here)
    print("╚" + "═" * MENU_WIDTH + "╝")
    
    # 6. Return the chosen option so the rest of your program can use it
    option = int(input("\nEnter your choice: "))
    return option


staff_name = input("Hello, Welcome to Patient Data Manager! \nPlease input your name before proceeding: ")      

user_choice = None

while user_choice != 6:
    user_choice = main_menu(staff_name)

    if user_choice == 1:
        pass
    elif user_choice == 2:
        re.process()
    elif user_choice == 3:
        pass
    elif user_choice == 4:
        pass
    elif user_choice == 5:
        pass
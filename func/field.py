import os
import config


def print_menu_line(sentence):
    print(f"║{sentence:^{config.MENU_WIDTH}}║")

def mandatory_field(input_sentence):
    while True:
        input_field = input(f"Enter {input_sentence}: ").strip()

        if input_field:
            break
        else:
            print(f"Error: This field is mandatory. Please enter {input_sentence}")

    return input_field


def ask_data(process, limit = None):
    os.system('clear')

    print("\033[3mFill in patients data below\033[0m")

    # Mandatory Data Input
    print_menu_line('=')
    patient_first_name = mandatory_field("patient's first name")
    patient_last_name = mandatory_field("patient's last name")

    # Ask if user wants to see all data
    if process == 'read':
        limit = input('How many rows of data would you like to see?(write numbers or all): ')

    mandatory_data = {"patient_first_name":patient_first_name,
                        "patient_last_name":patient_last_name}

    return mandatory_data, limit
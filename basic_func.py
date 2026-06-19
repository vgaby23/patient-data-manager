import subprocess
import config

def print_menu_line(sentence):
    print(f"║{sentence:^{config.MENU_WIDTH}}║")

def main_menu(list_menu):

    menu_lines = list_menu

    subprocess.run(["clear"])

    # Print the top border
    print("╔" + "═" * config.MENU_WIDTH + "╗")
    
    for line in menu_lines:
        print_menu_line(line)
        
    print("╚" + "═" * config.MENU_WIDTH + "╝")
    
    option = input("\nEnter your choice: ")
    return option
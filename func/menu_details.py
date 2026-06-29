import config_dir.config as config

main_menu_lines = [
    f"Hello {config.STAFF_NAME.upper()}!",
    "=" * config.MENU_WIDTH,
    " ",
    "Welcome to Patient Data Manager",
    " ",
    "=" * config.MENU_WIDTH,
    " ",
    "Main Menu",
    " ",
    "=" * config.MENU_WIDTH,
    " ",
    "1 - Create new patient data",
    "2 - Find patient data",
    "3 - Update patient data",
    "4 - Delete patient data",
    "5 - Analytics",
    "6 - Exit",
    " "
]

delete_menu_lines = [
        f"Hello {config.STAFF_NAME.upper()}!",
        "=" * config.MENU_WIDTH,
        " ",
        "Welcome to Patient Data Manager",
        " ",
        "=" * config.MENU_WIDTH,
        " ",
        "How would you like to proceed?",
        " ",
        "=" * config.MENU_WIDTH,
        " ",
        "1 - Delete patient's data",
        "2 - Delete appointment data",
        "3 - Delete checkup bill",
        "4 - Delete treatment schedule",
        "5 - Back to main menu",
        " "
    ]

create_menu_lines = [
        f"Hello {config.STAFF_NAME.upper()}!",
        "=" * config.MENU_WIDTH,
        " ",
        "Welcome to Patient Data Manager",
        " ",
        "=" * config.MENU_WIDTH,
        " ",
        "How would you like to proceed?",
        " ",
        "=" * config.MENU_WIDTH,
        " ",
        "1 - Create patient data",
        "2 - Create appointment",
        "3 - Create checkup bill",
        "4 - Create treatment schedule",
        "5 - Back to main menu",
        " "
    ]

read_menu_lines = [
        f"Hello {config.STAFF_NAME.upper()}!",
        "=" * config.MENU_WIDTH,
        " ",
        "Welcome to Patient Data Manager",
        " ",
        "=" * config.MENU_WIDTH,
        " ",
        "How would you like to proceed?",
        " ",
        "=" * config.MENU_WIDTH,
        " ",
        "1 - Get patient's data",
        "2 - Get patient's appointment data",
        "3 - Get patient's checkup bill",
        "4 - Get patient's treatment schedule",
        "5 - Back to main menu",
        " "
    ]
update_menu_lines = [
        f"Hello {config.STAFF_NAME.upper()}!",
        "=" * config.MENU_WIDTH,
        " ",
        "Welcome to Patient Data Manager",
        " ",
        "=" * config.MENU_WIDTH,
        " ",
        "How would you like to proceed?",
        " ",
        "=" * config.MENU_WIDTH,
        " ",
        "1 - Update patient's data",
        "2 - Update patient's appointment data",
        "3 - Update patient's checkup bill",
        "4 - Update patient's treatment schedule",
        "5 - Back to main menu",
        " "
    ]
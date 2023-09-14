import re

def password_check():
    from main import starting_menu
    error_count = 4
    while error_count != 0:
        error_count = 4
        print()
        password = input("Input the password for your account. \n"
                         "Rules: \n"
                         "1) Minimum 8 symbols; \n"
                         "2) Minimum 1 number symbol \n"
                         "3) Minimum 1 special symbol \n"
                         "4) Minimum 1 uppercased letter\n"
                         "5) No spaces \n\n"
                         "Input your desired password:")
        password_repeat = input("Repeat the password you inputed: ")
        if password != password_repeat:
            print("Password don't coincide, repeat again")
            continue
        if len(password) >= 8:
            error_count -= 1
        else:
            print("Password is too short (must be at least 8 symbols)")
        if re.compile('[^A-Z]+'):
            error_count -= 1
        else:
            print("Password must contain at least one uppercased letter")
        if re.compile('[0-9]+'):
            error_count -= 1
        else:
            print("Password must contain at least 1 number")
        if not password.isalnum():
            error_count -= 1
        else:
            print("Password must contain at least 1 special symbol")
        if error_count == 0:
            print("Password was created successfully")
            return password
        choice = " "
        while choice not in ("ab"):
            choice = input("Password had some problems, do you want to proceed with creating a new password, or come back to main menu?\n\n"
                "a) Repeat password creation\n"
                "b) Come back to main menu\n")
        if choice == "a":
            continue
        if choice == "b":
            print("\n\nCancelling operation, coming back to main screen...\n")
            starting_menu()


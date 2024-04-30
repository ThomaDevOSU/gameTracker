import os

def main():
    print("Welcome to the Game Tracker!")
    directory = "accounts"
    file_name = "user_accounts.txt"
    file_path = os.path.join(directory, file_name)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.isfile(file_path):
        print("No user accounts found.")
        handle_no_accounts(file_path)
    else:
        user_data = login(file_path)
        if user_data:
            application_main(file_path, user_data)

def handle_no_accounts(file_path):
    print("Creating an account will allow you to personalize your application and keep track of your games!")
    action = input("Would you like to create an account (C) or quit (Q)? ").strip().upper()
    if action == 'C':
        create_account(file_path)
    elif action == 'Q':
        print("Exiting the application. Goodbye!")
    else:
        print("Invalid input. Exiting the application.")

def create_account(file_path):
    username = input("Enter a new username: ")
    password = input("Enter a new password: ")
    with open(file_path, 'a') as file:
        file.write(f"{username}:{password}\n")
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Account created successfully!")
    user_data = (username, password)
    application_main(file_path, user_data)

def login(file_path):
    attempts = 3
    while attempts > 0:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        with open(file_path, 'r') as file:
            for line in file:
                stored_username, stored_password = line.strip().split(':')
                if username == stored_username and password == stored_password:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("Login successful! Welcome to the Game Tracker.")
                    return (username, password)
        attempts -= 1
        print(f"Invalid username or password. You have {attempts} attempts remaining.")
    print("Too many failed login attempts. Exiting the application.")
    return None

def application_main(file_path, user_data):
    while True:
        print("Game Tracker: Track game progress using your account!")
        print("\nMain Application")
        print("1. Edit Account")
        print("2. Logout (Exit)")
        choice = input("Select an option: ")
        if choice == '1':
            os.system('cls' if os.name == 'nt' else 'clear')
            edit_account(file_path, user_data)
        elif choice == '2':
            print("Logging out. Goodbye!")
            break
        else:
            print("Invalid option, please choose again.")

def edit_account(file_path, user_data):
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        print("\nEdit Account")
        print("1. Change Username/Password")
        print("2. Logout (Exit)")
        print("3. Back")
        choice = input("Select an option: ")
        if choice == '1':
            print("Warning: The change will be permanent. Are you sure you would like to continue?")
            print("1. Yes")
            print("2. No")
            choice = input("Select an option: ")
            if choice == '1':
                change_credentials(file_path, user_data)
            elif choice == '2':
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Understood! Returning to Edit Account Menu")
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Invalid option, returning to Edit Account")
        elif choice == '2':
            print("Logging out. Goodbye!")
            exit()
            break
        elif choice == '3':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Returning to main menu")
            break
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Invalid option, please choose again.")

def change_credentials(file_path, user_data):
    os.system('cls' if os.name == 'nt' else 'clear')
    new_username = input("Enter your new username: ")
    new_password = input("Enter your new password: ")
    with open(file_path, 'r') as file:
        lines = file.readlines()
    with open(file_path, 'w') as file:
        for line in lines:
            stored_username, stored_password = line.strip().split(':')
            if stored_username == user_data[0] and stored_password == user_data[1]:
                file.write(f"{new_username}:{new_password}\n")
            else:
                file.write(line)
    print("Username and password changed successfully!")
    return (new_username, new_password)

if __name__ == "__main__":
    main()

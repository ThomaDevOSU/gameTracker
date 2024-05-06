import os
import time

# global games array
games = []
# global progress dictionary, game title as key, progress as array.
progress = {}

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
    clear()
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
                    clear()
                    print("Login successful! Welcome to the Game Tracker.")
                    return (username, password)
        attempts -= 1
        print(f"Invalid username or password. You have {attempts} attempts remaining.")
    print("Too many failed login attempts. Exiting the application.")
    return None

def application_main(file_path, user_data):
    load_data()
    while True:
        print("Game Tracker: Track game progress using your account!")
        print("\nMain Application")
        print("1. Add Game")
        print("2. Add Progress")
        print("3. Edit Account")
        print("4. Logout (Exit)")
        choice = input("Select an option: ")
        if choice == '1':
            game_adder()
        elif choice == '2':
            progress_adder()
        elif choice == '3':
            clear()
            edit_account(file_path, user_data)
        elif choice == '4':
            print("Logging out. Goodbye!")
            break
        else:
            print("Invalid option, please choose again.")

def progress_adder():
    clear()
    if(len(games) < 1):
        while(True):
            print("You have no games in your library! Would you like to add one?")
            print("[1] Yes")
            print("[2] No")
            res = input("Enter Here: ")
            if res == "1":
                game_adder()
                return
            if res == "2":
                clear()
                print("Understood! Returning to Main Menu")
                return
            else:
                clear()
                print("Incorrect Input, Try Again")
        
    print("Progress Adder: Add progress to your games!")
    while True:
        print("What game would you like to add progress to?")
        print("[Game Name] To manually find the game")
        print("[0] Return to Main Menu")
        for i in range(len(games)):
            print("[" + str(i+1) + "] " + games[i])
        res = input("Enter Here: ")
        if res == "0":
            clear()
            print("Understood! Returning to Previous Menu")
            return
        if not res.isdigit():
            found = False
            for item in games:
                if res == item:
                    print("Game Found!")
                    found = True
                    add_progress(res)
                    break
            if not found:
                print("The Game " + res + " could not be found in the library")
        elif int(res) <= len(games) and int(res) > 0:
            add_progress(games[int(res)-1])
        else:
            clear()
            print("Incorrect Input, Try again")

        
def add_progress(game : str):
    while True:
        print("What progress would you like to add to " + game + "?")
        print("[0] Back")
        print("[Enter Progress Made] Logs progress for this game")
        res = input("Enter Here: ")
        if res == "0":
            clear()
            print("Understood! Returning to Previous Menu")
            return
        while True:
                print("Are you sure?")
                print("[1] Yes")
                print("[2] No")
                res2 = input("Enter Here: ")
                if res2 == "1":
                    print("Adding progress to game...")
                    progress[game].append(res)
                    save_data()
                    break
                elif res2 == "2":
                    clear()
                    print("Understood!")
                    break
                else:
                    clear()
                    print("Incorrect answer, try again")

def game_adder():
    clear()
    while True:
        print("What game would you like to add?")
        print("[Game Name] adds game to library")
        print("[0] Cancel")
        res = input("Enter Here: ")
        
        if res == "0":
            clear()
            print("Returning to Main Menu!")
            return

        canAdd = True

        if res.isdigit():
            clear()
            print("We apologize, We do not support Games with only digits as a name")
            canAdd = False
            
        for item in games:
            if res == item:
                print("That game already exists in your library!")
                canAdd = False
                break

        # It was not in the list
        while True and canAdd:
            print("Are you sure?")
            print("[1] Yes")
            print("[2] No")
            res2 = input("Enter Here: ")
            clear()
            if res2 == "1":
                print("Saving " + res + " to library!")
                games.append(res)
                progress[res] = []
                save_data()
                break
            elif res2 == "2":
                print("Understood!")
                break
            else:
                print("Incorrect answer, try again")

def save_data():
    #command to save what games we have
    print("Saving games...")
    commandFile("1", games)
    #confirmation to save what games we have
    waitForResponse("-1")
    #command to save what progress we have
    print("Saving game progress...")
    commandFile("2", progress)
    #confirmation to save what progress we have
    waitForResponse("-1")

def load_data():
    print("Loading games...")
    #command to load what games we have
    commandFile("3")
    #confirmation to load what games we have
    waitForResponse("-2")
    #command to load what progress we have
    print("Loading game progress...")
    commandFile("4")
    #confirmation to load what progress we have
    waitForResponse("-3")

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def edit_account(file_path, user_data):
    clear()
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
                clear()
                print("Understood! Returning to Edit Account Menu")
            else:
                clear()
                print("Invalid option, returning to Edit Account")
        elif choice == '2':
            print("Logging out. Goodbye!")
            exit()
            break
        elif choice == '3':
            clear()
            print("Returning to main menu")
            break
        else:
            clear()
            print("Invalid option, please choose again.")

def change_credentials(file_path, user_data):
    clear()
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

def commandFile(x, y = None):
    x=str(x)
    with open("cmd.txt", 'w') as file:
        file.write(x)
    if y is not None:
        if type(y) == list:
            with open("action.txt", 'w') as file:
                for item in y:
                    file.write(str(item) + "\n")
            return
        elif type(y) == dict: 
            with open("action.txt", 'w') as file:
                for key in y.keys():
                    file.write(str(key))
                    for item in y[key]:
                        file.write(":")
                        file.write(item)
                    file.write("\n")
        else:
            with open("action.txt", 'w') as file:
                file.write(y)

def waitForResponse(x):
    x=str(x)
    res = None
    while True:
        with open("cmd.txt", "r") as file:
            res = file.read()
        time.sleep(0.2)
        # basic response, action completed
        if res == "-1":
            print("Action complete!")
            commandFile(0)
            return
        # games loaded
        elif res == "-2":
            with open("action.txt", "r") as file:
                lines = file.readlines()
            for line in lines:
                    games.append(line.strip())
            if len(games) > 0:
                print("Games loaded!")
            commandFile(0)
            return
        # progress loaded
        elif res == "-3":
            with open("action.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    gp = line.strip().split(':')
                    progress[gp[0]] = []
                    for i in range(1, len(gp)):
                        progress[gp[0]].append(gp[i])
            if len(progress) > 0:
                print("Progress loaded!")
            commandFile(0)
            return
            
        


if __name__ == "__main__":
    main()

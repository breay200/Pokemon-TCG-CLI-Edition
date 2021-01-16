import json
import os, os.path
import random
from datetime import date
import socket
import select
import errno
import sys
import time
import pickle

#FUNCTIONS START

#CLIENT SERVER
def clientSocket(username, server_info):
    #ROCK PAPER SCISSORS INPUT AND VERIFICATION
    def rockPaperScissors():
        choice = str(input("To decide who flips the coin, we must play 'rock, paper, scissors'\n(enter one of the following rock, paper, or scissors): ")).lower()
        while choice not in ('rock', 'paper', 'scissors'):
            choice = str(input("Please enter a valid choice: "))
        return choice
    

    #ENCODE DATA IN UTF-8 AND SEND
    def encodeAndSend(variable):
        variable = variable.encode('utf-8')
        variable_header = f"{len(variable):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(variable_header+variable)
        return


    #RECEIVE DATA FROM SERVER
    def receiveData():
        try: 
            while True:
                #time.sleep(3)
                data_header = client_socket.recv(HEADER_LENGTH)
                data_length = int(data_header.decode('utf-8').strip())
                data = client_socket.recv(data_length).decode('utf-8')
                
                if len(data) >= len(data_length):
                    break


        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error', str(e))
                sys.exit()
        
        except Exception as e:
            print('General error',str(e))
            sys.exit()
        
        return data


    #COMPARE ROCK PAPER SCISSOR RESULTS
    def compareRockPaperScissors(your_choice, their_choice):
        
        while your_choice == their_choice:
            print("\nyou and the opponent both chose the same, try again: ")
            your_choice = rockPaperScissors()
            encodeAndSend(your_choice)
            their_choice = receiveData()
        
        if your_choice == 'rock' and their_choice == 'scissors':
            print(f"\nrock beats scissors, {username} gets to choose.")
        elif your_choice == 'paper' and their_choice == 'rock':
            print(f"\npaper beats rock, {username} gets to choose.")
        elif your_choice == 'scissors' and their_choice == 'paper':
            print(f"\nscissors beats paper, {username} gets to choose.")
        elif your_choice == 'scissors' and their_choice =='rock':
            print("\nrock beats scissors, opponent gets to choose.")
        elif your_choice == 'rock' and their_choice == 'paper':
            print("\npaper beats rock, opponent gets to choose.")
        elif your_choice == 'paper' and their_choice == 'scissors':
            print("\nscissors beats paper, opponent gets to choose")
        
        return


    HEADER_LENGTH = 10
    #IP = "127.0.0.1"
    #PORT = 8080
    server_info = tuple(server_info)

    encoded_username = username.encode('utf-8')
    username_header = f"{len(encoded_username):<{HEADER_LENGTH}}".encode('utf-8')

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #client_socket.connect((IP, PORT))
    client_socket.connect(server_info)
    client_socket.setblocking(False)

    client_socket.send(username_header + encoded_username)

    while True:
        #THE ACTUAL GAMEPLAY OCCURS IN THIS WHILE LOOP
        your_choice = rockPaperScissors()
        encodeAndSend(your_choice)
        their_choice = receiveData()
        compareRockPaperScissors(your_choice, their_choice)
        break


#ADD CARDS TO DATABASE - DICTIONARY
def addToDatabase(no_cards_adding):
    for i in range(no_cards_adding):
        card_database[i] = {}
        card_type = str(input("Enter card type: "))
        card_database[i]['card_type'] = card_type
        #print(card_database)

        if card_type == 'pokemon':
            def binaryValidation(variable, string):
                variable = str(input(string)).lower()
                while variable not in ('yes', 'y', 'no', 'n'):
                    variable = str(input(string)).lower()
                return variable


            def stringValidation(variable, string, error_string, while_comparison):
                variable = str(input(string)).lower()
                while variable not in (while_comparison):
                    variable = str(input(error_string)).lower()
                return variable


            energy_type = ""
            energy_type_string = "Enter the pokemon's energy type: "
            while_comparison_energy_type = "'grass', 'fire', 'water', 'lightning', 'fighting', 'psychic', 'normal', 'colorless', 'colourless', 'darkness', 'metal', 'dragon', 'fairy', 'none'"
            energy_type_error_string = "Enter a valid energy type (" + while_comparison_energy_type + "): "
            energy_type = stringValidation(energy_type, energy_type_string, energy_type_error_string, while_comparison_energy_type)
            card_database[i]['type'] = energy_type

            card_database[i]['name'] = str(input("Enter the pokemon's name: ")).lower()
            
            level = ""
            while_comparison_level = "'basic', 'stage 1', 'stage 2'"
            level_string = "Enter the pokemon's level (basic, stage 1 or stage 2): "
            level_error_string = "Enter a valid level (basic, stage 1 or stage 2: "
            level = stringValidation(level, level_string, level_error_string, while_comparison_level)
            card_database[i]['level'] = level

            card_database[i]['health'] = int(input("Enter the pokemon's health: "))

            weakness = ""
            weakness_string = "Enter the pokemon's weakness ('none' if there isn't one): "
            weakness = stringValidation(weakness, weakness_string, energy_type_error_string, while_comparison_energy_type)
            card_database[i]['weakness'] = weakness

            resistance = ""
            resistance_string = "Enter the pokemon's resistance ('none' if there isn't one): "
            resistance = stringValidation(resistance, resistance_string, energy_type_error_string, while_comparison_energy_type)
            card_database[i]['resistance'] = resistance

            card_database[i]['retreat_cost'] = int(input("Enter retreat cost (enter 0 if there isn't one): "))

            is_gx_string = "Enter 'yes' if pokemon is GX or 'no' if not: "
            is_gx = ""

            is_gx = binaryValidation(is_gx, is_gx_string)

            card_database[i]['is_gx'] = is_gx
            
            has_passive_string = "Enter 'yes' if the pokemon has a passive ability, and 'no' if it does not: "
            has_passive = ""

            has_passive = binaryValidation(has_passive, has_passive_string)

            if (has_passive == 'yes') or (has_passive == 'y'):
                card_database[i]['passive_name'] = str(input("Enter the passive's name (if there is none type 'none'): ")).lower()
                card_database[i]['passive_description'] = str(input("""Enter the passive's description: """))

            no_moves = int(input("How many moves does the pokemon have? "))
            card_database[i]['no_moves'] = no_moves

            for x in range(no_moves):
                
                def basicAbilityReq():
                    card_database[i][ability_name] = str(input(f"Enter ability {num} name: ")).lower()
                    card_database[i][ability_no_energy] = int(input(f"Enter number of required energies for ability {num} (1, 2, 3...): "))
                    card_database[i][ability_energy_req_type] = str(input(f"Enter ability {num} energy requirement (1 fire, 2 water, 3 grass... if normal type none): ")).lower()


                num = x + 1
                ability_name = "ability_" + str(num) + "_name"
                ability_damage = "ability_" + str(num) + "_damage"
                ability_no_energy = "ability_" + str(num) + "_no_energy"
                ability_energy_req_type = "ability_" + str(num) + "_energy_req_type"
                ability_passive_desc = "ability_" + str(num) + "_passive_desc"
                
                has_passive = str(input(f"Does ability {num} have a passive? (answer with 'yes' or 'no') "))
                deals_damage = str(input(f"Does ability {num} deal damage? (answer with 'yes' or 'no') "))

                if has_passive == 'yes' and deals_damage == 'yes':
                    basicAbilityReq()
                    card_database[i][ability_passive_desc] = str(input(f"Enter passive description for ability {num}: "))
                    card_database[i][ability_damage] = int(input(f"Enter ability {num} damage: "))
                elif has_passive == 'yes' and deals_damage == 'no':
                    basicAbilityReq()
                    card_database[i][ability_passive_desc] = str(input(f"Enter passive description for ability {num}: "))
                else:
                    basicAbilityReq()
                    card_database[i][ability_damage] = int(input(f"Enter ability {num} damage: "))
        
        elif card_type == 'trainer':
            trainer_type = str(input("Enter either 'item', 'supporter' or 'stadium': ")).lower()
            
            while trainer_type not in ('item', 'supporter', 'stadium'):
                trainer_type = str(input("Enter a valid trainer card type (item, supporter or stadium): ")).lower()
            
            card_database[i]['type'] = trainer_type
            card_database[i]['name'] = str(input("Enter name of trainer card: ")).lower()
            card_database[i]['action'] = str(input("Enter the card's description: "))

        else:
            energy_types = "'grass', 'fire', 'water', 'lightning', 'fighting', 'psychic', 'normal', 'colorless', 'colourless', 'darkness', 'metal', 'dragon', 'fairy'"
            energy_type = str(input("Enter energy type: "))
            
            while energy_type not in (energy_types):
                energy_type = str(input(f"Enter a valid energy type ({energy_types})")).lower()

            card_database[i]['type'] = energy_type


#WRITE DICTIONARY TO FILE WITH JSON
def dictToFile(dictionary, path, filename, string):
    global json
    #scriptpath = os.path.dirname(__file__)
    #filename = os.path.join(scriptpath, filename)
    path = path
    save_path = path + "/" + filename
    f = open(save_path, "w")
    f.write(json.dumps(dictionary))
    f.close()
    print(string)


#LOAD JSON FILE AND RECONSTRUCT AS DICTIONARY
def loadFromDict(file_path):
    with open(file_path) as f: 
        data = f.read()
    dictionary = json.loads(data)
    return dictionary
    #print("Data type after reconstruction : ", type(loaded_cards))


def deleteAFile(file):
    os.remove(file)
    print(f"\n{file} has been deleted!")


#VIEW DECK OPTION 
def manageGameOptions():
    def inputDecision():
        decision = str(input("\nEnter 'v' to view your deck, 's' to save your deck to file, 'l' to load your deck from a file, 'd' to delete a save file, 'r' to return to the main menu: ")).lower()
        while decision not in ('v', 's', 'l', 'r', 'd'):
            decision = validInput(decision)
        return decision.lower()


    def validInput(decision):
        decision = str(input("\nPlease enter a valid input (enter 'h' for help): ")).lower()
        if decision == "h":
            print("\nEnter 'v' to view your deck, 's' to save your deck to file, 'l' to load your deck from a file, 'd' to delete a save file, or 'r' to return to the main menu: ")
        return decision.lower()


    def loadADeck():
        global deck_in_use
        print("\nAvailable Save Files: \n")
        path = "save_files/decks"
        files = listFiles(path)
        
        printDecks(files)
        selection = input("\nType the name of the deck you would like to load: ")

        while selection not in files:
            selection = str(input("\nEnter the name of a valid deck: (enter 'v' to view options again) "))
            if selection == 'v':
                printDecks(files)
        
        filename = path + "/" + selection
        deck_in_use = loadFromDict(filename)


    def deleteADeck():
        path = "save_files/decks"
        files = listFiles(path)
        print("Available files: \n")
        printDecks(files)
        selection = str(input("\nEnter the name of a valid deck: (enter 'v' to view options again) "))
        
        while selection not in files:
            selection = str(input("\nEnter the name of a valid deck: (enter 'v' to view options again) "))
            if selection == 'v':
                printDecks(files)
        
        selection = path + "/" + selection

        deleteAFile(selection)

    
    def printDecks(files):
        for f in files:
            print(f)


    def listFiles(path):
        return os.listdir(path)
    

    print("\n------- GAME OPTIONS MENU -------")

    decision = inputDecision().lower()

    while decision != 'r':
        if decision == 'v':
            pass
        elif decision == 's':
            #today = date.today()
            #dateStr = today.strftime("%d-%m-%Y")
            #filename = str(username + "-"  + dateStr + ".json")
            #print(filename)
            #dictToFile(cards, filename)
            pass
        elif decision == 'l':
            loadADeck()
            print(deck_in_use)
        elif decision == 'd':
            deleteADeck()
        
        decision = inputDecision().lower()


#WRITE DATA TO FILE, WORKS FOR LISTS ATM
def txtToFile(path, data):
    #COULD ADD IF TYPE(DATA) IS LIST THEN ... THEREFORE WE CAN HANDLE MULTIPLE DATA TYPES
    with open(path, 'wb') as filehandle:
        pickle.dump(data, filehandle)
    print("\nFinished saving data!")


#LOADS LIST FROM FILE, RETURNS LIST
def loadFromTxt(path):
    with open(path, 'rb') as filehandle:
        data = pickle.load(filehandle)
    return data


def manageConfiguration():
    def updateToFile():
            IP = str(input("Please enter the IP address of the server: (e.g. 127.0.0.1 if using loopback) "))
            PORT = int(input("Please enter the port on the server that you would like to connect to: (use lesser known ports, e.g. 8080, 1234) "))
            print(f"\nWhen starting a new match, your computer will attempt to port {PORT} on {IP}.\nWriting this information to file...")
            networkList = [IP, PORT]
            path = config_path + "/server_settings"
            txtToFile(path, networkList)


    print("\n------- NETWORK CONFIGURATION MENU -------\n")

    today = date.today()

    if 'date_joined' not in user_account_dictionary:
        print("\nIf you haven't set-up an account, please still configure network settings.")
    elif user_account_dictionary['date_joined'] == today.strftime("%d-%m-%Y"):
        print("\nIf this is your first time playing, please configure network settings.")
    
    config_path = "save_files/network_config"
    existing_config = os.listdir(config_path)

    decision = str(input("\nEnter 'c' to configure network, or 'r' to return home: ")).lower()

    while decision != 'r':
        if decision == 'c':
            if existing_config:
                ask_edit = str(input("\nWould you like to update the network configuration? ('y' for yes, 'n' for no) ")).lower()
                if ask_edit == 'y':
                    updateToFile()
            else:
                ask_edit = str(input("\nWould you like to update the network configuration? ('y' for yes, 'n' for no) ")).lower()
                if ask_edit == 'y':
                    updateToFile()
                else:
                    print(f"\n{username.title()}, you won't be able to play if you do not configure the settings.")
        decision = str(input("Enter 'c' to configure network, or 'r' to return home: ")).lower()
    

def selectionScreen():
    def menuSelection():
        selection = str(input(f"\n{username.title()}, please enter 's' to start a new battle, 'm' to manage game options (deck, etc.), 'c' to configure settings, or 'e' to exit: ")).lower()

        while selection not in ('s', 'm', 'c', 'e'):
            selection = str(input(f"\n{username.upper()}, please enter a valid option (enter 'h' for help): ")).lower()
            if selection == 'h':
                print(("Enter 's' to start a new battle, 'm' to manage game options (deck, etc.), 'c' to configure settings, or 'e' to exit: ")).lower()
        
        return selection
    

    selection = menuSelection().lower()

    while True:
        if selection == 's':
            path = "save_files/network_config/server_settings"
            server_info = []
            
            while server_info == []:
                try:
                    server_info = loadFromTxt(path)
                except FileNotFoundError:
                    print("\nYou must configure server settings prior to playing.")
                    manageConfiguration()

            clientSocket(username, server_info)

        elif selection == 'm':
            manageGameOptions()
        elif selection == 'c':
            manageConfiguration()
        elif selection == 'e':
            print("\nExiting the program...")
            quit()
        
        selection = menuSelection()
        

def startBattle():
    coin_toss = str(input(f"\n{username}, please select heads or tails: "))
    coin_toss.lower()
    #IT WORKS
    while coin_toss not in ('heads', 'h', 'tails', 't'):
        coin_toss = str(input(f"{username}, please enter either 'head' or 'tails: "))

    coin_toss.lower()

    if (coin_toss == 't'):
        coin_toss = "tails"
    elif (coin_toss == 'h'):
        coin_toss = "heads"
    else:
        pass

    random_coin_choice = random.choice(coin_sides)

    print(f"\nflipping the coin... \n{random_coin_choice}!")

    if (coin_toss == "heads") and (random_coin_choice == "heads"):
        decision = str(input("\nWould you like to go first or second? "))

        while decision not in ('first', '1', '1st', 'second', '2', '2nd'):
            decision = str(input("\nPlease enter a valid input, 'first' or 'second': "))

        print(f"\nyou decided to go {decision}")


def createLocalUserAccount(user_save_path):
    print("\n------- ACCOUNT CREATION -------\n")
    fav_pokemon = str(input("What's your favourite Pokemon? ")).lower()
    fav_type = str(input("What's your favourite energy type? ")).lower()
    today = date.today()
    dateStr = today.strftime("%d-%m-%Y")

    if fav_type == 'water':
        print(f"\n{fav_type}... good choice\n")
    
    user_account_dictionary['fav_pokemon'] = fav_pokemon
    user_account_dictionary['fav_type'] = fav_type
    user_account_dictionary['date_joined'] = dateStr
    user_account_dictionary['no_wins'] = 0
    user_account_dictionary['no_losses'] = 0

    message = "File has successfully been created!\nAccount creation completed."
    dictToFile(user_account_dictionary, user_save_path, username, message)
    #print(f"Completed account creation: {user_account_dictionary}")


def checkIfAccount():
    global user_account_dictionary
    user_save_path = "save_files/users"
    saved_user_accounts = os.listdir(user_save_path)

    if username not in saved_user_accounts:
        choice = str(input(f"\nThere doesn't seems to be any account associated with the username: {username.title()}. \nWould you like to set one up? (enter 'y' for yes or 'n' for no) " ))
        if choice == 'y':
            createLocalUserAccount(user_save_path)
        else:
            user_account_dictionary['username'] = username
            print(f"That's okay {username}, we respect your privacy.")
    elif username in saved_user_accounts:
        file_path = user_save_path + "/" + username
        user_account_dictionary = loadFromDict(file_path)
        print("\nYour save data has been loaded from file!")


#FUNCTIONS END

#VARIABLES START
card_database = {}
user_account_dictionary = {}
deck_in_use = {}
coin_sides = ["heads", "tails"]
##VARIABLES END

#PROGRAM STARTS HERE
print("\nWelcome to Pokemon TCG Cli Edition!\n")

username = str(input("Please enter your username: ")).lower()

checkIfAccount()
     
print(f"\n{username.title()}, please ensure that you have network settings configured before entering a battle.\n")

if 'fav_pokemon' in user_account_dictionary:
   print(f"It's what {user_account_dictionary.get('fav_pokemon')} would have wanted...")

selectionScreen()
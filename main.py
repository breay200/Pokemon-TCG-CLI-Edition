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

    def pickleDumpAndSend(variable):
        variable = pickle.dumps(variable)
        variable_header = bytes(f'{len(variable):<{HEADER_LENGTH}}', "utf-8")
        client_socket.send(variable_header+variable)
        return

    def receiveData():
        try:
            while True:
                #time.sleep(3)
                data_header = client_socket.recv(HEADER_LENGTH)
                data_length = int(float(data_header.decode('utf-8').strip()))
                data = client_socket.recv(data_length).decode('utf-8')
                if data:
                    break

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error', str(e))
                sys.exit()
        
        except Exception as e:
            print('General error',str(e))
            sys.exit()
        
        return data

    #RECEIVE DATA FROM SERVER
    def receivePickleData():
        try:
            while True:
                #time.sleep(3)
                data_header = client_socket.recv(HEADER_LENGTH)
                data_length = int(float(data_header.decode('utf-8').strip()))
                data = client_socket.recv(data_length)
                data = pickle.loads(data)
                if data:
                    break

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error', str(e))
                sys.exit()
        
        except Exception as e:
            print('General error',str(e))
            sys.exit()
        
        return data


    def attack():
        def decideMove():
            no_moves = active_pokemon.get('no_moves')
            options = ['retreat', 'end turn']

            for x in range(no_moves):
                print(f"\nEnter {active_pokemon.get(f'ability_{x}_name')} if you choose this ability: ")
                options.append(active_pokemon.get(f'ability_{x}_name'))

            print(f"\nEnter 'retreat' if you want to retreat the active pokemon: ")
            print(f"\nEnter 'end turn' if you cannot attack and want to end your turn: ")
            decision = str(input(f"\nPlease choose one the following options ({options})"))
            decision = stringValidation(decision, options)
            options.clear()
            return decision
        
        def attackEnemy(decision):
            no_moves = active_pokemon.get('no_moves')
            for x in range(no_moves):
                if decision == active_pokemon.get(f'ability_{x}_name'):
                    opponent_health = int(opponents_active_pokemon.get('health'))
                    opponents_active_pokemon['health'] = opponent_health - int(active_pokemon.get(f'ability_{x}_damage'))
                    print(f"\nYou attacked {opponents_active_pokemon.get('name').title()} for {active_pokemon.get(f'ability_{x}_damage')} damage...")
                    
                    if opponents_active_pokemon.get('health') > 0:
                        print(f"\nNow {opponents_active_pokemon.get('name').title()} has only {opponents_active_pokemon.get('health')}HP!")
                    else:
                        print(f"\nWOW... {active_pokemon.get('name').title()} knocked out {opponents_active_pokemon.get('name').title()}!")
                        print(f"\nYou get to draw a prize card!")
                        your_hand = takePrizeCard(your_hand)
            return active_pokemon, benched_pokemon, opponents_active_pokemon, opponents_benched_pokemon, prize_deck, your_hand

        global active_pokemon
        global benched_pokemon
        global opponents_active_pokemon
        global opponents_benched_pokemon
        global your_hand
        global prize_deck

        options = ['y', 'n']
        decision = str(input(f"\nDo you want to attack the enemy's {opponents_active_pokemon.get('name')}? (enter 'y' or 'n') "))
        decision = stringValidation(decision, options)

        if decision == 'y':
            
            viewActivePokemon()
            while True:
                decision = decideMove()
                no_moves = active_pokemon.get('no_moves')

                for x in range(no_moves):
                    if decision == active_pokemon.get(f'ability_{x}_name'):
                        if int(active_pokemon.get('no_attached_energy')) >= int(active_pokemon.get(f'ability_{x}_no_energy')):
                            active_pokemon, benched_pokemon, opponents_active_pokemon, opponents_benched_pokemon, prize_deck, your_hand = attackEnemy(decision)
                            return active_pokemon, benched_pokemon, opponents_active_pokemon, opponents_benched_pokemon, prize_deck, your_hand
                        elif int(active_pokemon.get('no_attached_energy')) < int(active_pokemon.get(f'ability_{x}_no_energy')):
                            print("\nYou don't have enough energy cards for this attack")
                            decision = decideMove()
            
                if decision == 'retreat':
                    if active_pokemon.get('retreat_cost').lower() == 'none' or active_pokemon.get('retreat_cost').lower() == 0:
                        playable_pokemon = []
                        print("\nSelect one of the following pokemon to make the new active pokemon: ")
                        
                        for key in benched_pokemon:
                            print(f"\n{key}) {benched_pokemon.get('name').title()}")
                            playable_pokemon.append(benched_pokemon[key].get('name'))
                        
                        decision = str(input(f"\nEnter the name of the currently benched pokemon that you want to make the active ({playable_pokemon}): "))
                        decision = stringValidation(decision, playable_pokemon)

                        x = len(benched_pokemon) + 1
                        benched_pokemon[x] = active_pokemon
                        active_pokemon = {}

                        for x in benched_pokemon:
                            x = str(x)
                            if decision == benched_pokemon[x].get('name'):
                                for key, value in benched_pokemon[x]:
                                    active_pokemon[key] = value
                                del benched_pokemon[key]
                                break
                        
                        print(f"\n{active_pokemon.get('name').title()} is now the active pokemon")
                        print(f"\n{decision.title()} has been returned to the bench")
                        decision = decideMove()

                    elif active_pokemon.get('no_attached_energy') < active_pokemon.get('retreat_cost'):
                        print(f"\nYou do not have enough energy cards to retreat {active_pokemon.get('name').title()} ")
                        decision = decideMove()

                    elif decision == 'end turn':
                        print("\nEnding your turn...")
                        return active_pokemon, benched_pokemon, opponents_active_pokemon, opponents_benched_pokemon, prize_deck, your_hand
        
        else:
            print("\nYou chose not to attack this turn")
            return active_pokemon, benched_pokemon, opponents_active_pokemon, opponents_benched_pokemon, prize_deck, your_hand

    #COMPARE ROCK PAPER SCISSOR RESULTS
    def compareRockPaperScissors(your_choice, their_choice):
        while your_choice == their_choice:
            print("\nyou and the opponent both chose the same, try again: ")
            your_choice = rockPaperScissors()
            encodeAndSend(your_choice)
            their_choice = receiveData()
        
        if your_choice == 'rock' and their_choice == 'scissors':
            print(f"\nrock beats scissors, {username} gets to choose.")
            answer = flipCoin()
            time.sleep(3)
            encodeAndSend(answer)
            return answer
        elif your_choice == 'paper' and their_choice == 'rock':
            print(f"\npaper beats rock, {username} gets to choose.")
            answer = flipCoin()
            time.sleep(3)
            encodeAndSend(answer)
            return answer
        elif your_choice == 'scissors' and their_choice == 'paper':
            print(f"\nscissors beats paper, {username} gets to choose.")
            answer = flipCoin()
            time.sleep(3)
            encodeAndSend(answer)
            return answer
        elif your_choice == 'scissors' and their_choice =='rock':
            print(f"\nrock beats scissors, {opponent_username} gets to choose.")
            answer = receiveData()
            if answer == 'first':
                my_answer = 'second'
            else:
                my_answer == 'first'
            return my_answer
        elif your_choice == 'rock' and their_choice == 'paper':
            print(f"\npaper beats rock, {opponent_username} gets to choose.")
            answer = receiveData()
            if answer == 'first':
                my_answer = 'second'
            else:
                my_answer == 'first'
            return my_answer
        elif your_choice == 'paper' and their_choice == 'scissors':
            print(f"\nscissors beats paper, {opponent_username} gets to choose")
            answer = receiveData()
            if answer == 'first':
                my_answer = 'second'
            else:
                my_answer == 'first'
            return my_answer

    global prize_deck
    global your_hand
    global deck_in_use
    global active_pokemon
    global benched_pokemon
    global opponents_active_pokemon
    global opponents_benched_pokemon
    global user_account_dictionary

    your_hand = []
    active_pokemon = {}
    benched_pokemon = {}
    opponents_active_pokemon = {}
    opponents_benched_pokemon = {}
    global HEADER_LENGTH
    HEADER_LENGTH = 1024
    #IP = "127.0.0.1"
    #PORT = 8080
    server_info = tuple(server_info)

    encoded_username = username.encode('utf-8')
    username_header = f"{len(encoded_username):<{HEADER_LENGTH}}".encode('utf-8')

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #client_socket.connect((IP, PORT))
    client_socket.connect(server_info)
    #client_socket.setblocking(False)

    client_socket.send(username_header + encoded_username)

    while True:
        #THE ACTUAL GAMEPLAY OCCURS IN THIS WHILE LOOP
        time.sleep(2)
        encodeAndSend(username)
        opponent_username = receiveData()
        print(f"{opponent_username} has connected")

        your_choice = rockPaperScissors()
        encodeAndSend(your_choice)

        their_choice = receiveData()
        answer = compareRockPaperScissors(your_choice, their_choice)

        random.shuffle(deck_in_use)
        prize_deck = removePrizeCardFromDeck(5, deck_in_use)
        your_hand = drawCard(7, deck_in_use)

        if answer == 'first':
            #START YOUR TURN
            your_hand = drawCard(1, deck_in_use)
            playPokemon()
            addEnergy()
            #SEND DATA TO OTHER USER
            pickleDumpAndSend(active_pokemon)
            pickleDumpAndSend(benched_pokemon)
        elif answer == 'second':
            #RECEIVE DATA FROM OTHER USER
            opponents_active_pokemon = receivePickleData()
            opponents_benched_pokemon = receivePickleData()
            #START YOUR TURN
            your_hand = drawCard(1, deck_in_use)
            playPokemon()
            addEnergy()
            active_pokemon, benched_pokemon, opponents_active_pokemon, opponents_benched_pokemon, prize_deck, your_hand = attack()
            #SEND DATA TO OTHER USER
            pickleDumpAndSend(active_pokemon)
            pickleDumpAndSend(benched_pokemon)
            pickleDumpAndSend(opponents_active_pokemon)
            pickleDumpAndSend(opponents_benched_pokemon)
            pickleDumpAndSend(len(prize_deck))

        if answer == 'first':
            #RECEIVE DATA FROM OTHER USER
            opponents_active_pokemon = receivePickleData()
            opponents_benched_pokemon = receivePickleData()
            active_pokemon = receivePickleData()
            benched_pokemon = receivePickleData()
            opponents_no_prize_cards = receivePickleData()
        
        while True:
            if answer == 'first':
                #START YOUR TURN
                your_hand = drawCard(1, deck_in_use)
                
                if not active_pokemon:
                    playPokemon()
                
                addEnergy()
                active_pokemon, benched_pokemon, opponents_active_pokemon, opponents_benched_pokemon, prize_deck, your_hand = attack()
                #SEND DATA TO OTHER USER
                pickleDumpAndSend(active_pokemon)
                pickleDumpAndSend(benched_pokemon)
                pickleDumpAndSend(opponents_active_pokemon)
                pickleDumpAndSend(opponents_benched_pokemon)
                pickleDumpAndSend(len(prize_deck))
                if len(prize_deck) < 1:
                    print("\nYOU WIN! CONGRATULATIONS")
                    user_account_dictionary['no_wins'] += 1
                    return
            elif answer == 'second':
                #RECEIVE DATA FROM OTHER USER
                opponents_active_pokemon = receivePickleData()
                opponents_benched_pokemon = receivePickleData()
                active_pokemon = receivePickleData()
                benched_pokemon = receivePickleData()
                opponents_no_prize_cards = receivePickleData()
                if opponents_no_prize_cards < 1:
                    print("\nYOU LOST... MAYBE NEXT TIME")
                    user_account_dictionary['no_losses'] -= 1
                    return
                #START YOUR TURN
                your_hand = drawCard(1, deck_in_use)
                if not active_pokemon:
                    playPokemon()
                addEnergy()
                attack()
                #SEND DATA TO OTHER USER
                pickleDumpAndSend(active_pokemon)
                pickleDumpAndSend(benched_pokemon)
                pickleDumpAndSend(opponents_active_pokemon)
                pickleDumpAndSend(opponents_benched_pokemon)
                pickleDumpAndSend(len(prize_deck))
                if len(prize_deck) < 1:
                    print("\nYOU WIN! CONGRATULATIONS!")
                    user_account_dictionary['no_wins'] += 1
                    return
            
            if answer == 'first':
                opponents_active_pokemon = receivePickleData()
                opponents_benched_pokemon = receivePickleData()
                active_pokemon = receivePickleData()
                benched_pokemon = receivePickleData()
                opponents_no_prize_cards = receivePickleData()
                if opponents_no_prize_cards < 1:
                    print("\nYOU LOST... MAYBE NEXT TIME")
                    user_account_dictionary['no_losses'] -= 1
                    return
        
        client_socket.close()


        
        


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
            while_comparison_energy_type = "'grass', 'fire', 'water', 'electric', 'fighting', 'psychic', 'normal', 'dark', 'steel', 'dragon', 'fairy'"
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
                    return


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
        
        return


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
    return


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
    return


#VIEW DECK OPTION 
def manageGameOptions():
    def inputDecision():
        decision = str(input("\nEnter 'a' to add cards to the database, 'v' to view your deck, 's' to save progress to your user account,  'l' to load your deck from a file, 'd' to delete a save file, 'r' to return to the main menu: ")).lower()
        while decision not in ('a', 'v', 's', 'l', 'r', 'd'):
            decision = validInput(decision)
        return decision.lower()


    def validInput(decision):
        decision = str(input("\nPlease enter a valid input (enter 'h' for help): ")).lower()
        if decision == "h":
            print("\nEnter 'a' to add cards to the database, 'v' to view your deck, 's' to save progress to your user account, 'l' to load your deck from a file, 'd' to delete a save file, or 'r' to return to the main menu: ")
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
        deck_in_use = loadFromTxt(filename)
        return


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

        return

    
    def printDecks(files):
        for f in files:
            print(f)
        return


    def listFiles(path):
        return os.listdir(path)

    #BROKEN GETS KEY ERROR 0
    def viewDeckInUse():
        print(f"\nThere are {len(deck_in_use)} cards in your deck")
        for x in deck_in_use:
            print(f"\n{card_database[x].get('card_type')}")
        return
    

    print("\n------- GAME OPTIONS MENU -------")

    decision = inputDecision().lower()

    while decision != 'r':
        if decision == 'a':
            no_cards_adding = int(input("How many cards would you like to add to the Pokemon database? "))
            addToDatabase(no_cards_adding)
        elif decision == 'v':
            viewDeckInUse()
        elif decision == 's':
            #today = date.today()
            #dateStr = today.strftime("%d-%m-%Y")
            #filename = str(username + "-"  + dateStr + ".json")
            path = "save_files/users"
            text = "Finished updating user profile!"
            filename = username
            dictToFile(user_account_dictionary, path, filename, text)
        elif decision == 'l':
            loadADeck()
        elif decision == 'd':
            deleteADeck()
        
        decision = inputDecision().lower()


#WRITE DATA TO FILE, WORKS FOR LISTS ATM
def txtToFile(path, data):
    #COULD ADD IF TYPE(DATA) IS LIST THEN ... THEREFORE WE CAN HANDLE MULTIPLE DATA TYPES
    with open(path, 'wb') as filehandle:
        pickle.dump(data, filehandle)
    print("\nFinished saving data!")
    return


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
            return


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
    return

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
        

def flipCoin():
    options = ['heads', 'tails']
    coin_toss = str(input(f"\n{username}, choose 'heads' or 'tails': ")).lower()
    coin_toss = stringValidation(coin_toss, options)

    random_coin_choice = random.choice(options)

    print(f"\nflipping the coin... \n{random_coin_choice}!")

    if coin_toss == random_coin_choice:
        options = ['first', 'second']
        decision = str(input("\nWould you like to go 'first' or 'second'? "))
        decision = stringValidation(decision, options)
        return decision
    else:
        print(f"\nYou chose {coin_toss} and it landed {random_coin_choice}...\nYour opponent gets to choose who goes first")
        if coin_toss == 'first' and random_coin_choice == 'second':
            decision = 'second'
        else:
            decision = 'first'
        return decision


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

    return


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
    
    return


def removePrizeCardFromDeck(no_prize_cards, deck_in_use):
    prizeCards = []
    for x in range(no_prize_cards):
        x = deck_in_use.pop(0)
        prizeCards.append(x)
    return prizeCards

def takePrizeCard(your_hand):
    global prize_deck
    x = prize_deck.pop()
    your_hand.append(x)
    print(f"\nAdded 1 prize card to your hand, you now have {len(your_hand)} cards ")
    return your_hand


#THIS IS EXACTLY THE SAME CODE LOL
def drawCard(no_cards_to_draw, deck_in_use):
    bufferList = []
    for x in range(no_cards_to_draw):
        x = deck_in_use.pop(0)
        bufferList.append(x)
    return bufferList


## FIRST TURN START
#SHOULD ONLY PLAY METHOD IF TAKE FIRST TURN IS TRUE BECAUSE THERE IS NO ATTACK METHOD HERE
def playPokemon():
    def addToBench(chosen_bench, no_basic_pokemon):
        global benched_pokemon
        for x in your_hand:
            x = str(x)
            if chosen_bench == card_database[x].get('name'):
                benched_pokemon[x] = card_database[x]
                benched_pokemon[x]['no_attached_energy'] = 0
                benched_pokemon[x]['attached_energy_types'] = ""
                x = int(x)
                playable_pokemon.remove(chosen_bench)
                no_basic_pokemon -= 1
                your_hand.remove(x)
                print(f"{chosen_bench.title()} was added to bench")
                return no_basic_pokemon
        

    def addToActive(chosen_active, no_basic_pokemon):
        global active_pokemon
        for x in your_hand:
            x = str(x)
            if chosen_active == card_database[x].get('name'):
                active_pokemon = card_database[x]
                active_pokemon['no_attached_energy'] = 0
                active_pokemon['attached_energy_types'] = ""
                x = int(x)
                playable_pokemon.remove(chosen_active)
                no_basic_pokemon -= 1
                your_hand.remove(x)
                return no_basic_pokemon

    global your_hand
    global deck_in_use
    playable_pokemon = []
    no_basic_pokemon = int(0) 
    chosen_bench = ""

    while no_basic_pokemon == 0:
        for x in your_hand:
            x = str(x)
            if card_database[x].get('card_type') == 'pokemon' and card_database[x].get('level') == 'basic':
                print(f"{card_database[x].get('name').title()} is a {card_database[x].get('level')} {card_database[x].get('type')} pokemon with {card_database[x].get('health')}HP and {card_database[x].get('no_moves')} moves\n")
                no_basic_pokemon += 1
                playable_pokemon.append(card_database[x].get('name').lower())

        if no_basic_pokemon != 0:
            break
        else:
            print("\nAs there are no basic pokemon in your hand, we must reshuffle.")
            your_hand = drawCard(7, deck_in_use)


    print(f"There are {len(playable_pokemon)} playable basic pokemon: {playable_pokemon}")

    chosen_active = str(input("Please enter the name of the pokemon you wish to make the active/in play: ")).lower()
    
    chosen_active = stringValidation(chosen_active, playable_pokemon)

    no_basic_pokemon = addToActive(chosen_active, no_basic_pokemon)

    while no_basic_pokemon > 0:
        print(f"\nYou have {no_basic_pokemon} basic Pokemon in your hand.")
        options = ['y', 'n']
        decision = str(input("Would you like to place a Pokemon on the bench? ('y' for yes, or 'n' for no) ")).lower()
        decision = stringValidation(decision, options)
        if decision == 'y':
            print(f"There are {len(playable_pokemon)} playable basic pokemon: {playable_pokemon}")
            chosen_bench = str(input("Please enter the name of the pokemon you want to add to the bench: ")).lower()
            chosen_bench = stringValidation(chosen_bench, playable_pokemon)
            no_basic_pokemon = addToBench(chosen_bench, no_basic_pokemon)
        elif decision == 'n':
            print("\nYou chose not to play a benched pokemon")
            return
    return
    

def stringValidation(decision, options):
    while decision not in options:
        decision = str(input("\nWhat you enter was not a valid option, please try again: (enter 'h' for help) ")).lower()
        if decision == 'h':
            print(f"\nThese are the valid options ({options})")
    return decision


def viewActivePokemon():
    global active_pokemon
    print(f"\n{active_pokemon.get('name').title()} has {active_pokemon.get('health')}HP and {active_pokemon.get('no_attached_energy')} energy cards attached.")
    no_moves = active_pokemon.get('no_moves')
    for x in range(no_moves):
        num = x
        print(f"\n{active_pokemon.get(f'ability{num}_name').title()} does {active_pokemon.get(f'ability_{num}_damage')} damage and requires {active_pokemon.get(f'ability_{num}_no_energy')} energies ")
        if active_pokemon.get(f'ability_{num}_energy_req_type') != 'none':
            print(f"\nAbility {num+1} has a requirement that there be {active_pokemon.get(f'ability_{num}_energy_req_type')} energies ")
        else:
            print(f"\nAbility {num+1} does not require any specific energy card type ")
        return

def viewBenchedPokemon():
    global benched_pokemon
    for key in benched_pokemon:
        print(f"\n{benched_pokemon[key].get('name').title()} has {benched_pokemon[key].get('health')}HP and {benched_pokemon[key].get('no_attached_energy')} energy cards attached.")
        no_moves = benched_pokemon[key].get('no_moves')
    for x in range(no_moves):
        num = x
        print(f"\n{benched_pokemon[key].get(f'ability{num}_name').title()} does {benched_pokemon[key].get(f'ability_{num}_damage')} damage and requires {benched_pokemon[key].get(f'ability_{num}_no_energy')} energies ")
        if benched_pokemon[key].get(f'ability_{num}_energy_req_type') != 'none':
            print(f"\nAbility {num+1} has a requirement that there be {benched_pokemon[key].get(f'ability_{num}_energy_req_type')} energies ")
        else:
            print(f"\nAbility {num+1} does not require any specific energy card type ")
    return

def addEnergy():
    def attachChosenEnergy(chosen_energy, your_hand):
        global active_pokemon
        for x in your_hand:
            x = str(x)
            if card_database[x].get('card_type') == 'energy' and chosen_energy == card_database[x].get('type'):
                active_pokemon['no_attached_energy'] += 1
                if active_pokemon['attached_energy_types'] == "":
                    active_pokemon['attached_energy_types'] = chosen_energy
                else:
                    active_pokemon['attached_energy_types'] = active_pokemon['attached_energy_types'] + ", " + chosen_energy
                x = int(x)
                your_hand.remove(x)
                return your_hand
    
    def attachToBenched(chosen_energy, chosen_pokemon, your_hand):
        global benched_pokemon
        for x in your_hand:
            x = str(x)
            if card_database[x].get('name') == chosen_pokemon:
                benched_pokemon[x]['no_attached_energy'] += 1
                if benched_pokemon[x]['attached_energy_types'] == "":
                    benched_pokemon[x]['attached_energy_types'] = chosen_energy
                else:
                    benched_pokemon[x]['attached_energy_types'] = active_pokemon['attached_energy_types'] + ", " + chosen_energy
                x = int(x)
                your_hand.remove(x)
                return your_hand

    def viewEnergiesInHand(playable_energies, counter_dictionary):
        for x in playable_energies:
            if x == 'water':
                counter_dictionary['water energy'] += 1
            elif x == 'grass':
                counter_dictionary['grass energy'] += 1
            elif x == 'fire':
                counter_dictionary['fire energy'] += 1
            elif x == 'electric':
                counter_dictionary['electric energy'] += 1
            elif x == 'fighting':
                counter_dictionary['fighting energy'] += 1
            elif x == 'dark':
                counter_dictionary['dark energy'] += 1
            elif x == 'fairy':
                counter_dictionary['fairy energy'] += 1
            elif x == 'steel':
                counter_dictionary['steel energy'] += 1
            elif x == 'dragon':
                counter_dictionary['dragon energy'] += 1
            elif x == 'psychic':
                counter_dictionary['psychic energy'] += 1
            elif x == 'normal':
                counter_dictionary['normal energy'] += 1

        for key, value in counter_dictionary.items():
            if value > 0:
                print(f"\nYou have {value} {key} cards in your hand")

    global your_hand
    global active_pokemon
    global benched_pokemon
    counter_dictionary = {
        'water energy': 0,
        'grass energy': 0,
        'electric energy': 0,
        'fire energy': 0,
        'fighting energy': 0,
        'steel energy': 0,
        'dark energy': 0,
        'dragon energy': 0,
        'psychic energy': 0,
        'normal energy': 0,
        'fairy energy': 0,
    }

    playable_energies = []
    bench_pokemon_list = []
    no_eneries = 0
    
    for x in your_hand:
        x = str(x)
        if card_database[x].get('card_type') == 'energy':
            no_eneries += 1
            playable_energies.append(card_database[x].get('type').lower())
    
    if no_eneries > 0:
        options = ['y', 'n']
        decision = str(input("\nWould you like to add an energy card (enter 'y' or 'n')? "))
        decision = stringValidation(decision, options)

        if decision == 'y':
            options = ['a', 'b']
            decision = str(input("\nWould you like to add an energy to the active pokemon, or a pokemon on the bench? (enter 'a' or 'b') "))
            decision = stringValidation(decision, options)

            if decision == 'a':
                #print(f"\nYour hand contains {no_eneries} energy cards.\n")
                
                viewEnergiesInHand(playable_energies, counter_dictionary)
                
                options = ['y', 'n']
                decision = str(input("Would you like to view information about the active pokemon prior to placing an energy card? (enter 'y', or 'n') "))
                decision = stringValidation(decision, options)
                
                if decision == 'y':
                    viewActivePokemon()

                chosen_energy = str(input("\nPlease enter the type of energy you would like to attach: ")).lower()
                chosen_energy = stringValidation(chosen_energy, playable_energies)
                your_hand = attachChosenEnergy(chosen_energy, your_hand)

                print(f"\nYou successfully attached a {chosen_energy} energy to {active_pokemon.get('name').title()}!")

            else:
                viewEnergiesInHand(playable_energies, counter_dictionary)

                options = ['y', 'n']
                decision = str(input("Would you like to view information about your benched pokemon prior to placing an energy card? (enter 'y', or 'n') "))
                decision = stringValidation(decision, options)

                if decision == 'y':
                    viewBenchedPokemon()
                
                for key in benched_pokemon:
                    bench_pokemon_list.append(benched_pokemon[key].get('name'))
                
                print(bench_pokemon_list)
                chosen_pokemon = str(input("Please enter the name of the benched pokemon that you would like to attach an energy to: "))
                chosen_pokemon = stringValidation(chosen_pokemon, bench_pokemon_list)

                chosen_energy = str(input(f"\nPlease enter the type of energy you would like to attach to {chosen_pokemon}: ")).lower()
                chosen_energy = stringValidation(chosen_energy, playable_energies)
                
                your_hand = attachToBenched(chosen_energy, chosen_pokemon, your_hand)

                print(f"\nYou successfully attached a {chosen_energy} energy to {chosen_pokemon.title()}!")

        else:
            return

    else:
        print("\nYou have no energies in your hand")
        return


#FUNCTIONS END

#VARIABLES START
card_database = {}
user_account_dictionary = {}
deck_in_use = []
##VARIABLES END

#PROGRAM STARTS HERE
path = "save_files/database.json"
card_database = loadFromDict(path)

#for key in card_database:
#    print(card_database[key].get('name'))

#corresponds with the no. of pokemon cards in the deck
'''
fire_deck = [0, 1, 1, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, 11, 11, 12, 13, 14, 14, 15, 15, 16, 16, 16, 17, 17, 17, 18, 18, 19]
path = "save_files/decks/fire_deck.txt"
txtToFile(path, fire_deck)
'''

#pop(0) removes the first item from a list
#x = fire_deck.pop(0)

#PRIZE DECK GOES BEFORE YOUR HAND DECLARATION


print("\nWelcome to Pokemon TCG Cli Edition!\n")

username = str(input("Please enter your username: ")).lower()

checkIfAccount()
     
print(f"\n{username.title()}, please ensure that you have network settings configured before entering a battle.\n")

if 'fav_pokemon' in user_account_dictionary:
   print(f"It's what {user_account_dictionary.get('fav_pokemon')} would have wanted...")

selectionScreen()

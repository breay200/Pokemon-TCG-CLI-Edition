import json
import os, os.path
import random
from datetime import date
import socket
import select
import errno
import sys

'''
cards = {
    1: {"card_type" : "pokemon", "name" : "charmander", "type" : "fire", "level" : "basic", "no_moves" : 2, "health" : 70, "weakness" : "water", "resistance" : "none", "retreat_cost" : 1, "attack_1_name" : "scratch", "attack_1_damage" : 10, "attack_1_energy_req" : 1, "attack_1_energy_type_req" : "none", "attack_2_name" : "flame tail", "attack_2_damage" : 20, "attack_2_energy_req" : 2, "attack_2_energy_type_req" : "1 fire"}
}
'''

#FUNCTIONS START

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
def loadFromFile(dictionary, file_path):
    with open(file_path) as f: 
        data = f.read()
    dictionary = json.loads(data)
    return dictionary
    #print("Data type after reconstruction : ", type(loaded_cards))

#VIEW DECK OPTION 
def viewDeck():

    def inputDecision():
        decision = str(input("\nEnter 'v' to view your deck, 's' to save your deck to file, 'l' to load your deck from a file, 'd' to delete a save file, 'r' to return to the main menu: "))
        while decision not in ('v', 's', 'l', 'r', 'd'):
            decision = validInput(decision)
        return decision

    def validInput(decision):
        decision = str(input("\nPlease enter a valid input (enter 'h' for help): "))
        if decision == "h":
            print("\nEnter 'v' to view your deck, 's' to save your deck to file, 'l' to load your deck from a file, 'd' to delete a save file, or 'r' to return to the main menu: ")
        return decision

    def loadSaveFunctionality():
        print("\nAvailable Save Files: \n")
        path = "save_files"
        files = listFiles(path)
        for f in files:
            print(f)
        print(files)
        #loadFromFile()

    def listFiles(path):
        return os.listdir(path)
    
    print("\n------- VIEW DECK MENU -------")

    decision = inputDecision()

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
            loadSaveFunctionality()
        elif decision == 'd':
            pass
        
        decision = inputDecision()
        

def selectionScreen(selection):
    if selection == 's':
        startBattle()
    elif selection == 'v':
        viewDeck()
    elif selection == 'c':
        #call settings config function
        pass
    elif selection == 'e':
        print("\nExiting the program...")
        quit()
    else:
        print("ERROR HAS OCCURED AT IN SELECTION SCREEN")

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

#FUNCTIONS END

#VARIABLES START
card_database = {}
coin_sides = ["heads", "tails"]
##VARIABLES END

#GAME STARTS HERE
print("\nWelcome to Pokemon TCG Cli Edition!\n")

username = str(input("Please enter your username: ")).lower()

user_account_dictionary = {}

user_save_path = "save_files/users"
saved_user_accounts = os.listdir(user_save_path)

##THIS SHOULD BE A FUNCTION
if username not in saved_user_accounts:
    choice = str(input(f"\nThere doesn't seems to be any account associated with the username: {username.title()}. \nWould you like to set one up? (enter 'y' for yes or 'n' for no) " ))
    if choice == 'y':
        createLocalUserAccount(user_save_path)
    else:
        user_account_dictionary['username'] = username
        print(f"That's okay {username}, we respect your privacy.")
elif username in saved_user_accounts:
    file_path = user_save_path + "/" + username
    user_account_dictionary = loadFromFile(user_account_dictionary, file_path)
    print("\nYour save data has been loaded from file!")

print(user_account_dictionary)        

#TO DO: create load functionality for username

start_selection = str(input(f"\n{username.title()}, please enter 's' to start a new battle, 'v' to view your deck, 'c' to config settings, or 'e' to exit: "))

while start_selection not in ('s', 'v', 'c', 'e'):
    start_selection = str(input(f"\n{username.upper()}, please enter a valid option (enter 'h' for help): "))
    if start_selection == 'h':
        print(("Enter 's' to start a new battle, 'v' to view your deck, 'c' to config settings, or 'e' to exit: "))

selectionScreen(start_selection)

'''Objective:
Develop a text-based adventure game in Python set in the fantastical land of "To Le Do." Your game will feature a choice between two paths: becoming a Wizard or a Knight. Each path involves selecting from a list of three options, with only one path leading to success. This assignment tests your ability to use programming concepts such as variables, user input, if statements, loops, lists, and error checking to handle invalid inputs.

Assignment Details:

Game Introduction:
Begin your game by welcoming the player to "To Le Do," and describe this wondrous land in your own words.

Path Selection:
Prompt the player to choose their path: Wizard or Knight. Use a list to store the paths and retrieve the player's choice.

Wizard Path:
- The player seeks the ancient tome that holds the secrets of the universe.  

Choices:
Use a list to manage these choices.
1. "Search the Ancient Library: You spend years among the tomes, but the book is nowhere to be found. Your quest ends in wisdom, but not victory."
2. "Explore the Forbidden Cave: The cave is treacherous and full of traps. Unfortunately, you do not make it out alive."
3. "Venture into the Enchanted Forest: Within the heart of the Enchanted Forest, you find the ancient tome. Your quest is a success! The secrets of the universe are yours."

Knight Path:
- The player vows to defeat the dragon terrorizing "To Le Do" for centuries.  

Choices:
Use a list to manage these choices.
1. "Attack in the Dragon's Lair: You fight valiantly in the dragon's lair, but it's too strong in its home territory. You fall in battle, remembered as a hero."
2. "Challenge to a Duel: The dragon accepts your challenge but proves too powerful in combat. The kingdom mourns its brave knight."
3. "Seek the help of a Sorcerer: With the help of a sorcerer, you weaken the dragon and defeat it in battle. The kingdom is saved, and you are hailed as its greatest hero."

Error Checking:
Implement loops around the input sections to ensure that players can only proceed with valid choices from the lists. If an invalid option is entered, the game should inform the player and prompt them to choose again. The program should ignore case.

Implementation Guidelines: 
- Describe the land of To Le Do in your own words at the beginning of the program.
- Prompt the user for inputs, using lists to store the choices (listed in bold) and retrieve them based on user input.
- Use if statements to direct the flow of the game based on the player's choices.
- Include nested if statements within each main path to handle the subsequent choices from the list.
- Apply while loops to validate user inputs, ensuring the game continues to prompt for a decision until a valid choice is made (choices are listed in bold above)
- Store player inputs in variables and use these to determine the game's outcome.
- Provide clear and concise feedback for each choice, mirroring the exact text provided above for each outcome.
- Use only programming techniques already covered in class.
- Support upper and lower case options by converting the input to lower case.
- The code must be completely your own work, not from Chegg, ChatGPT, nor your friend. If you need help, ask during the lab.

Example Code Structure:
print("Welcome to 'To Le Do'!")
# describe the land of "To Le Do" here in your own words.
paths=["wizard", "knight"]
choice=input("Choose your path (Wizard/Knight): ").lower()
while choice not in paths:
    print("Invalid choice. Please choose again.")
    choice =input("Choose your path (Wizard/Knight): ").lower()

if choice == "wizard":
    # Wizard path with list of choices and nested if and while for error checking
elif choice == "knight":
    # Knight path with list of choices and nested if and while for error checking


At the end of the game, ask the user if they would like to play again. If yes, start the game again; otherwise, exit the program.

Requirements:
- Submit a Python script (.py file) to Blackboard that runs the adventure game from start to finish.
- Ensure your script includes the instructions as comments and comments explaining major sections and logic used in the game in your own words.
- Test your game to ensure all paths work as expected and that invalid inputs are handled gracefully.
- You must store the user options in a list.

This assignment will help you practice control structures in Python, including decision-making with if statements, looping with while, and using lists and input validation to create an engaging text-based game.'''

#This is out section for listing the options the player will go through will choosing their class, items and adventuring area.
a = "Welcome to Gillinor! A land full of choices, mystery and potential for massive rewards. Anybody can make it in this world with the right loadout. Now, select your class: Knight or Wizard. "
choice = input(a).capitalize()

tasks = ["Shop", "Adventuring"]
items = ["Potion", "Armor", "Weapons"]
potion_items = ["Healing Potion", "Harming Potion", "Physical Potion"]
armor_items = ["Adamant equipment", "Mithril equipment", "Rune equipment"]
weapons_items = ["Adamant sword", "Mithril sword", "Rune sword"]
actions = ["Open the Tomb", "Hack the Branches", "Open the Door"]

#By labeling this def shop I can have all of the options and their consequences added into a easy to read format I will do the same for adventuring later I also need the while true statement here to give the player the option to come back to the start.
def shop():
    while True:
        print("Welcome to the shop! Here are your items: ")
        print(items)

        selected_item = input("Please select an item (Potion, Armor, Weapons), or type 'Exit' to leave the shop: ").capitalize()

        if selected_item == "Potion":
            print("You have selected Potions: ", potion_items)
            potion_choice = input("Which potion would you like to buy? ").title()
            if potion_choice == "Healing Potion":
                print("You have obtained a Healing Potion.")
            elif potion_choice == "Harming Potion":
                print("You have obtained a Harming Potion.")
            elif potion_choice == "Physical Potion":
                print("You have obtained a Physical Potion.")
            else:
                print("Invalid potion choice.")

        elif selected_item == "Armor":
            print("You have selected Armor: ", armor_items)
            armor_choice = input("Which armor would you like to buy? ").title()
            if armor_choice == "Adamant Equipment":
                print("You have obtained Adamant equipment.")
            elif armor_choice == "Mithril Equipment":
                print("You have obtained Mithril equipment.")
            elif armor_choice == "Rune Equipment":
                print("You have obtained Rune equipment.")
            else:
                print("Invalid armor choice.")

        elif selected_item == "Weapons":
            print("You have selected Weapons: ", weapons_items)
            weapon_choice = input("Which weapon would you like to buy? ").title()
            if weapon_choice == "Adamant Sword":
                print("You have obtained an Adamant sword.")
            elif weapon_choice == "Mithril Sword":
                print("You have obtained a Mithril sword.")
            elif weapon_choice == "Rune Sword":
                print("You have obtained a Rune sword.")
            else:
                print("Invalid weapon choice.")

        elif selected_item == "Exit":
            print("Thank you for visiting the shop. See you next time!")
            break  

        else:
            print("That is not an item choice. Please select Potion, Armor, or Weapons.")

#As with the shop tab this is for the player to choose their adventure and what will happen with their choses I cannot code a full game so the choices are as indepth.
def adventuring():
    print("Welcome to the start of your adventure!")
    selected_action = input("Where do you want to explore? Choose one: Open the Tomb, Hack the Branches, Open the Door: ").title()

    if selected_action == "Open The Tomb":
        print("You approach the ancient tomb. The stone door creaks open as you step inside...")
        print("You notice four red doorways that illuminate the area")
        door_choice = input("What door do you go through? N, W, E, S: ").upper()
        if door_choice in ["N", "W", "E", "S"]:
            print("You fall through a trapdoor and perish.")
        else:
            print("Invalid door choice.")

    elif selected_action == "Hack The Branches":
        print("You hack your way through the thick branches, revealing a hidden path into the forest...")
        print("As you walk through the forest you see a building. Do you enter? Y/N ")
        building_choice = input("Do you enter? Y/N ").upper()
        if building_choice == "Y":
            print("You are stabbed from behind and slain")
        else:
            print("You decide to turn around returning to the village.")

    elif selected_action == "Open The Door":
        print("You push the door open and step into a grand hall filled with mysteries...")
        print("You see a book that looks extra special. Do you reach for the book? Y/N ")
        book_choice = input("Y/N ").upper()
        if book_choice == "Y":
            print("The book levitates off from the bookshelf and begins attacking you. You were unable to get proper footing and fall to the book.")
        else:
            print("You decide to turn around returning to the village.")

    else:
        print("Invalid action. Please choose 'Open the Tomb', 'Hack the Branches', or 'Open the Door'.")

#This section is for the choice on what class they want along with what they plan to do after selecting their class.
if choice == "Knight" or choice == "Wizard":
    while True:  
        activity = input("Would you like to go to the Shop, Adventuring, or Exit? ").capitalize()

        if activity == "Shop":
            shop()
        elif activity == "Adventuring":
            adventuring()
        elif activity == "Exit":
            print("Thank you for playing!")
            break  
        else:
            print("Invalid choice, please choose Shop, Adventuring, or Exit.")
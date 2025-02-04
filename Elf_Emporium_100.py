import random
import time
import os

# Utility functions
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause(seconds=2):
    time.sleep(seconds)

def print_delayed(text, delay=0.05):
    """Print text character by character for dramatic effect."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print("")

# Main game function
def main():
    clear_screen()
    print_delayed("=============================================")
    print_delayed("        WELCOME TO THE ELF TRADING RPG       ")
    print_delayed("=============================================\n")
    
    player_name = input("Greetings, noble wanderer! What shall I call you? ").strip()
    if not player_name:
        player_name = "Mystic Elf"
    print_delayed(f"\nAh, {player_name}! May your pockets be heavy and your trades be ever profitable!")
    pause(2)
    
    # Player status
    gold = 150
    inventory = {
        'Magic Potion': 2,
        'Elven Bread': 8,
        'Crystal Shard': 3,
        'Glittering Acorn': 1
    }
    
    # Items available at the market (with humorous descriptions)
    market_items = {
        'Mystic Herb': {'price': 12, 'desc': 'A herb that smells suspiciously like unicorn tears.'},
        'Ancient Relic': {'price': 60, 'desc': 'An ancient relic rumored to be cursed (or blessed, who can tell?)'},
        'Enchanted Bow': {'price': 100, 'desc': 'A bow that sings ballads when you shoot an arrow.'},
        'Pixie Dust': {'price': 25, 'desc': 'Sparkling dust to make your trades extra magical.'},
        'Goblin Gadget': {'price': 40, 'desc': 'A mysterious gadget made by goblins. Its purpose? Even they are unsure!'}
    }
    
    # Main game loop
    while True:
        clear_screen()
        print(f"========== {player_name}'s Enchanted Inventory ==========")
        print(f"Gold: {gold}")
        for item, count in inventory.items():
            print(f"  - {item}: {count}")
        print("=============================================\n")
        
        print("What misadventure shall you embark on today?")
        print("1. Haggling with a fellow elf")
        print("2. Visiting the magical market")
        print("3. Roaming the enchanted forest")
        print("4. Stopping by the quirky tavern")
        print("5. Exit the realm (quit game)")
        
        choice = input("Your choice (1-5): ").strip()
        if choice == "1":
            gold, inventory = trade_with_elf(gold, inventory)
        elif choice == "2":
            gold, inventory = visit_market(gold, inventory, market_items)
        elif choice == "3":
            gold, inventory = wander_forest(gold, inventory)
        elif choice == "4":
            gold, inventory = visit_tavern(gold, inventory)
        elif choice == "5":
            print_delayed("\nFarewell, brave traveler! May the forest whisper secrets of fortune to you!")
            break
        else:
            print_delayed("I beg your pardon? Please choose a valid option (1-5)!")
        
        pause(2)

# Function for trading with another elf
def trade_with_elf(gold, inventory):
    clear_screen()
    print_delayed("You stroll along a mossy path until you meet a flamboyant elf wearing a sparkling cape...\n")
    trade_offer = generate_trade_offer()
    offer_item = trade_offer['offer_item']
    demand_item = trade_offer['demand_item']
    extra_dialog = trade_offer['dialog']
    
    print_delayed(f"The caped elf exclaims: '{extra_dialog}'")
    print_delayed(f"'I propose a trade: I'll bestow upon you a {offer_item} if you hand over one {demand_item}.'")
    
    # Sometimes the elf throws in a twist!
    alt_gold = None
    if random.choice([True, False]):
        alt_gold = random.randint(10, 30)
        print_delayed(f"Or, if you're feeling cheeky, you can pay me {alt_gold} gold instead of offering your {demand_item}!")
    
    answer = input("Do you accept this whimsical trade? (yes/no): ").strip().lower()
    if answer in ("yes", "y"):
        if inventory.get(demand_item, 0) > 0:
            inventory[demand_item] -= 1
            inventory[offer_item] = inventory.get(offer_item, 0) + 1
            print_delayed(f"Splendid! You traded one {demand_item} and now possess one {offer_item}.")
        elif alt_gold is not None and gold >= alt_gold:
            alt_choice = input(f"You lack a {demand_item}. Pay {alt_gold} gold instead? (yes/no): ").strip().lower()
            if alt_choice in ("yes", "y"):
                gold -= alt_gold
                inventory[offer_item] = inventory.get(offer_item, 0) + 1
                print_delayed(f"Aha! You parted with {alt_gold} gold and gained a {offer_item}.")
            else:
                print_delayed("Alas, the elf folds his arms and vanishes into the twilight.")
        else:
            print_delayed("Oh dear! You don't have the required item or enough gold. The elf shrugs and walks away.")
    else:
        print_delayed("You decline the offer, and the caped elf theatrically bows before disappearing into the mist.")
    
    pause(2)
    return gold, inventory

# Function for visiting the market
def visit_market(gold, inventory, market_items):
    clear_screen()
    print_delayed("You arrive at the magical market, where stalls shimmer with enchantments and oddities.\n")
    print("Items available for purchase:")
    for idx, (item, data) in enumerate(market_items.items(), start=1):
        print(f"  {idx}. {item} - {data['price']} gold | {data['desc']}")
    print("")
    
    selection = input("Enter the number of the item you wish to acquire (or 'b' to bail out): ").strip()
    if selection.lower() == 'b':
        print_delayed("You decide to wander off, leaving the market behind.")
        pause(1)
        return gold, inventory

    # Validate that the input is a number and within the correct range.
    try:
        selection_num = int(selection)
    except ValueError:
        print_delayed("That doesn't seem to be a valid number! Let's head back to the main path.")
        pause(1)
        return gold, inventory

    if selection_num < 1 or selection_num > len(market_items):
        print_delayed("Hmm... that stall doesn't exist. Returning to the main path!")
        pause(1)
        return gold, inventory

    # Retrieve the chosen item and its price.
    item = list(market_items.keys())[selection_num - 1]
    price = market_items[item]['price']
    
    # Ask for quantity until a valid positive integer is provided.
    while True:
        quantity_input = input(f"How many {item}(s) would you like to purchase? ").strip()
        try:
            quantity = int(quantity_input)
            if quantity < 1:
                print_delayed("You must purchase at least one! Try again.")
            else:
                break
        except ValueError:
            print_delayed("That's not a valid number! Please enter a numeric value.")

    total_cost = price * quantity
    if total_cost > gold:
        print_delayed("Oh no! You don't have enough gold for that purchase!")
    else:
        gold -= total_cost
        inventory[item] = inventory.get(item, 0) + quantity
        print_delayed(f"Splendid purchase! You bought {quantity} {item}(s) for {total_cost} gold.")
    
    pause(2)
    return gold, inventory

# Function for wandering the enchanted forest
def wander_forest(gold, inventory):
    clear_screen()
    print_delayed("You venture deep into the enchanted forest, where every rustle might hide a secret...\n")
    event = random.choice(['treasure', 'sprite', 'mysterious_cabin', 'riddle_tree', 'nothing'])
    
    if event == 'treasure':
        found_gold = random.randint(20, 60)
        gold += found_gold
        print_delayed(f"Fortune smiles upon you! You discover a hidden stash containing {found_gold} gold.")
    elif event == 'sprite':
        if inventory:
            lost_item = random.choice(list(inventory.keys()))
            if inventory.get(lost_item, 0) > 0:
                inventory[lost_item] -= 1
                print_delayed(f"A mischievous sprite zooms by and snatches a {lost_item} right out of your bag!")
            else:
                print_delayed("A playful sprite dances around you, but finds nothing to steal.")
        else:
            print_delayed("A lonely sprite flutters by, but you have no belongings for it to meddle with.")
    elif event == 'mysterious_cabin':
        print_delayed("You stumble upon a mysterious wooden cabin. An old sign reads 'Free hugs and free trades!'\n")
        trade = input("Do you enter the cabin for a free trade? (yes/no): ").strip().lower()
        if trade in ("yes", "y"):
            gold, inventory = trade_with_elf(gold, inventory)
        else:
            print_delayed("You decide to leave the peculiar cabin behind.")
    elif event == 'riddle_tree':
        print_delayed("A gnarled old tree speaks: 'Answer my riddle, and I shall reward you!'")
        print_delayed("'I speak without a mouth and hear without ears. I have nobody, but I come alive with wind. What am I?'")
        answer = input("Your answer: ").strip().lower()
        if "echo" in answer:
            reward = random.randint(15, 40)
            gold += reward
            print_delayed(f"'Correct!' booms the tree. You are gifted {reward} gold for your wisdom.")
        else:
            print_delayed("The tree groans, 'Alas, wrong answer!' and nothing happens.")
    elif event == 'nothing':
        print_delayed("The forest is peaceful and quiet... maybe too quiet. You return with no news.")
    
    pause(2)
    return gold, inventory

# Function for visiting the quirky tavern
def visit_tavern(gold, inventory):
    clear_screen()
    print_delayed("You enter 'The Drunken Dryad', a tavern famed for its outrageous stories and even stranger patrons.\n")
    print_delayed("A boisterous bard sings: 'Welcome, traveler! Trade a story for a bargain, if you dare!'")
    
    action = random.choice(['story_trade', 'free_drink', 'joke_challenge'])
    if action == 'story_trade':
        print_delayed("A mysterious patron approaches and says, 'Tell me a funny tale and I'll give you a rare item!'")
        story = input("Spin your tale (or press enter to stay silent): ").strip()
        if story:
            reward_item = random.choice(['Goblin Gadget', 'Pixie Dust', 'Enchanted Feather'])
            inventory[reward_item] = inventory.get(reward_item, 0) + 1
            print_delayed(f"The patron bursts out laughing and gifts you a {reward_item}!")
        else:
            print_delayed("Silence... The patron frowns and retreats to his corner.")
    elif action == 'free_drink':
        print_delayed("The tavern keeper shouts, 'Drink up, on the house!' You enjoy a free, magically restorative drink.")
        bonus = random.choice(['Magic Potion', 'Elven Bread'])
        inventory[bonus] = inventory.get(bonus, 0) + 1
        print_delayed(f"You receive an extra {bonus} as a bonus!")
    elif action == 'joke_challenge':
        print_delayed("A cheeky dwarf challenges you: 'Tell me your best joke, and I'll lower my prices for a trade!'")
        joke = input("Your joke: ").strip()
        if joke:
            print_delayed("The dwarf cackles heartily, 'Ha! That's a good one!'")
            discount = random.randint(5, 15)
            gold += discount  # reward you by topping up a bit of gold
            print_delayed(f"You receive a bonus of {discount} gold for your wit!")
        else:
            print_delayed("The dwarf shakes his head, 'No joke? No discount! Better luck next time.'")
    
    pause(2)
    return gold, inventory

# Generate a quirky trade offer with extra dialog
def generate_trade_offer():
    possible_items = [
        'Magic Potion',
        'Elven Bread',
        'Crystal Shard',
        'Glittering Acorn',
        'Mystic Herb',
        'Ancient Relic',
        'Enchanted Bow',
        'Pixie Dust',
        'Goblin Gadget'
    ]
    offer_item = random.choice(possible_items)
    demand_item = random.choice(possible_items)
    while demand_item == offer_item:
        demand_item = random.choice(possible_items)
    
    dialogs = [
        f"'I've been eyeing a fine {offer_item} all morning!'",
        f"'I just acquired a {offer_item} and I'm feeling generous!'",
        f"'This {offer_item} practically sings if you have a {demand_item} to spare!'",
        f"'Trade with me and let the fates smile upon you with a {offer_item}!'"
    ]
    dialog = random.choice(dialogs)
    return {'offer_item': offer_item, 'demand_item': demand_item, 'dialog': dialog}

if __name__ == "__main__":
    main()

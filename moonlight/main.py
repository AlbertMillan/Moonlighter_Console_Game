from map import Map
from character import Player

# Adjust player's health based on the monsters in the room
def fight(myPlayer, myMap):
    monsters = myMap.scenes[ myMap.currentScene ].get_monsters()                # Three element array containing the number of monsters of each type
    myPlayer.hurted( monsters[0] * 5 + monsters[1] * 4 + monsters[2] * 2)       # PlayerHealth = PlayerHealth - number_of_monsters_of_given_type * attack_damage_of_the_monsters
    myMap.scenes[ myMap.currentScene ].kill_monsters()                          # Monsters die after attacking
    if myPlayer.health <= 0:                                                    # Check if player is dead
        myPlayer.switch_state()

# Prints the current screen and the options the player can take.
def print_player_position():
    if len(myMap.scenes[ myMap.currentScene].connections) == 1:
        print("Billy is at scene %r. This scene has doors leading towards scene %d. What way should Billy take? Please type in the door number." % (myMap.currentScene, myMap.scenes[ myMap.currentScene ].connections[0] )  )
    elif len(myMap.scenes[ myMap.currentScene].connections) == 2:
        print("Billy is at scene %r. This scene has doors leading towards scene %d and %d. What way should Billy take? Please type in the door number." % (myMap.currentScene, myMap.scenes[ myMap.currentScene ].connections[0], myMap.scenes[ myMap.currentScene ].connections[1] )  )
    else:
        print("Billy is at scene %r. This scene has doors leading towards scene %d, %d and %d. What way should Billy take? Please type in the door number." % (myMap.currentScene, myMap.scenes[ myMap.currentScene ].connections[0], myMap.scenes[ myMap.currentScene ].connections[1], myMap.scenes[ myMap.currentScene ].connections[2]))

# Process the user input checking if it matches with the available options.
def process_room_input(move):
    while not move:
        user_input = int(input(prompt))                                     # Store user input

        # User input matches with the posible rooms it can move to
        if user_input in myMap.scenes[ myMap.currentScene ].connections:
            myMap.move_to(user_input)
            move = True
        # Invalid move.
        else:
            print("That is not a valid scene. Billy will starve to death if he doesn't know the directions!")
    

myMap = Map(12)
myPlayer = Player( 50, 7 )
chest_count = 0
finished = False
move = False
game_over = False
visited = []
user_input = 0
prompt = ">>> "

print("""Welcome to Moonlighter for console version. In this game, you will incarnate Billy, an adventurous guy that tends to seek fortune in
highly dangerous dungeons. Billy just happened to enter the cave.\n""")

while not finished:
    
    # Prints the rooms the player has previously visited.
    if len(visited) > 0:
        print("Scenes visited:", visited)

    # Prints the current screen and the options the player can take.
    print_player_position()
    print(myMap.scenes[ myMap.currentScene ].connections)
    move = False

    # Handle user input
    process_room_input(move)

    # Move successful message
    print("Billy Moved successfully to scene %r. This scene has %d monsters." % (myMap.currentScene, len(myMap.scenes[ myMap.currentScene ].enemies) ) )
    monsters = myMap.scenes[ myMap.currentScene ].get_monsters()
    print("It has %d fast, %d moderate, and %d tank." % ( monsters[0], monsters[1], monsters[2] )  ) 

    # Case where monsters in a given scene are already dead.
    if monsters.count(0) != 3:
        print("Billy has %d health points" % myPlayer.health)
        print("What will Billy do? \'Start fight\' or \'Go back\'?")
        visited.append(myMap.currentScene)
        move = False
        has_fought = False

        # Process action taken when entering a new room ('Start fight' or 'Go back')
        while not move:
            user_input = input(prompt)

            if user_input == "Start fight":
                # Attack system function
                fight(myPlayer, myMap)
                move = True
                has_fought = True
            # Go back to previous room
            elif user_input == "Go back":
                myMap.move_to( myMap.scenes[ myMap.currentScene ].connections[0] )
                print("Billy went back successfully.")
                move = True
            else:
                print("That is not a valid action. Billy will be attacked if he doesn't decide quickly!")

    if myPlayer.is_alive:
        if has_fought:
            print("Billy won the fight. He has %d hitpoints remaining." % myPlayer.health)
            # Check if scene contains a chest, display message accordingly.
            if myMap.scenes[ myMap.currentScene ].has_chest:
                chest_count = chest_count + 1
                print("Good job, this scene contained a chest!")
            else:
                print("Harsh luck, no chest in this scene.")

        # Player wins
        elif len(visited) == len(myMap.scenes):
            finished = True

        else:
            print("Billy went back successfully.")
    # Player is dead
    else:
        game_over = True
        finished = True

if game_over:
    print("Billy died. Unlucky. Restart the progam to play again.")
else:
    print("Congratulations! You won the game!")
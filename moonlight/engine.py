from random import randint, choice, shuffle

enemies = ['fast', 'moderate', 'tank']
children = [1, 2]

class Map(object):    # can be level
    
    def __init__( self, size ):
        self.scenes = []
        self.arr = []
        self.closed = []
        self.currentScene = 0
        
        # Create scenes given the size of the map
        for i in range(size):
            # Create scenes
            newScene = Scene( i, randint(0, 4) )
            self.scenes.append(newScene)

            # Contains the id of each scenes. Scenes in this list have not yet been 'connected' to other scenes.
            self.arr.append(i)
            
            if i < 2:
                self.closed.append(True)             # At least two nodes/scenes must be closed (have no child nodes)
            else:
                self.closed.append(False)            # All others can be open (have child nodes)
        
        # Adjust for: First element is manually 'connected' with others.
        self.arr.pop(0)          # Node 0
        self.closed.pop()
        self.closed.pop()
        shuffle(self.closed)

    # 'Connect' each scene with others in order to create a map. Remove them from the possible connections. 
    # A child cannot be connected with other same level nodes on the tree
        # Root node has initially 3 children
        self.scenes[0].set_connection( self.scenes[self.arr.pop(0)] )     # Node 1
        self.scenes[0].set_connection( self.scenes[self.arr.pop(0)] )     # Node 2
        self.scenes[0].set_connection( self.scenes[self.arr.pop(0)] )     # Node 3


        # Generate the 'connections' of the remaining nodes.
        self.generate_tree_structure(size)


    # Generate the 'connections' of the remaining nodes.
    def generate_tree_structure(self, size):
        for i in range(size-2):
            print( "\n", self.arr, "\n", self.closed )

            # Set the number of connections of the current node
            scene_connections = self.get_children()

            # Current node has one child (2 connections: parent + child)
            if scene_connections == 1:
                self.scenes[i+1].set_connection( self.scenes[self.arr.pop(0)] )

            # Current node has two child nodes (3 connections: parent + 2 * child)
            elif scene_connections == 2:
                self.scenes[i+1].set_connection( self.scenes[self.arr.pop(0)] )
                self.scenes[i+1].set_connection( self.scenes[self.arr.pop(0)] )

                # Two children means an extra path, which must be closed at some point. Keep the same number of nodes.
                swap = False
                j = 0
                while not swap:
                    if self.closed[j] == False:
                        self.closed[j] = True
                        swap = True
                    j = j + 1

            else:
                self.scenes[i+1].set_chest()
                print("Scene %d has no doors to other rooms" % (i+1) ) 

        print("Loop Completed!")

    # Probabilistic determination of the number of children of given node (none, 1, or 2)
    def get_children(self):
        pos = randint( 0, len(self.closed) ) - 1    # Initially, two nodes must be closed (have no children)

        if self.closed[pos]   ==   False:
            scene_connections = choice(children)
        else:
            scene_connections = None
        
        self.closed.pop(pos)

        return scene_connections

    # Move to scene specified by the user (destination variable)
    def move_to (self, destination):
        self.currentScene = destination
        #print("Billy Moved successfully to scene %r" % self.currentScene)



# TODO CORRECTIONS. IGNORE FOR NOW.
class Scene(object):
    
    def __init__(self, id, number_of_enemies):
        self.enemies = []

        for i in range(number_of_enemies):
            self.enemies.append( Enemy(i) )

        self.has_chest = False
        self.id = id
        self.connections = []
        self.number_of_connections = 0

    # Connects current scene with the 'other' scene. Id of the other is stored.
    def set_connection(self, other):
        self.connections.append(other.id)
        other.connections.append(self.id)
        self.number_of_connections  = self.number_of_connections + 1
        other.number_of_connections = other.number_of_connections + 1

    def set_chest(self):
        self.has_chest = True



# Stores the basic attributes (health + attack damage) of the player and enemy characters
class Character(object):

    def __init__(self, health, attack_damage):
        self.health = health
        self.attack_damage = attack_damage
        self.is_alive = True

class Player(Character):

    def __init__(self, health, attack_damage):
        super(Player, self).__init__(health, attack_damage)

class Enemy(Character):
    
    def __init__(self, id):
        self.id = id
        self.type = choice(enemies)
        

        # Set enemy attributes
        if self.type == 'fast':
            health = randint( 1, 4 )
            attack_damage = randint( 3, 6 )
        elif self.type == 'moderate':
            health = randint( 4, 10 )
            attack_damage = randint( 4, 8 )
        else:
            health = randint( 6, 13 )
            attack_damage = randint( 1, 5 )

        super(Enemy, self).__init__( health, attack_damage )

    def switch_state(self):
        self.is_alive = False




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
    
    if len(visited) > 0:
        print("Scenes visited:", visited)

    print("Billy is at scene %r. This scene has doors leading towards scene %d, %d and %d. What way should Billy take? Please type in the door number." % myMap.currentScene, 
    myMap.scenes[ myMap.currentScene ].connections[0], myMap.scenes[ myMap.currentScene ].connections[1], myMap.scenes[ myMap.currentScene ].connections[3])
    user_input = input(prompt)
    move = False

    while not move:
        if user_input in myMap.scenes[ myMap.currentScene ].connections:
            myMap.move_to(user_input)
            move = True
        else:
            print("That is not a valid scene. Billy will starve to death if he doesn't know the directions!")

    print("Billy Moved successfully to scene %r. This scene has %d monsters." % (myMap.currentScene, len(myMap.scenes[ myMap.currentScene ].enemies) )
    #print("It has %d fast, %d moderate, and %d tank." % ( myMap.scenes[ myMap.currentScene ].enemies.count() )))
    print("What will Billy do? \'Start fight\' or \Go back\'?")
    visited.append(myMap.currentScene)
    user_input = input(prompt)
    move = False
    has_fought = False

    while not move:
        if user_input == "Start fight":
            # Attack system function
            
            move = True
            has_fought = True
        # Go back to previous room
        elif user_input == "Go back":
            myMap.move_to( myMap.scenes[ myMap.currentScene ].connections[0] )
            print("Billy went back successfully.")
            move = True
        else:
            print("That is not a valid action. Billy will be attacked if he doesn't decide quickly!")

    if myPlayer.is_alive and has_fought:
         # Check if scene contains a chest, display message accordingly.
        if myMap.scenes[ myMap.currentScene ].has_chest:
            chest_count = chest_count + 1
            print("Good job, this scene contained a chest!")
        else:
            print("Harsh luck, no chest in this scene.")
    # Player went back to previous room.
    elif: myPlayer.is_alive:
        print("Keep going!")
    # Player is dead
    else:
        game_over = True
        finished = True



   

    
    

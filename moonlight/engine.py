from random import randint, choice, shuffle

enemies = ['weak', 'moderate', 'strong']
children = [1, 2]

class Map(object):    # can be level
    
    def __init__(self, size, max_connections ):
        self.scenes = []
        self.arr = []
        self.closed = []
        
        # Create scenes given the size of the map
        for i in range(size):
            # Create scenes
            newScene = Scene(i, randint(0, 4), randint(-1, 1) )
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



# TODO CORRECTIONS. IGNORE FOR NOW.
class Scene(object):
    
    def __init__(self, id, number_of_enemies, contains_chest):
        self.enemies = number_of_enemies
        self.has_chest = contains_chest
        self.id = id
        self.connections = []
        self.number_of_connections = 0

    # Connects current scene with the 'other' scene. Id of the other is stored.
    def set_connection(self, other):
        self.connections.append(other.id)
        other.connections.append(self.id)
        self.number_of_connections  = self.number_of_connections + 1
        other.number_of_connections = other.number_of_connections + 1



# Stores the basic attributes (health + attack damage) of the player and enemy characters
class Character(object):

    def __init__(self, health, attack_damage):
        self.health = health
        self.attack_damage = attack_damage

class Player(Character):

    def __init__(self, health, attack_damage):
        super(Player, self).__init__(health, attack_damage)

class Enemy(Character):
    
    def __init__(self, health, attack_damage):
        super(Enemy, self).__init__(health, attack_damage)
        self.type = choice(enemies)


myMap = Map(12, 3)
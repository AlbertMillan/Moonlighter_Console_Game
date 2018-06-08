from random import randint, choice

enemies = ['weak', 'moderate', 'strong']
children = [None, 1, 2]

class Map(object):    # can be level
    
    def __init__(self, size, max_connections ):
        self.scenes = []
        arr = []
        
        #Create scenes given by size
        for i in size:
            self.scenes.append(Scene(i, randint(0, 4), randint(-1, 1)))
            arr.append(i)

        # 'Connect' each scene with others in order to create a map
        self.scenes[0].set_connection(1, 2, 3)

        # remove them from the possible connections. A child cannot be connected with other same level nodes on the tree
        arr.pop(0)
        arr.pop(0)
        arr.pop(0)
        arr.pop(0)

        for i in size-1:
            # set the number of connections of the current node
            scene_connections = choice(children)

            if scene_connections == 1:
                #self.scenes[i+1].set_connection[i+2]
                self.scenes[i+1].set_connection( arr.pop(0), None )

            elif scene_connections == 2:
                #self.scenes[i+1].set_connection[i+2]
                #self.scenes[i+1].set_connection[i+3]
                self.scenes[i+1].set_connection( arr.pop(0), arr.pop(1) )

            else:
                print("Scene %d has no doors to other rooms" % i)





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

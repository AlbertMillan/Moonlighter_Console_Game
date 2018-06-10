from character import Enemy

class Scene(object):
    
    def __init__(self, id, number_of_enemies):
        self.enemies = []

        # Do not create monsters in the starting scene
        if id != 0:
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

    def get_monsters(self):
        monsters = [0, 0, 0]
        for i in range(len(self.enemies)):
            if self.enemies[i].is_alive:
                if self.enemies[i] == 'fast':
                    monsters[0] = monsters[0] + 1
                elif self.enemies[i] == 'moderate':
                    monsters[1] = monsters[1] + 1
                else:
                    monsters[2] = monsters[2] + 1
        
        return monsters

    def kill_monsters(self):
        for i in range(len(self.enemies)):
            self.enemies[i].switch_state()
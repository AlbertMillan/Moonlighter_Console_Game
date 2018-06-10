from random import choice

enemies = ['fast', 'moderate', 'tank']

# Stores the basic attributes (health + attack damage) of the player and enemy characters
class Character(object):

    def __init__(self, health, attack_damage):
        self.health = health
        self.attack_damage = attack_damage
        self.is_alive = True

class Player(Character):

    def __init__(self, health, attack_damage):
        super(Player, self).__init__(health, attack_damage)

    def hurted(self, attack_damage):
        self.health = self.health - attack_damage

    def switch_state(self):
        self.is_alive = False

class Enemy(Character):
    
    def __init__(self, id):
        self.id = id
        self.type = choice(enemies)
        

        # Set enemy attributes
        if self.type == 'fast':
            health = 3
            attack_damage = 5
        elif self.type == 'moderate':
            health = 8
            attack_damage = 4
        else:
            health = 13
            attack_damage = 2

        super(Enemy, self).__init__( health, attack_damage )

    def check_alive(self):
        return self.is_alive

    def switch_state(self):
        self.is_alive = False

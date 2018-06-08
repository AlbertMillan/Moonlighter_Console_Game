from random import randint

class Map(object):    # can be level
    
    def __init__(self, size):
        self.scenes = []
        for i in size:
            self.scenes.append(Scene(i, randint(0, 5), randint(0, 2)))



class Scene(object):
    
    def __init__(self, id, number_of_enemies, contains_chest):
        self.enemies = number_of_enemies
        self.has_chest = contains_chest
        self.id = id

#class Player(object):

   # def __init__(self):




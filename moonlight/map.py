from random import randint, choice, shuffle
from scene import Scene

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
            newScene = Scene( i, randint(2, 4) )
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

                # Does not execute when there are no elements remaining
                if len(self.arr) > 0:
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

        print("Loop Completed!\n")

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
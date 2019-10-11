#This file contains definition of self-defined classes
import numpy as np

# Define Node
class Node:

    def __init__(self, seq, x, y):
        self.seq = seq
        self.x = x
        self.y = y

    # length between two nodes
    def length(self, neighbor):

        x1 = float(self.x)
        y1 = float(self.y)

        x2 = float(neighbor.x)
        y2 = float(neighbor.y)

        length = np.sqrt((x1-x2)**2 + (y1-y2)**2)

        return length

# Define Route
# distance method has to be called for each route instance to get length
class Route():
    
    def __init__(self, route):
        self.route = route
        self.length = 0

    def distance(self):
        if self.length == 0:
            if len(self.route) == 1:
                return 0
            else:
                temp = 0
                first_node = self.route[0]

                for i in range(len(self.route)):
                    start_node = self.route[i]

                    if i == (len(self.route) - 1):
                        break
                    else:
                        dest_node = self.route[i+1]

                        temp += start_node.length(dest_node)

                start_node = dest_node
                dest_node = first_node
                temp += start_node.length(dest_node)

                self.length = temp
        return self.length
import random
import math
import csv


class Model:

    def __init__(self):
        self.allNodes = []
        self.customers = []
        self.matrix = []
        self.capacity = -1


    def BuildModel(self):
      
        f = open("data2.txt", "r")
        reader=csv.reader(f)
        for row in reader:
           cust = (Nodes(int(row[0]),int(row[1]),int(row[2]),int(row[3]),int(row[4])))
           self.allNodes.append(cust)
           self.customers.append(cust)

        rows = len(self.allNodes)
        self.matrix = [[0.0 for x in range(rows)] for y in range(rows)]

        for i in range(0, len(self.allNodes)):
            a = self.allNodes[i]

            for j in range(0, len(self.allNodes)):
                b = self.allNodes[j]
                dist = math.sqrt(math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2))
                self.matrix[i][j] = dist

#ID,XCOORD,YCOORD,DEMAND,UNLOADING_TIME
class Nodes:
    def __init__(self,ID,xcoord,ycoord,demand,unload_time):
        self.x = xcoord
        self.y = ycoord
        self.ID = ID
        self.demand = demand
        self.unload_time = unload_time
        self.isRouted = False
   

class Route:
    def __init__(self, dp, cap):
        self.sequenceOfNodes = []
        self.sequenceOfNodes.append(dp)
        self.sequenceOfNodes.append(dp)
        self.cost = 0
        self.capacity = cap
        self.load = 0  
        



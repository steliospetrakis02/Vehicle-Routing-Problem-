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
        dem2=[]
        
        for row in reader:
           cust = (Node(int(row[0]),int(row[1]),int(row[2]),int(row[3]),int(row[4])))
           dem2.append(int(row[3]))

           self.allNodes.append(cust)
           self.customers.append(cust)
        
        rows = len(self.allNodes)
        self.matrix = [[0.0 for x in range(rows)] for y in range(rows)]
        self.capacity = 200

        totalCustomers = 100

        for i in range(0, len(self.allNodes)):
            
            for j in range(0, len(self.allNodes)):
                a = self.allNodes[i]
                b = self.allNodes[j]
                dist = math.sqrt(math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2))
                self.matrix[i][j] = dist

#ID,XCOORD,YCOORD,DEMAND,UNLOADING_TIME
class Node:
    def __init__(self, idd, xx, yy, dem,unload_time):
        self.x = xx
        self.y = yy
        self.ID = idd
        self.demand = dem
        self.unload_time = unload_time
        self.isRouted = False


class Route:
    def __init__(self, dp, cap):
        self.sequenceOfNodes = []
        self.sequenceOfNodes.append(dp)
        self.cost = 0
        self.capacity = cap
        self.load = 0  
        



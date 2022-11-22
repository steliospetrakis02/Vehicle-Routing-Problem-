import random
import math
import csv



#ID,XCOORD,YCOORD,DEMAND,UNLOADING_TIME
class Nodes:
    def __init__(self,id,xcoord,ycoord,demand,unload_time):
        self.matrix = []
        self.id = id
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.demand = demand
        unload_time = unload_time
        
    

clients=[]
nodes=[]
def buildModel():
        rows = len(nodes)
        matrix = [[0.0 for x in range(0,101)] for y in range(0,101)]
        #CREATE ARRAY OF COSTS
        for i in range(0, len(nodes)):
            a = nodes[i]
            for j in range(0, len(nodes)):
                b = nodes[j]
                dist = math.sqrt(math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2))
                matrix[i][j] = dist
        return matrix
    
def get_Data():
        # 0,35,35,0,0
        #wh = Node(0,35,35,0,0)
        f = open("data2.txt", "r")
        reader=csv.reader(f)
        i=0
        for row in reader:
           print(row[1])
           cust = (Nodes(row[0],row[1],row[2],row[3],row[4]))
           clients.append(cust)
           nodes.append(cust)
           i=i+1

get_Data()
buildModel()           
       
    
        
  
    

    
    
    
    

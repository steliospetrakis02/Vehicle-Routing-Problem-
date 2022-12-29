from VRP_Model import *
from SolutionDrawer import *


class Solution:
    def __init__(self):
        self.cost = 0.0
        self.routes = []
        self.test_routes = []
     
class Solver:
    def __init__(self, m):
        self.allNodes = m.allNodes
        self.customers = m.customers
        self.depot = m.allNodes[0]
        self.distanceMatrix = m.matrix
        self.capacity = m.capacity
        self.sol = None
        self.bestSolution = None

    def solve(self):
        self.SetRoutedFlagToFalseForAllCustomers()
        self.sol=self.start_all_routes()
        self.Solve(self.sol)
      
        self.ReportSolution(self.sol)
        return self.sol
   
    
    def SetRoutedFlagToFalseForAllCustomers(self):
        for i in range(0, len(self.customers)):
            self.customers[i].isRouted = False

        for c in self.customers:
            c.isRouted = False

    def ReportSolution(self, sol):
        f = open("res.txt", "w")
        f.write("Cost:")
        f.write("\n")
        f.write(str(self.sol.cost))
        f.write("\n")
        f.write("Routes:")
        f.write("\n")
        f.write(str(len(sol.routes)))
        f.write("\n")

        for i in range(0, len(sol.routes)):
            rt = sol.routes[i]
           # print(rt.sequenceOfNodes[0].ID, end=',')
            f.write(str(rt.sequenceOfNodes[0].ID))
            f.write(",")
            for j in range (0, len(rt.sequenceOfNodes)):
                if(rt.sequenceOfNodes[j].ID==0):
                    continue
                if(j == len(rt.sequenceOfNodes) - 1):    
                    print(rt.sequenceOfNodes[j].ID)
                    f.write(str(rt.sequenceOfNodes[j].ID))  
                    break
                
                print(rt.sequenceOfNodes[j].ID , end=",")
                f.write(str(rt.sequenceOfNodes[j].ID))
              
                f.write(",")
           
            f.write(" \n")
            
        SolDrawer.draw('Greedy', self.sol, self.allNodes)
       
        f.close()
    
    def ApplyNearestNeighborMethod(self,sol,route_number):
        
        indexOfTheNextCustomer = -1
        minimumInsertionCost = 1000000
        rt=sol.routes[route_number]
        lastNodeInTheCurrentSequence = rt.sequenceOfNodes[-1]
       
        
        for j in range (0, len(self.customers)):
            candidate = self.customers[j]
            if candidate.isRouted == True:
                continue
            
            trialCost = self.distanceMatrix[lastNodeInTheCurrentSequence.ID][candidate.ID]
            if(trialCost==0):
                continue
            
            if (trialCost < minimumInsertionCost):
                indexOfTheNextCustomer = j
                minimumInsertionCost = trialCost
        
        insertedCustomer = self.customers[indexOfTheNextCustomer]
      
        rt.sequenceOfNodes.append(insertedCustomer)
        
        insertedCustomer.isRouted = True
        return sol
    
    def find_best_route(self,sol,route_number):
        
        indexOfTheNextCustomer = -1
        minimumInsertionCost = 1000000
        rt=sol.test_routes[route_number]
        lastNodeInTheCurrentSequence = rt.sequenceOfNodes[-1]
       
        
        for j in range (0, len(self.customers)):
            candidate = self.customers[j]
            if candidate.isRouted == True:
                continue
            
            trialCost = self.distanceMatrix[lastNodeInTheCurrentSequence.ID][candidate.ID]
            if(trialCost==0):
                continue
            
            if (trialCost < minimumInsertionCost):
                indexOfTheNextCustomer = j
                minimumInsertionCost = trialCost
        
        insertedCustomer = self.customers[indexOfTheNextCustomer]
      
        rt.sequenceOfNodes.append(insertedCustomer)
        
        #self.ReportSolution(sol)
        possible_route=self.CalculateTotalCost(sol)
        rt.sequenceOfNodes.pop()
     
        return possible_route

    def start_all_routes(self):
        s = Solution()
        for i in range(14):
            rt = Route(self.depot, self.capacity)
            s.routes.append(rt)
            s.test_routes.append(rt)

        return s
    
    
    def CalculateTotalCost(self, sol):
        total_cost = 0
        for i in range(len(sol.routes)):
            rt = sol.routes[i]
            tot_time = 0       
            rt_cumulative_cost = 0
            for j in range(0,len(rt.sequenceOfNodes) - 1):
                         
                from_node = rt.sequenceOfNodes[j]            
                to_node = rt.sequenceOfNodes[j + 1]            
                tot_time += self.distanceMatrix[from_node.ID][to_node.ID]            
                rt_cumulative_cost += tot_time            
                tot_time += to_node.unload_time
                       
            total_cost += rt_cumulative_cost    
        return total_cost
    
   
    
    def Solve(self,sol):
        
        for i in range(len(self.customers)):
            max_obj=100000000
            for j in range(14):
               
                s=self.find_best_route(sol,j)
             
                if(s<max_obj):
                    max_obj=s
                    index=j
       
            self.ApplyNearestNeighborMethod(sol,index)
        
        sol.cost = self.CalculateTotalCost(sol)
  


m = Model()
m.BuildModel()
s = Solver(m)
sol = s.solve()

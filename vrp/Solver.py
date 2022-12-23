from VRP_Model import *
from SolutionDrawer import *


class Solution:
    def __init__(self):
        self.cost = 0.0
        self.routes = []
     

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
      
        for i in range(0, len(sol.routes)):
            rt = sol.routes[i]
            print(rt.sequenceOfNodes[0].ID, end=',')
            for j in range (0, len(rt.sequenceOfNodes)):
                
                if(rt.sequenceOfNodes[j].ID==0):
                    continue
                if(rt.sequenceOfNodes[j].ID==100):
                    continue
                print(rt.sequenceOfNodes[j].ID, end=',')   

                
            print(" ")
            
        SolDrawer.draw('MinIns', self.sol, self.allNodes)
        print(self.sol.cost)
    
    
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

    def start_all_routes(self):
        s = Solution()
        for i in range(14):
            rt = Route(self.depot, self.capacity)
            s.routes.append(rt)

        return s
    
    def distance(from_node, to_node):
        dx = from_node.x - to_node.x
        dy = from_node.y - to_node.y
        dist = math.sqrt(dx ** 2 + dy ** 2)
        return dist
  
    
    def calc_objective(self,nodes_sequence):
        
      rt_cumulative_cost = 0
      tot_time = 0
      for i in range(len(nodes_sequence) - 1):
          from_node = nodes_sequence[i]
          to_node = nodes_sequence[i+1]
          tot_time += self.distance(from_node, to_node)
          rt_cumulative_cost += tot_time
          tot_time += to_node.serv_tim
          
      return rt_cumulative_cost
    
    def Solve(self,sol):
        max_obj=100000000
        for i in range(len(self.customers)):
            
            for j in range(14):
                #s=self.calc_objective()
                self.ApplyNearestNeighborMethod(sol,j)

        
    def CalculateTotalCost(self, sol):
        c = 0
        for i in range(0, len(sol.sol)):
            rt = sol.routes[i]
            for j in range(0, len(rt.sequenceOfNodes) - 1):
                a = rt.sequenceOfNodes[j]
                b = rt.sequenceOfNodes[j + 1]
                c += self.distanceMatrix[a.ID][b.ID]
        return c



m = Model()
m.BuildModel()
s = Solver(m)
sol = s.solve()

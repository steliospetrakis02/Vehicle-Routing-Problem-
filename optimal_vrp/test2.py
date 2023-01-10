from VRP_Model import *
from SolutionDrawer import *


class Solution:
    def __init__(self):
        self.cost = 0.0
        self.routes = []


class RelocationMove(object):
    def __init__(self):
        self.originRoutePosition = None
        self.targetRoutePosition = None
        self.originNodePosition = None
        self.targetNodePosition = None
        self.costChangeOriginRt = None
        self.costChangeTargetRt = None
        self.moveCost = None

    def Initialize(self):
        self.originRoutePosition = None
        self.targetRoutePosition = None
        self.originNodePosition = None
        self.targetNodePosition = None
        self.costChangeOriginRt = None
        self.costChangeTargetRt = None
        self.moveCost = 10 ** 9

class SwapMove(object):
    def __init__(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.costChangeFirstRt = None
        self.costChangeSecondRt = None
        self.moveCost = None

    def Initialize(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.costChangeFirstRt = None
        self.costChangeSecondRt = None
        self.moveCost = 10 ** 9

class TwoOptMove(object):
    def __init__(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.moveCost = None
    def Initialize(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.moveCost = 10 ** 9


class CustomerInsertion(object):
    def __init__(self):
        self.customer = None
        self.route = None
        self.cost = 10 ** 9

class CustomerInsertionAllPositions(object):
    def __init__(self):
        self.customer = None
        self.route = None
        self.insertionPosition = None
        self.cost = 10 ** 9


class Solver:
    def __init__(self, m):
        self.allNodes = m.allNodes
        self.customers = m.customers
        self.depot = m.allNodes[0]
        self.distance_matrix = m.matrix
        self.capacity = m.capacity
        self.sol = None
        self.bestSolution = None
        rows = len(self.allNodes)
        self.distance_matrix_penalized = [[self.distance_matrix[i][j] for j in range(rows)] for i in range(rows)]
        self.times_penalized = [[0 for j in range(rows)] for i in range(rows)]
        self.penalized_n1_ID = -1
        self.penalized_n2_ID = -1

    def solve(self):
        self.SetRoutedFlagToFalseForAllCustomers()
        self.sol = self.start_all_routes()
        self.Solve(self.sol)
       
        self.ReportSolution(self.sol)
    
        random.seed(109)
        obj2=self.CalculateTotalCost(self.sol)
        for i in range(4):
            self.VNS2()
            self.exhange_last_route()   
        random.seed(109)

        for i in range(60):
                
                random_route=random.randint(0,13)
                random_route2=random.randint(0,13)
                rt1= self.sol.routes[random_route]
                rt2= self.sol.routes[random_route2]
                
                min1=len(rt1.sequenceOfNodes)
                min2=len(rt2.sequenceOfNodes)
                min_=min(min1,min2)
                random_customer_Indx=random.randint(1,(min_)-2)
                random_customer2_Indx=random.randint(1,(min_)-2)   
                random_customer=rt1.sequenceOfNodes[random_customer_Indx]
                random_customer2=rt2.sequenceOfNodes[random_customer2_Indx]
                B = random_customer

                if rt1 != rt2:
                    while(rt2.load + B.demand > rt2.capacity):
                        random_route=random.randint(0,13)
                        random_route2=random.randint(0,13)
                        rt1= self.sol.routes[random_route]
                        rt2= self.sol.routes[random_route2]
                        min1=len(rt1.sequenceOfNodes)
                        min2=len(rt2.sequenceOfNodes)
                        min_=min(min1,min2)
                        random_customer_Indx=random.randint(1,(min_)-2)
                        random_customer2_Indx=random.randint(1,(min_)-2)   
                        random_customer=rt1.sequenceOfNodes[random_customer_Indx]
                        random_customer2=rt2.sequenceOfNodes[random_customer2_Indx]
                        B = random_customer
                    
                    self.swapPositions(rt1.sequenceOfNodes,rt2.sequenceOfNodes,random_customer_Indx,random_customer2_Indx)
                else:
                    self.swapPositions(rt1.sequenceOfNodes,rt2.sequenceOfNodes,random_customer_Indx,random_customer2_Indx)      
    
                for i in range(4):
                    self.VNS()
                    self.exhange_last_route()   

                obj=self.CalculateTotalCost(self.sol)
                if (obj < obj2):
                    obj2=obj
                    self.sol.cost=obj
                    self.bestSolution.cost=obj
                    self.bestSolution = self.cloneSolution(self.sol)
                    self.ReportSolution(self.sol)
        print("objectakias")
        print(obj2)
        return self.sol
    
    def exhange_last_route(self):
        obj=self.CalculateTotalCost(self.sol)
        for i in range(0,len(self.sol.routes)):
            #self.ReportSolution(self.sol)
            currenct_route=self.sol.routes[i]
            
            for j in range(0,len(self.sol.routes)):
                exchanged_route=self.sol.routes[j]
                
                obj=self.CalculateTotalCost(self.sol)
                poped_element = currenct_route.sequenceOfNodes.pop()
                exchanged_route.sequenceOfNodes.append(poped_element)
                obj2=self.CalculateTotalCost(self.sol)
                if(obj2< obj):
                    pass
                    #sol better
                else:
                    currenct_route.sequenceOfNodes.append(poped_element)
                    exchanged_route.sequenceOfNodes.pop()
                
            
    def start_all_routes(self):
        s = Solution()
       
        number_of_trucks = 14
        for i in range(number_of_trucks):
            rt = Route(self.depot, 200)
        
            s.routes.append(rt)
  
        return s
    
    def Solve(self, sol):
            
        for i in range(len(self.customers)):
            max_obj = 100000000  # min?
            for j in range(len(self.sol.routes)):
                s = self.find_best_route(sol, j)
                if (s < max_obj):
                    max_obj = s
                    index = j
            
            self.ApplyNearestNeighborMethod(sol, index)
        rt=sol.routes[0]
        rt.sequenceOfNodes.pop(2)
        sol.cost = self.CalculateTotalCost(sol)
        print("Cost: ", sol.cost)
        
    def SetRoutedFlagToFalseForAllCustomers(self):
        for i in range(0, len(self.customers)):
            self.customers[i].isRouted = False
            
    def CalculateTotalCost(self, sol):
        total_cost = 0
        for i in range(len(sol.routes)):
            rt = sol.routes[i]
            tot_time = 0       
            rt_cumulative_cost = 0
            for j in range(len(rt.sequenceOfNodes) - 1):
                
                from_node = rt.sequenceOfNodes[j]            
                to_node = rt.sequenceOfNodes[j + 1]
                tot_time += self.distance_matrix[from_node.ID][to_node.ID]
                rt_cumulative_cost += tot_time
                tot_time += to_node.unload_time
            total_cost += rt_cumulative_cost
        return total_cost
    
    def ApplyNearestNeighborMethod(self,sol,route_number):
        
        indexOfTheNextCustomer = -1
        minimumInsertionCost = 1000000
        rt = sol.routes[route_number]
        lastNodeInTheCurrentSequence = rt.sequenceOfNodes[-1]
        
        
        for j in range (0, len(self.customers)):
            candidate = self.customers[j]
            if candidate.isRouted == True:
                continue
            
            trialCost = self.distance_matrix[lastNodeInTheCurrentSequence.ID][candidate.ID]
            if(trialCost == 0):
                continue
           
            if (trialCost < minimumInsertionCost):
                indexOfTheNextCustomer = j
                minimumInsertionCost = trialCost

        insertedCustomer = self.customers[indexOfTheNextCustomer]
        
       
        rt.sequenceOfNodes.append(insertedCustomer)

        insertedCustomer.isRouted = True
        
        return sol
    
        
    def create_random_cust(self):
        random_route=random.randint(0,13)
        random_route2=random.randint(0,13)
        rt1= self.sol.routes[random_route]
        rt2= self.sol.routes[random_route2]
        random_customer_Indx=random.randint(1,len(rt1.sequenceOfNodes)-1)
        random_customer2_Indx=random.randint(1,len(rt2.sequenceOfNodes)-1)   
        random_customer=rt1.sequenceOfNodes[random_customer_Indx]
        random_customer2=rt2.sequenceOfNodes[random_customer2_Indx]
        B = random_customer

        return rt1,rt2,random_customer,random_customer_Indx,random_customer2_Indx
        
    def VNS2(self):
        obj2=self.CalculateTotalCost(self.sol)
        self.bestSolution = self.cloneSolution(self.sol)
        terminationCondition = False
        rm = RelocationMove()
        sm = SwapMove()
        top=TwoOptMove()
        random.seed(109)
        while terminationCondition is False:
            operator=random.randint(0,2)
            self.InitializeOperators(rm, sm, top)
            #SolDrawer.draw(localSearchIterator, self.sol, self.allNodes)

            # Relocations
            if operator == 0:
                self.FindBestRelocationMove(rm)
                if rm.originRoutePosition is not None:
                    if rm.moveCost < 0:
                        self.ApplyRelocationMove(rm)
                    else:
                        terminationCondition = True
            # Swaps
            elif operator == 1:
                self.FindBestSwapMove(sm)
                if sm.positionOfFirstRoute is not None:
                    if sm.moveCost < 0:
                        self.ApplySwapMove(sm)
                    else:
                        terminationCondition = True
            elif operator == 2:
                self.FindBestTwoOptMove(top)
                if top.positionOfFirstRoute is not None:
                    if top.moveCost < 0:
                        self.ApplyTwoOptMove(top)
                    else:
                        terminationCondition = True

            obj=self.CalculateTotalCost(self.sol)
            if (self.sol.cost < self.bestSolution.cost): 
                self.bestSolution = self.cloneSolution(self.sol)
            #if (self.sol.cost < self.bestSolution.cost):
                #self.bestSolution = self.cloneSolution(self.sol)
         
           
        self.sol = self.bestSolution
    
    def VNS(self):
        obj2=self.CalculateTotalCost(self.sol)
        self.bestSolution = self.cloneSolution(self.sol)
        terminationCondition = False
        rm = RelocationMove()
        sm = SwapMove()
        top=TwoOptMove()
       
        while terminationCondition is False:
            operator=random.randint(0,2)
            self.InitializeOperators(rm, sm, top)
            #SolDrawer.draw(localSearchIterator, self.sol, self.allNodes)

            # Relocations
            if operator == 0:
                self.FindBestRelocationMove(rm)
                if rm.originRoutePosition is not None:
                    if rm.moveCost < 0:
                        self.ApplyRelocationMove(rm)
                    else:
                        terminationCondition = True
            # Swaps
            elif operator == 1:
                self.FindBestSwapMove(sm)
                if sm.positionOfFirstRoute is not None:
                    if sm.moveCost < 0:
                        self.ApplySwapMove(sm)
                    else:
                        terminationCondition = True
            elif operator == 2:
                self.FindBestTwoOptMove(top)
                if top.positionOfFirstRoute is not None:
                    if top.moveCost < 0:
                        self.ApplyTwoOptMove(top)
                    else:
                        terminationCondition = True

            obj=self.CalculateTotalCost(self.sol)
            if (self.sol.cost < self.bestSolution.cost): 
                self.bestSolution = self.cloneSolution(self.sol)
            #if (self.sol.cost < self.bestSolution.cost):
                #self.bestSolution = self.cloneSolution(self.sol)
         
           
        self.sol = self.bestSolution
        
    def swapPositions(self,list_of_nodes1,list_of_nodes2 ,pos1, pos2):
        first_ele = list_of_nodes1.pop(pos1)  
        second_ele = list_of_nodes2.pop(pos2)
        list_of_nodes1.insert(pos1, second_ele) 
        list_of_nodes2.insert(pos2, first_ele)
        
        if(pos1==1):
            fourth=list_of_nodes1.pop(pos1+1)
        else:
            fourth=list_of_nodes1.pop(pos1-1)
        if(pos2==1):
            third_elem=list_of_nodes2.pop(pos2+1)
        else:
            third_elem=list_of_nodes2.pop(pos2-1)
         
        if(pos1==1):
            list_of_nodes1.insert(pos1+1, third_elem) 
        else:
            list_of_nodes2.insert(pos1-1, third_elem)
        if(pos2==1):
            list_of_nodes2.insert(pos2+1, fourth)
        else:
            list_of_nodes2.insert(pos2-1, fourth)
        print("-")
       # self.ReportSolution(self.sol)
        print("-")
           
        
        
        
    def cloneRoute(self, rt: Route):
        cloned = Route(self.depot, self.capacity)
        cloned.cost = rt.cost
        cloned.load = rt.load
        cloned.sequenceOfNodes = rt.sequenceOfNodes.copy()
        return cloned

    def cloneSolution(self, sol: Solution):
        cloned = Solution()
        for i in range(0, len(sol.routes)):
            rt = sol.routes[i]
            clonedRoute = self.cloneRoute(rt)
            cloned.routes.append(clonedRoute)
        cloned.cost = self.sol.cost
        return cloned

    def FindBestRelocationMove(self, rm):
        for originRouteIndex in range(1, len(self.sol.routes)):
            rt1:Route = self.sol.routes[originRouteIndex]
            for targetRouteIndex in range (1, len(self.sol.routes)):
                rt2:Route = self.sol.routes[targetRouteIndex]
                for originNodeIndex in range (1, len(rt1.sequenceOfNodes) - 2):
                    for targetNodeIndex in range (0, len(rt2.sequenceOfNodes) - 2):
                        
                        if originRouteIndex == targetRouteIndex and (targetNodeIndex == originNodeIndex or targetNodeIndex == originNodeIndex - 1):
                            continue

                        A = rt1.sequenceOfNodes[originNodeIndex - 1]
                        B = rt1.sequenceOfNodes[originNodeIndex]
                        C = rt1.sequenceOfNodes[originNodeIndex + 1]

                        F = rt2.sequenceOfNodes[targetNodeIndex]
                        G = rt2.sequenceOfNodes[targetNodeIndex + 1]

                        if rt1 != rt2:
                            if rt2.load + B.demand > rt2.capacity:
                                continue

                        costAdded = self.distance_matrix[A.ID][C.ID] + self.distance_matrix[F.ID][B.ID] + self.distance_matrix[B.ID][G.ID]
                        costRemoved = self.distance_matrix[A.ID][B.ID] + self.distance_matrix[B.ID][C.ID] + self.distance_matrix[F.ID][G.ID]

                        originRtCostChange = self.distance_matrix[A.ID][C.ID] - self.distance_matrix[A.ID][B.ID] - self.distance_matrix[B.ID][C.ID]
                        targetRtCostChange = self.distance_matrix[F.ID][B.ID] + self.distance_matrix[B.ID][G.ID] - self.distance_matrix[F.ID][G.ID]

                        moveCost = costAdded - costRemoved

                        if (moveCost < rm.moveCost) and abs(moveCost) > 0.0001:

                            self.StoreBestRelocationMove(originRouteIndex, targetRouteIndex, originNodeIndex, targetNodeIndex, moveCost, originRtCostChange, targetRtCostChange, rm)

        return rm.originRoutePosition
    
    def find_best_route(self, sol, route_number):
            
        indexOfTheNextCustomer = -1
        minimumInsertionCost = 1000000
        rt = sol.routes[route_number]
        lastNodeInTheCurrentSequence = rt.sequenceOfNodes[-1]

        for j in range (0, len(self.customers)):
            candidate = self.customers[j]
            if candidate.isRouted == True:
                continue
            
            trialCost = self.distance_matrix[lastNodeInTheCurrentSequence.ID][candidate.ID]
            if(trialCost == 0):
                continue
            
            if (trialCost < minimumInsertionCost):
                indexOfTheNextCustomer = j
                minimumInsertionCost = trialCost

        insertedCustomer = self.customers[indexOfTheNextCustomer]
        rt.sequenceOfNodes.append(insertedCustomer)

        possible_route = self.CalculateTotalCost(sol)
        rt.sequenceOfNodes.pop()
     
        return possible_route
    
    def FindBestSwapMove(self, sm):
        for firstRouteIndex in range(0, len(self.sol.routes)):
            rt1:Route = self.sol.routes[firstRouteIndex]
            for secondRouteIndex in range (firstRouteIndex, len(self.sol.routes)):
                rt2:Route = self.sol.routes[secondRouteIndex]
                for firstNodeIndex in range (1, len(rt1.sequenceOfNodes) - 1):
                    startOfSecondNodeIndex = 1
                    if rt1 == rt2:
                        startOfSecondNodeIndex = firstNodeIndex + 1
                    for secondNodeIndex in range (startOfSecondNodeIndex, len(rt2.sequenceOfNodes) - 1):

                        a1 = rt1.sequenceOfNodes[firstNodeIndex - 1]
                        b1 = rt1.sequenceOfNodes[firstNodeIndex]
                        c1 = rt1.sequenceOfNodes[firstNodeIndex + 1]

                        a2 = rt2.sequenceOfNodes[secondNodeIndex - 1]
                        b2 = rt2.sequenceOfNodes[secondNodeIndex]
                        c2 = rt2.sequenceOfNodes[secondNodeIndex + 1]



                        moveCost = None
                        costChangeFirstRoute = None
                        costChangeSecondRoute = None

                        if rt1 == rt2:
                            if firstNodeIndex == secondNodeIndex - 1:
                                costRemoved = self.distance_matrix[a1.ID][b1.ID] + self.distance_matrix[b1.ID][b2.ID] + self.distance_matrix[b2.ID][c2.ID]
                                costAdded = self.distance_matrix[a1.ID][b2.ID] + self.distance_matrix[b2.ID][b1.ID] + self.distance_matrix[b1.ID][c2.ID]
                                moveCost = costAdded - costRemoved
                            else:

                                costRemoved1 = self.distance_matrix[a1.ID][b1.ID] + self.distance_matrix[b1.ID][c1.ID]
                                costAdded1 = self.distance_matrix[a1.ID][b2.ID] + self.distance_matrix[b2.ID][c1.ID]
                                costRemoved2 = self.distance_matrix[a2.ID][b2.ID] + self.distance_matrix[b2.ID][c2.ID]
                                costAdded2 = self.distance_matrix[a2.ID][b1.ID] + self.distance_matrix[b1.ID][c2.ID]
                                moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                        else:
                            if rt1.load - b1.demand + b2.demand > self.capacity:
                                continue
                            if rt2.load - b2.demand + b1.demand > self.capacity:
                                continue

                            costRemoved1 = self.distance_matrix[a1.ID][b1.ID] + self.distance_matrix[b1.ID][c1.ID]
                            costAdded1 = self.distance_matrix[a1.ID][b2.ID] + self.distance_matrix[b2.ID][c1.ID]
                            costRemoved2 = self.distance_matrix[a2.ID][b2.ID] + self.distance_matrix[b2.ID][c2.ID]
                            costAdded2 = self.distance_matrix[a2.ID][b1.ID] + self.distance_matrix[b1.ID][c2.ID]

                            costChangeFirstRoute = costAdded1 - costRemoved1
                            costChangeSecondRoute = costAdded2 - costRemoved2

                            moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                        if moveCost < sm.moveCost and abs(moveCost) > 0.0001:
                            self.StoreBestSwapMove(firstRouteIndex, secondRouteIndex, firstNodeIndex, secondNodeIndex, moveCost, costChangeFirstRoute, costChangeSecondRoute, sm)
    
    def ApplyRelocationMove(self, rm: RelocationMove):

        oldCost = self.CalculateTotalCost(self.sol)

        originRt = self.sol.routes[rm.originRoutePosition]
        targetRt = self.sol.routes[rm.targetRoutePosition]

        B = originRt.sequenceOfNodes[rm.originNodePosition]

        if originRt == targetRt:
            del originRt.sequenceOfNodes[rm.originNodePosition]
            if (rm.originNodePosition < rm.targetNodePosition):
                targetRt.sequenceOfNodes.insert(rm.targetNodePosition, B)
            else:
                targetRt.sequenceOfNodes.insert(rm.targetNodePosition + 1, B)

            originRt.cost += rm.moveCost
        else:
            del originRt.sequenceOfNodes[rm.originNodePosition]
            targetRt.sequenceOfNodes.insert(rm.targetNodePosition + 1, B)
            originRt.cost += rm.costChangeOriginRt
            targetRt.cost += rm.costChangeTargetRt
            originRt.load -= B.demand
            targetRt.load += B.demand

        self.sol.cost += rm.moveCost

        newCost = self.CalculateTotalCost(self.sol)
        

    def ApplySwapMove(self, sm):
        oldCost = self.CalculateTotalCost(self.sol)
        rt1 = self.sol.routes[sm.positionOfFirstRoute]
        rt2 = self.sol.routes[sm.positionOfSecondRoute]
        b1 = rt1.sequenceOfNodes[sm.positionOfFirstNode]
        b2 = rt2.sequenceOfNodes[sm.positionOfSecondNode]
        rt1.sequenceOfNodes[sm.positionOfFirstNode] = b2
        rt2.sequenceOfNodes[sm.positionOfSecondNode] = b1

        if (rt1 == rt2):
            rt1.cost += sm.moveCost
        else:
            rt1.cost += sm.costChangeFirstRt
            rt2.cost += sm.costChangeSecondRt
            rt1.load = rt1.load - b1.demand + b2.demand
            rt2.load = rt2.load + b1.demand - b2.demand

        self.sol.cost += sm.moveCost

        newCost = self.CalculateTotalCost(self.sol)
        
    def ReportSolution(self, sol):
        obj = self.CalculateTotalCost(self.sol)
        f = open("res.txt", "w")
        f.write("Cost:")
        f.write("\n")
        f.write(str(obj))
        f.write("\n")
        f.write("Routes:")
        f.write("\n")
        f.write(str(len(sol.routes)))
        f.write("\n")
      
        for i in range(0, len(sol.routes)):
            rt = sol.routes[i]
           
            for j in range (0, len(rt.sequenceOfNodes)):
                
                if(j == len(rt.sequenceOfNodes) - 1):    
                    print(rt.sequenceOfNodes[j].ID)
                    f.write(str(rt.sequenceOfNodes[j].ID))  
                    break
                
                print(rt.sequenceOfNodes[j].ID , end=",")
                f.write(str(rt.sequenceOfNodes[j].ID))
                f.write(",")
           
            f.write(" \n")
                
            
        SolDrawer.draw('Optimal', self.sol, self.allNodes)
        
        f.close()
    
    def StoreBestRelocationMove(self, originRouteIndex, targetRouteIndex, originNodeIndex, targetNodeIndex, moveCost,
                                 originRtCostChange, targetRtCostChange, rm: RelocationMove):
        rm.originRoutePosition = originRouteIndex
        rm.originNodePosition = originNodeIndex
        rm.targetRoutePosition = targetRouteIndex
        rm.targetNodePosition = targetNodeIndex
        rm.costChangeOriginRt = originRtCostChange
        rm.costChangeTargetRt = targetRtCostChange
        rm.moveCost = moveCost

    def StoreBestSwapMove(self, firstRouteIndex, secondRouteIndex, firstNodeIndex, secondNodeIndex, moveCost,
                           costChangeFirstRoute, costChangeSecondRoute, sm):
        sm.positionOfFirstRoute = firstRouteIndex
        sm.positionOfSecondRoute = secondRouteIndex
        sm.positionOfFirstNode = firstNodeIndex
        sm.positionOfSecondNode = secondNodeIndex
        sm.costChangeFirstRt = costChangeFirstRoute
        sm.costChangeSecondRt = costChangeSecondRoute
        sm.moveCost = moveCost

    
    def InitializeOperators(self, rm, sm,top):
        rm.Initialize()
        sm.Initialize()
        top.Initialize()


    def FindBestTwoOptMove(self, top):
        for rtInd1 in range(0, len(self.sol.routes)):
            rt1: Route = self.sol.routes[rtInd1]
            for rtInd2 in range(rtInd1, len(self.sol.routes)):
                rt2: Route = self.sol.routes[rtInd2]
                for nodeInd1 in range(0, len(rt1.sequenceOfNodes) - 2):
                    start2 = 0
                    if (rt1 == rt2):
                        start2 = nodeInd1 + 2
                    for nodeInd2 in range(start2, len(rt2.sequenceOfNodes) - 2):
                        moveCost = 10 ** 9

                        A = rt1.sequenceOfNodes[nodeInd1]
                        B = rt1.sequenceOfNodes[nodeInd1 + 1]
                        K = rt2.sequenceOfNodes[nodeInd2]
                        L = rt2.sequenceOfNodes[nodeInd2 + 1]

                        if rt1 == rt2:
                            if nodeInd1 == 0 and nodeInd2 == len(rt1.sequenceOfNodes) - 2:
                                continue
                            costAdded = self.distance_matrix[A.ID][K.ID] + self.distance_matrix[B.ID][L.ID]
                            costRemoved = self.distance_matrix[A.ID][B.ID] + self.distance_matrix[K.ID][L.ID]
                            moveCost = costAdded - costRemoved
                        else:
                            if nodeInd1 == 0 and nodeInd2 == 0:
                                continue
                            if nodeInd1 == len(rt1.sequenceOfNodes) - 2 and nodeInd2 == len(rt2.sequenceOfNodes) - 2:
                                continue

                            if self.CapacityIsViolated(rt1, nodeInd1, rt2, nodeInd2):
                                continue
                            costAdded = self.distance_matrix[A.ID][L.ID] + self.distance_matrix[B.ID][K.ID]
                            costRemoved = self.distance_matrix[A.ID][B.ID] + self.distance_matrix[K.ID][L.ID]
                            moveCost = costAdded - costRemoved
                        if moveCost < top.moveCost:
                            self.StoreBestTwoOptMove(rtInd1, rtInd2, nodeInd1, nodeInd2, moveCost, top)


    def CapacityIsViolated(self, rt1, nodeInd1, rt2, nodeInd2):

        rt1FirstSegmentLoad = 0
        for i in range(0, nodeInd1 + 1):
            n = rt1.sequenceOfNodes[i]
            rt1FirstSegmentLoad += n.demand
        rt1SecondSegmentLoad = rt1.load - rt1FirstSegmentLoad

        rt2FirstSegmentLoad = 0
        for i in range(0, nodeInd2 + 1):
            n = rt2.sequenceOfNodes[i]
            rt2FirstSegmentLoad += n.demand
        rt2SecondSegmentLoad = rt2.load - rt2FirstSegmentLoad

        if (rt1FirstSegmentLoad + rt2SecondSegmentLoad > rt1.capacity):
            return True
        if (rt2FirstSegmentLoad + rt1SecondSegmentLoad > rt2.capacity):
            return True

        return False

    def StoreBestTwoOptMove(self, rtInd1, rtInd2, nodeInd1, nodeInd2, moveCost, top):
        top.positionOfFirstRoute = rtInd1
        top.positionOfSecondRoute = rtInd2
        top.positionOfFirstNode = nodeInd1
        top.positionOfSecondNode = nodeInd2
        top.moveCost = moveCost

    def ApplyTwoOptMove(self, top):
            
        rt1: Route = self.sol.routes[top.positionOfFirstRoute]
        rt2: Route = self.sol.routes[top.positionOfSecondRoute]

        if rt1 == rt2:
            # reverses the nodes in the segment [positionOfFirstNode + 1,  top.positionOfSecondNode]
            reversedSegment = reversed(rt1.sequenceOfNodes[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1])
            # lst = list(reversedSegment)
            # lst2 = list(reversedSegment)
            rt1.sequenceOfNodes[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1] = reversedSegment

            # reversedSegmentList = list(reversed(rt1.sequenceOfNodes[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1]))
            # rt1.sequenceOfNodes[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1] = reversedSegmentList

            rt1.cost += top.moveCost

        else:
            # slice with the nodes from position top.positionOfFirstNode + 1 onwards
            relocatedSegmentOfRt1 = rt1.sequenceOfNodes[top.positionOfFirstNode + 1:]

            # slice with the nodes from position top.positionOfFirstNode + 1 onwards
            relocatedSegmentOfRt2 = rt2.sequenceOfNodes[top.positionOfSecondNode + 1:]

            del rt1.sequenceOfNodes[top.positionOfFirstNode + 1:]
            del rt2.sequenceOfNodes[top.positionOfSecondNode + 1:]

            rt1.sequenceOfNodes.extend(relocatedSegmentOfRt2)
            rt2.sequenceOfNodes.extend(relocatedSegmentOfRt1)

            self.UpdateRouteCostAndLoad(rt1)
            self.UpdateRouteCostAndLoad(rt2)

        self.sol.cost += top.moveCost

    def UpdateRouteCostAndLoad(self, rt: Route):
        tc = 0
        tl = 0
        for i in range(0, len(rt.sequenceOfNodes) - 1):
            A = rt.sequenceOfNodes[i]
            B = rt.sequenceOfNodes[i + 1]
            tc += self.distance_matrix[A.ID][B.ID]
            tl += A.demand
        rt.load = tl
        rt.cost = tc


m = Model()
m.BuildModel()
s = Solver(m)
sol = s.solve()
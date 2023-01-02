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
        
        
class Solver:
    def __init__(self, m):
        self.allNodes = m.allNodes
        self.customers = m.customers
        self.depot = m.allNodes[0]
        self.distanceMatrix = m.matrix
        self.capacity = m.capacity
        self.sol = None
        self.bestSolution = None
        self.searchTrajectory = []  
              
    def solve(self):
        
        self.SetRoutedFlagToFalseForAllCustomers()
        self.sol = self.start_all_routes()
        self.Solve(self.sol)
      
        self.ReportSolution(self.sol)
        self.VND()
        self.ReportSolution(self.sol)
        return self.sol
   
    
    def SetRoutedFlagToFalseForAllCustomers(self):
        
        for i in range(0, len(self.customers)):
            self.customers[i].isRouted = False

        for c in self.customers:
            c.isRouted = False
        
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
            
        SolDrawer.draw('Greedy', self.sol, self.allNodes)
       
        f.close()
        
    def cloneSolution(self, sol: Solution):
        cloned = Solution()
        for i in range (0, len(sol.routes)):
            rt = sol.routes[i]
            clonedRoute = self.cloneRoute(rt)
            cloned.routes.append(clonedRoute)
        cloned.cost = self.sol.cost
        return cloned
    
    def cloneRoute(self, rt:Route):
        cloned = Route(self.depot, self.capacity)
        cloned.cost = rt.cost
        cloned.load = rt.load
        cloned.sequenceOfNodes = rt.sequenceOfNodes.copy()
        return cloned
    
    def InitializeOperators(self, rm):
        rm.Initialize()
      #  sm.Initialize()
      #  top.Initialize()
        
    def FindBestRelocationMove(self, rm):
        print("e")
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
                                print("diplaaa")
                                continue

                        costAdded = self.distanceMatrix[A.ID][C.ID] + self.distanceMatrix[F.ID][B.ID] + self.distanceMatrix[B.ID][G.ID]
                        costRemoved = self.distanceMatrix[A.ID][B.ID] + self.distanceMatrix[B.ID][C.ID] + self.distanceMatrix[F.ID][G.ID]

                        originRtCostChange = self.distanceMatrix[A.ID][C.ID] - self.distanceMatrix[A.ID][B.ID] - self.distanceMatrix[B.ID][C.ID]
                        targetRtCostChange = self.distanceMatrix[F.ID][B.ID] + self.distanceMatrix[B.ID][G.ID] - self.distanceMatrix[F.ID][G.ID]

                        moveCost = costAdded - costRemoved

                        if (moveCost < rm.moveCost) and abs(moveCost) > 0.0001:

                            self.StoreBestRelocationMove(originRouteIndex, targetRouteIndex, originNodeIndex, targetNodeIndex, moveCost, originRtCostChange, targetRtCostChange, rm)

        return rm.originRoutePosition
    
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
        rt1:Route = self.sol.routes[top.positionOfFirstRoute]
        rt2:Route = self.sol.routes[top.positionOfSecondRoute]

        if rt1 == rt2:
            # reverses the nodes in the segment [positionOfFirstNode + 1,  top.positionOfSecondNode]
            reversedSegment = reversed(rt1.sequenceOfNodes[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1])
            #lst = list(reversedSegment)
            #lst2 = list(reversedSegment)
            rt1.sequenceOfNodes[top.positionOfFirstNode + 1 : top.positionOfSecondNode + 1] = reversedSegment

            #reversedSegmentList = list(reversed(rt1.sequenceOfNodes[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1]))
            #rt1.sequenceOfNodes[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1] = reversedSegmentList

            rt1.cost += top.moveCost

        else:
            #slice with the nodes from position top.positionOfFirstNode + 1 onwards
            relocatedSegmentOfRt1 = rt1.sequenceOfNodes[top.positionOfFirstNode + 1 :]

            #slice with the nodes from position top.positionOfFirstNode + 1 onwards
            relocatedSegmentOfRt2 = rt2.sequenceOfNodes[top.positionOfSecondNode + 1 :]

            del rt1.sequenceOfNodes[top.positionOfFirstNode + 1 :]
            del rt2.sequenceOfNodes[top.positionOfSecondNode + 1 :]

            rt1.sequenceOfNodes.extend(relocatedSegmentOfRt2)
            rt2.sequenceOfNodes.extend(relocatedSegmentOfRt1)

            self.UpdateRouteCostAndLoad(rt1)
            self.UpdateRouteCostAndLoad(rt2)

        self.sol.cost += top.moveCost
        self.TestSolution()
        
    def UpdateRouteCostAndLoad(self, rt: Route):
        tc = 0
        tl = 0
        for i in range(0, len(rt.sequenceOfNodes) - 1):
            A = rt.sequenceOfNodes[i]
            B = rt.sequenceOfNodes[i+1]
            tc += self.distanceMatrix[A.ID][B.ID]
            tl += A.demand
        rt.load = tl
        rt.cost = tc

    def TestSolution(self):
        self.CalculateTotalCost(self.sol)
        totalSolCost = 0
        for r in range (0, len(self.sol.routes)):
            rt: Route = self.sol.routes[r]
            rtCost = 0
            rtLoad = 0
            for n in range (0 , len(rt.sequenceOfNodes) - 1):
                A = rt.sequenceOfNodes[n]
                B = rt.sequenceOfNodes[n + 1]
                rtCost += self.distanceMatrix[A.ID][B.ID]
                rtLoad += A.demand
            if abs(rtCost - rt.cost) > 0.0001:
                print ('Route Cost problem')
            if rtLoad != rt.load:
                print ('Route Load problem')

            totalSolCost += rt.cost

        if abs(totalSolCost - self.sol.cost) > 0.0001:
            print('Solution Cost problem')
            
    def IdentifyBestInsertionAllPositions(self, bestInsertion, rt):
        for i in range(0, len(self.customers)):
            candidateCust: Node = self.customers[i]
            if candidateCust.isRouted is False:
                if rt.load + candidateCust.demand <= rt.capacity:
                    lastNodePresentInTheRoute = rt.sequenceOfNodes[-2]
                    for j in range(0, len(rt.sequenceOfNodes) - 1):
                        A = rt.sequenceOfNodes[j]
                        B = rt.sequenceOfNodes[j + 1]
                        costAdded = self.distanceMatrix[A.ID][candidateCust.ID] + self.distanceMatrix[candidateCust.ID][B.ID]
                        costRemoved = self.distanceMatrix[A.ID][B.ID]
                        trialCost = costAdded - costRemoved

                        if trialCost < bestInsertion.cost:
                            bestInsertion.customer = candidateCust
                            bestInsertion.route = rt
                            bestInsertion.cost = trialCost
                            bestInsertion.insertionPosition = j

    def ApplyCustomerInsertionAllPositions(self, insertion):
        insCustomer = insertion.customer
        rt = insertion.route
        # before the second depot occurrence
        insIndex = insertion.insertionPosition
        rt.sequenceOfNodes.insert(insIndex + 1, insCustomer)
        rt.cost += insertion.cost
        self.sol.cost += insertion.cost
        rt.load += insCustomer.demand
        insCustomer.isRouted = True
        
    def VND(self):
        self.bestSolution = self.cloneSolution(self.sol)
        VNDIterator = 0
        kmax = 1
        rm = RelocationMove()
       # sm = SwapMove()
       # top = TwoOptMove()
        k = 0
        draw = False

        while k < kmax:
            print(k)
            self.InitializeOperators(rm)
            if k == 0:
                self.FindBestRelocationMove(rm)
            
                if rm.originRoutePosition is not None and rm.moveCost < 0:
                    self.ApplyRelocationMove(rm)
                    
                    
                    if draw:
                       
                       SolDrawer.draw(VNDIterator, self.sol, self.allNodes)
                        
                        
                    VNDIterator = VNDIterator + 1
                    self.searchTrajectory.append(self.sol.cost)
                    k = 0
                else:
                    k += 1
           
        rt=self.sol.routes[0]
        print((rt.sequenceOfNodes[2].ID))
      #  print(len(sol.routes))
        k=0
        print("LASTTTTTTTTTT")
        for i in range(len(self.sol.routes)):
            rt=self.sol.routes[i]
            k=k+(len(rt.sequenceOfNodes))
        print(k)
        obj = self.CalculateTotalCost(self.sol)
        print("Cost: ", obj)
        SolDrawer.draw('final_vnd', self.bestSolution, self.allNodes)
       # SolDrawer.drawTrajectory(self.searchTrajectory)
        
        
        
    def ApplyNearestNeighborMethod(self,sol,route_number):
        
        indexOfTheNextCustomer = -1
        minimumInsertionCost = 1000000
        rt = sol.routes[route_number]
        lastNodeInTheCurrentSequence = rt.sequenceOfNodes[-1]
        
        
        for j in range (0, len(self.customers)):
            candidate = self.customers[j]
            if candidate.isRouted == True:
                continue
            
            trialCost = self.distanceMatrix[lastNodeInTheCurrentSequence.ID][candidate.ID]
            if(trialCost == 0):
                continue
           
            if (trialCost < minimumInsertionCost):
                indexOfTheNextCustomer = j
                minimumInsertionCost = trialCost

        insertedCustomer = self.customers[indexOfTheNextCustomer]
        
        
        rt.sequenceOfNodes.append(insertedCustomer)

        insertedCustomer.isRouted = True
        
        return sol
    
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

        self.TestSolution()
        
                                                                                                                    
    def find_best_route(self, sol, route_number):
        
        indexOfTheNextCustomer = -1
        minimumInsertionCost = 1000000
        rt = sol.routes[route_number]
        lastNodeInTheCurrentSequence = rt.sequenceOfNodes[-1]

        for j in range (0, len(self.customers)):
            candidate = self.customers[j]
            if candidate.isRouted == True:
                continue
            
            trialCost = self.distanceMatrix[lastNodeInTheCurrentSequence.ID][candidate.ID]
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
    
    def StoreBestRelocationMove(self, originRouteIndex, targetRouteIndex, originNodeIndex, targetNodeIndex, moveCost, originRtCostChange, targetRtCostChange, rm:RelocationMove):
        rm.originRoutePosition = originRouteIndex
        rm.originNodePosition = originNodeIndex
        rm.targetRoutePosition = targetRouteIndex
        rm.targetNodePosition = targetNodeIndex
        rm.costChangeOriginRt = originRtCostChange
        rm.costChangeTargetRt = targetRtCostChange
        rm.moveCost = moveCost
    
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
        

    def CalculateTotalCost(self, sol):
        total_cost = 0
        for i in range(len(sol.routes)):
            rt = sol.routes[i]
            tot_time = 0       
            rt_cumulative_cost = 0
            for j in range(len(rt.sequenceOfNodes) - 1):
                
                from_node = rt.sequenceOfNodes[j]            
                to_node = rt.sequenceOfNodes[j + 1]
                tot_time += self.distanceMatrix[from_node.ID][to_node.ID]
                rt_cumulative_cost += tot_time
                tot_time += to_node.unload_time
            total_cost += rt_cumulative_cost
        return total_cost

m = Model()
m.BuildModel()
s = Solver(m)
sol = s.solve()

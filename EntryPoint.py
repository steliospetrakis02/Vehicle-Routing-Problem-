from SolutionDrawer import *
from solultion import Model

class Solution:
    def __init__(self):
        self.cost = 0.0
        self.sequenceOfNodes = []


def SetRoutedFlagToFalseForAllCustomers(customers):
    for i in range (0, len(customers)):
        customers[i].isRouted = False


def ApplyNearestNeighborMethod(depot, customers, sol, distanceMatrix):
    sol.sequenceOfNodes.append(depot)
    for i in range (0, len(customers)):
        indexOfTheNextCustomer = -1
        minimumInsertionCost = 1000000
        lastIndexInSolution = len(sol.sequenceOfNodes) - 1
        lastNodeInTheCurrentSequence = sol.sequenceOfNodes[lastIndexInSolution]
        # lastNodeInTheCurrentSequence = sol.sequenceOfNodes[-1]
        for j in range (0, len(customers)):
            candidate = customers[j]
            if candidate.isRouted == True:
                continue
            trialCost = distanceMatrix[lastNodeInTheCurrentSequence.ID][candidate.ID]
            if (trialCost < minimumInsertionCost):
                indexOfTheNextCustomer = j
                minimumInsertionCost = trialCost

        insertedCustomer = customers[indexOfTheNextCustomer]
        sol.sequenceOfNodes.append(insertedCustomer)
        sol.cost += distanceMatrix[lastNodeInTheCurrentSequence.ID][insertedCustomer.ID]
        insertedCustomer.isRouted = True

    lastIndexInSolution = len(sol.sequenceOfNodes) - 1
    lastNodeInTheCurrentSequence = sol.sequenceOfNodes[lastIndexInSolution]
    sol.sequenceOfNodes.append(depot)
    sol.cost += distanceMatrix[lastNodeInTheCurrentSequence.ID][depot.ID]

def MinimumInsertions(depot, customers, sol, distanceMatrix):

    sol.sequenceOfNodes.append(depot)
    sol.sequenceOfNodes.append(depot)

    for i in range (0, len(customers)):
        indexOfTheNextCustomer = -1
        positionOfInsertion = -1
        minimumInsertionCost = 1000000

        for j in range(0, len(customers)):
            candidate = customers[j]
            if candidate.isRouted == True:
                continue
            for k in range(0, len(sol.sequenceOfNodes) - 1):
                before = sol.sequenceOfNodes[k]
                after = sol.sequenceOfNodes[k + 1]
                costAdded = distanceMatrix[before.ID][candidate.ID] + distanceMatrix[candidate.ID][after.ID]
                costRemoved = distanceMatrix[before.ID][after.ID]
                trialCost = costAdded - costRemoved
                if trialCost < minimumInsertionCost:
                    indexOfTheNextCustomer = j
                    positionOfInsertion = k
                    minimumInsertionCost = trialCost

        insertedCustomer = customers[indexOfTheNextCustomer]
        sol.sequenceOfNodes.insert(positionOfInsertion + 1, insertedCustomer)
        sol.cost += minimumInsertionCost
        insertedCustomer.isRouted = True
    a = 0

def ReportSolution(sol):
    for i in range (0, len(sol.sequenceOfNodes)):
        print(sol.sequenceOfNodes[i].ID, end = ' ')


def CheckSolution(sol, distanceMatrix):
    cst = 0
    print (sol.cost)
    for i in range(len(sol.sequenceOfNodes) - 1):
        a = sol.sequenceOfNodes[i]
        b = sol.sequenceOfNodes[i+1]
        cst += distanceMatrix[a.ID][b.ID]
    if (abs(cst - sol.cost) > 0.00001):
        print('Error')


def solve(m):
    allNodes = m.allNodes
    customers = m.customers
    depot = allNodes[0]
    distanceMatrix = m.matrix

    sol = Solution()

    SetRoutedFlagToFalseForAllCustomers(customers)
    #ApplyNearestNeighborMethod(depot, customers, sol, distanceMatrix)
    MinimumInsertions(depot, customers, sol, distanceMatrix)
    CheckSolution(sol, distanceMatrix)
    ReportSolution(sol)
    SolDrawer.draw(0, sol, allNodes)

m = Model()
m.BuildModel()
solve(m)





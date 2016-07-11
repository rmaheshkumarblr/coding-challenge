## Objectives :

# 1) Create a datastructure that resembles the requirement. (Node class)
# 2) Create a graph that is going to represent the transaction information. (Graph class)
# 3) Take the incoming data and use the two classes to obtain the output

import sys
import json
import dateutil.parser
from datetime import datetime, timedelta


class Node:
    '''
    Objective of this class is to create a basic infrastructure that resembles the requirement.
    '''
    def __init__(self,actor):
        '''
            actor indicates the actor himself
            targets indicates the targets the actor is connected to
        '''
        self.actor = actor
        self.targets = []

    def addTarget(self, target):
        '''
            The function adds a target to the existing list of target if any
        '''
        self.targets.append(target)

    def removeTarget(self, target):
        '''
            The function removes a target from the existing list of target
        '''
        self.targets.remove(target)

    def getActor(self):
        '''
            The function returns the actor who is involved in the payment transactions
        '''
        return self.actor

    def getTargets(self):
        '''
            The function returns the targets who are involved in the payment transactions with the actor
        '''
        return self.targets


class Graph:
    '''
    Objective of this class is to use the Node class and represent the graph of the vertices/nodes(actors) and edges(payment transactions)
    '''
    def __init__(self):
        self.nodeList = {}
        self.nodeCount = 0

    def addNode(self, actor):
        '''
            The function adds an actor to the graph and updates the number of nodes present
        '''
        if actor not in self.nodeList:
            createdNode = Node(actor)
            self.nodeList[actor] = createdNode
            self.nodeCount = self.nodeCount + 1

    def getNode(self, actor):
        '''
            The function checks if an actor is present in the graph and if the actor is present return the actor
        '''
        if actor in self.nodeList:
            return self.nodeList[actor]
        else:
            return None

    def addEdge(self, actor, target):
        '''
            The function adds the actor and target to the graph if they are already not present.
            It also adds the target to the actor's target ( For both the actor and the target )
        '''
        if actor not in self.nodeList:
            self.addNode(actor)
        if target not in self.nodeList:
            self.addNode(target)

        self.nodeList[actor].addTarget(self.nodeList[target])
        self.nodeList[target].addTarget(self.nodeList[actor])

    def getNodes(self):
        '''
            Get the list of nodes(customers) that are part of the graph
        '''
        return self.nodeList.keys()

    def getNodesDegrees(self):
        '''
            Get the number of edges from every node in the graph
        '''
        return [len(self.getNode(node).getTargets()) for node in self.getNodes()]

    def removeEdges(self, edgesList):
        '''
            Remove a list of edges that are no longer suppose to be part of the graph
            Remove the node if it is no longer part of any payment transaction
        '''
        for edge in edgesList:
            if (self.getNode(edge['actor']) != None and self.getNode(edge['target']) != None):
                self.getNode(edge['actor']).removeTarget(self.nodeList[edge['target']])
                self.getNode(edge['target']).removeTarget(self.nodeList[edge['actor']])

            if len(self.getNode(edge['actor']).getTargets()) == 0:
                self.nodeList.pop(self.getNode(edge['actor']), None)

            if len(self.getNode(edge['target']).getTargets()) == 0:
                self.nodeList.pop(self.getNode(edge['target']), None)


def findMedian(lengthList):
    '''
        This function finds the median for a given list and outputs in the format as specified in the challenge
    '''
    sortedLengthList = sorted(lengthList)
    centralIndexIncludingZeroIndex = (len(sortedLengthList) - 1) / 2
    if ( len(sortedLengthList) % 2 ):
        return "{0:.2f}".format(sortedLengthList[centralIndexIncludingZeroIndex])
    else:
        return "{0:.2f}".format((sortedLengthList[centralIndexIncludingZeroIndex] + sortedLengthList[centralIndexIncludingZeroIndex + 1])/2.0)

def removeUnwantedEdges(activeGraph, activeWindow, minTime):
    '''
        This function removed the old unwanted edges from the activeGraph as well activeWindow and return activeWindow
    '''
    unwantedEdges = [ (content[0],content[1]) for content in activeWindow if content[2] < minTime ]
    if len(unwantedEdges) >= 1:
        activeGraph.removeEdges(unwantedEdges)
        activeWindow = [ transaction for transaction in activeWindow if (transaction[0],transaction[1]) not in unwantedEdges]
    return activeWindow

if __name__ == '__main__':

    if( len(sys.argv) != 3):
        print "Kindly provide two arguments. First one being the input file and second one being the output file.\n"
        print "Use the following syntax: ./" + sys.argv[0] + " inputFileLocation outputFileLocation"
    else:
        inputFile = sys.argv[1]
        outputFile = sys.argv[2]

        # Initialize the graph
        activeGraph = Graph()
        # Flag to update the start time during the first pass 
        maxTimeFlag = 0
        # Array to Store the current active window
        activeWindow = []

        # Opening the output file for writing
        with open(outputFile,'w') as outputFileHandler:
            # Opening the input file for reading
            with open(inputFile,'r+') as inputFileHandler:
                # Going through every paymenet transaction, one at a time
                for content in inputFileHandler:
                    # Considering the JSON data provided may not be in the right format, we need to ignore such transaction
                    try:
                        paymentTransactionJSON = json.loads(content)
                        # Ignoring data which does not contain actor / target or created time 
                        if ( len(paymentTransactionJSON['created_time']) != 0 and len(paymentTransactionJSON['actor']) !=0 and len(paymentTransactionJSON['target']) != 0):
                            # Converting the time to a known format.
                            createdTime = dateutil.parser.parse(paymentTransactionJSON['created_time'])
                            # Keeping Track of the maxTime
                            if( maxTimeFlag == 0 ):
                                maxTimeFlag = 1
                                maxTime = createdTime
                            elif ( createdTime > maxTime ):
                                maxTime = createdTime
                            # Keeping Track of the minTime
                            minTime = maxTime - timedelta(seconds=59)

                            # Update the rolling median for each iteration
                            if createdTime >= minTime:
                                # If the created time is greater than current window time minimum time and is less than the maximum time, consider it to be active
                                activeWindow.append((paymentTransactionJSON['actor'],paymentTransactionJSON['target'],createdTime))
                                activeGraph.addNode(paymentTransactionJSON['actor'])
                                activeGraph.addEdge(paymentTransactionJSON['actor'],paymentTransactionJSON['target'])
                                # Remove existing edges in the activeWindow if they are no longer part of the current active window time.
                                activeWindow = removeUnwantedEdges(activeGraph,activeWindow,minTime)
                                # Update the rolling median
                                outputFileHandler.write( str(findMedian(activeGraph.getNodesDegrees())) + "\n" )
                            else:
                                # Update the rolling median even if the input payment transactions is out of order
                                outputFileHandler.write( str(findMedian(activeGraph.getNodesDegrees())) + "\n" )

                    except:
                        # Ignoring transactions that don't have the input JSON in proper format.
                        pass





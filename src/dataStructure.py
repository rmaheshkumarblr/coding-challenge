## Objectives :

# 1) Create a datastructure that resembles the requirement. (Node class)
# 2) Create a graph that is going to represent the transaction information. (Graph class)
# 3) Take the incoming data and use the two classes to obtain the output

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
		return [len(self.getNodes(node).getTargets()) for node in self.getNodes()]

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





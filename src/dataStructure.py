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



class Node:
	def __init__(self,id,dist):
		self.id = id
		self.cost = 10000
		self.distanceToGoal = dist
		self.edges = []
		self.previousNode = id
		self.start = False
		self.end = False

class Edge:
	def __init__(self,cost,node):
		self.cost = cost
		self.connectedNode = node

def astarInit(board):
	stringParts = {'id':0,'edges':1,'distanceToGoal':2,'nodeType':3}

	nodes  = board.split('\n')
	nodeArray = []

	for string in nodes:
		attributes = string.split(',')
		node = Node(attributes[stringParts['id']],attributes[stringParts['distanceToGoal']])
		nodeType = attributes[stringParts['nodeType']]

		if nodeType == 'A':
			node.start = True
		elif nodeType == 'B':
			node.end = True

		edges = attributes[stringParts['edges']].split(':')
		for edge in edges:
			edge = edge.split(" ")
			node.edges.append(Edge(edge[0],edge[1]))

		nodeArray.append(node)
	
	return nodeArray

########################################################################################
################                  PUBLIC FINCTIONS             #########################
########################################################################################

#Board-format should be a comma-separated string with:
#<nodeNumber>,<edgecost1><space><connected node>:<edgecost2><space><connecten node 2>:...,<distance to goal>,<A = start or B = goal\n
#<nodeNumber>,...

def astarAlgorithm(board):
	nodeArray = astarInit(board)
	print(nodeArray)



	return 0

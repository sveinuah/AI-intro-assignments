INF = 50000

class Node:
	def __init__(self,id,dist):
		self.id = id
		self.cost = 10000
		self.distanceToGoal = dist
		self.edges = []
		self.previousNode = None
		self.start = False
		self.end = False

class Edge:
	def __init__(self,cost,node):
		self.cost = cost
		self.connectedNode = node

def dijkstraInit(board):
	stringParts = {'id':0,'edges':1,'distanceToGoal':2,'nodeType':3}

	nodes  = board.split('\n')
	nodeArray = []

	for string in nodes:
		attributes = string.split(',')
		node = Node(int(attributes[stringParts['id']]),int(attributes[stringParts['distanceToGoal']]))
		nodeType = attributes[stringParts['nodeType']]

		if nodeType == 'A':
			node.start = True
		elif nodeType == 'B':
			node.end = True
		elif nodeType == '#':
			node.cost = INF

		edges = attributes[stringParts['edges']].split(':')
		for edge in edges:
			edge = edge.split(" ")
			node.edges.append(Edge(int(edge[0]),int(edge[1])))

		nodeArray.append(node)
	
	startNode = Node(-1,10000)

	for node in nodeArray:
		if node.start:
			startNode = node
		for edge in node.edges:
			tempIndex = 0
			tempNode = nodeArray[0]
			while tempNode.id != edge.connectedNode:
				#print(len(nodeArray),tempIndex, edge.connectedNode)
				tempNode = nodeArray[tempIndex]
				tempIndex += 1
			edge.connectedNode = tempNode

	return nodeArray, startNode

########################################################################################
################                  PUBLIC FINCTIONS             #########################
########################################################################################

#Board-format should be a comma-separated string with:
#<nodeNumber>,<edgecost1><space><connected node>:<edgecost2><space><connecten node 2>:...,<distance to goal>,<A = start or B = goal\n
#<nodeNumber>,...

def dijkstraAlgorithm(board):
	nodeArray, startNode = dijkstraInit(board)
	shortestPath = INF
	currentNode = startNode
	previousNode = startNode
	currentNode.cost = 0
	nodeQueue = [currentNode]
	exploredNodes = []

	while True:
		if len(nodeQueue) == 0:
			print("failed")
			return -1
		
		currentNode = nodeQueue[0]
		nodeQueue = nodeQueue[1:]

		if currentNode.end:
			return currentNode

		exploredNodes.append(currentNode)

		for edge in currentNode.edges:
			if edge.connectedNode.cost == INF:
				exploredNodes.append(edge.connectedNode)
			elif edge.connectedNode not in exploredNodes and edge.connectedNode not in nodeQueue:
				edge.connectedNode.cost = currentNode.cost + edge.cost
				edge.connectedNode.previousNode = currentNode
				nodeQueue.append(edge.connectedNode)
			elif edge.connectedNode in nodeQueue:
				if edge.connectedNode.cost > (currentNode.cost + edge.cost):
					edge.connectedNode.cost = currentNode.cost + edge.cost
					edge.connectedNode.previousNode = currentNode

		nodeQueue = sorted(nodeQueue,key = lambda nodeQueue: nodeQueue.cost)

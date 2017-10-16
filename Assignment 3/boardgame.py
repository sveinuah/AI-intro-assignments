import astar

fileList = ["boards/board-1-1.txt","boards/board-1-2.txt","boards/board-1-3.txt","boards/board-1-4.txt"]
nodeArray = []
numRows = 0
numCols = 0


class Node:
	def __init__(self):
		self.id = id(self)
		self.cost = 10000
		self.distanceToGoal = 10000
		self.edges = []
		self.previousNode = id(self)
		self.obstacle = False
		self.start = False
		self.end = False

class Edge:
	def __init__(self,cost,node1,node2):
		self.cost = cost
		self.connectedNodes = [node1,node2]


def findChildren():

	for i in range(0,numRows):
		for j in range(0,numCols):
			children = []
			ownId = nodeArray[i][j].id

			if nodeArray[i][j].obstacle:
				nodeArray[i][j].edges.append(children)
			
			else:
				if i-1 >= 0 and not nodeArray[i-1][j].obstacle:
					children.append(Edge(1,ownId,nodeArray[i-1][j].id))

				if i+1 < numRows and not nodeArray[i+1][j].obstacle:
					children.append(Edge(1,ownId,nodeArray[i+1][j].id))

				if j-1 >= 0 and not nodeArray[i][j-1].obstacle:
					children.append(Edge(1,ownId,nodeArray[i][j-1].id))

				if j+1 < numCols and not nodeArray[i][j+1].obstacle:
					children.append(Edge(1,ownId,nodeArray[i][j+1].id))

				nodeArray[i][j].edges.append(children)



def findDistanceToGoal():
	goalPosX = -1
	goalPosY = -1

	for i in range(0,numRows):
		for j in range(0,numCols):
			if nodeArray[i][j].end == True:
				goalPosX = i
				goalPosY = j

	for i in range(0,numRows):
		for j in range(0,numCols):
			nodeArray[i][j].distanceToGoal = abs(goalPosX-i) + abs(goalPosY-j)


def boardInit():
	choice = int(input("Input number between 1-4 to choose a board: "))
	filename = fileList[choice-1]

	with open(filename) as f:
		contents = f.read()
	
	print(contents)

#-------------- Node making -------------------------
	row = 0
	col = 0
	tempArray = []

	for element in contents:
		if element == '\n':
			row = row + 1
			col = 0
			if len(tempArray) > 0:
				nodeArray.append(tempArray)
				tempArray = []
		else:
			tempArray.append(Node())
			if(element == 'A'):
				tempArray[col].start = True
			elif element == 'B':
				tempArray[col].end = True
			elif element == '#':
				tempArray[col].obstacle = True
			col = col + 1

	global numRows
	global numCols
	numRows = len(nodeArray)
	numCols = len(nodeArray[0])					#Assuming all rows have equal number of elements

	findChildren()
	findDistanceToGoal()

# ------------ Game -------------------------------

def game():

	for i in range(0,numRows):
		for j in range(0,numCols):
			if nodeArray[i][j].start:
				startX = i
				startY = j


	shortestPath = astar.astarAlgorithm(nodeArray,startX,startY)

boardInit()
game()


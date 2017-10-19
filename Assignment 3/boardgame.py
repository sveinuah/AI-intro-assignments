import dijkstra
import astar

goalNode = -1
startNode = -1

fileList = ["boards/board-1-1.txt","boards/board-1-2.txt","boards/board-1-3.txt","boards/board-1-4.txt","boards/board-2-1.txt","boards/board-2-2.txt","boards/board-2-3.txt","boards/board-2-4.txt"]
formattedBoard = ""
costDict = {".":1,"#":1,"A":0,"B":0,"w":100,"m":50,"f":10,"g":5,"r":1}

def findDistanceToGoal(nodeNum,goalNode,rowLength,colLength):
	goalRow = int(goalNode/rowLength)
	goalCol = int(goalNode%rowLength)
	nodeRow = int(nodeNum/rowLength)
	nodeCol = int(nodeNum%rowLength)

	return abs(goalRow-nodeRow) + abs(goalCol-nodeCol)

def boardInit():
	choice = int(input("Input number between 1-8 to choose a board: "))
	filename = fileList[choice-1]

	with open(filename) as f:
		contents = f.read()
	
	print(contents)

#-------------- formatting  -------------------------
	rows = contents.split('\n')
	rowNum = 0
	colNum = 0
	nodeNum = 0
	nodeEdges = []
	nodeGoalDistance = 0
	nodeType = ""

	rowLength = len(rows[0]) #Assuming equal row length
	colLength = len(rows) #Assuming equal column length
	global formattedBoard
	global startNode
	global goalNode

	for row in rows:
		for char in row:
			if char ==  'B':
				goalNode = colNum + rowLength*rowNum
			colNum += 1		
		rowNum += 1
		colNum = 0

	for row in range(0,len(rows)):
		for col in range(0,len(rows[row])):
			nodeNum = col + (row)*rowLength
			nodeEdges = []
			formattedBoard += (str(nodeNum)+',')
			if col > 0:
				nodeEdges.append(str(costDict[rows[row][col-1]])+" "+str(nodeNum-1))
			if col < rowLength-1:
				nodeEdges.append(str(costDict[rows[row][col+1]])+" "+str(nodeNum+1))
			if row > 0:
				nodeEdges.append(str(costDict[rows[row-1][col]])+" "+str(nodeNum - rowLength))
			if row < colLength-2:
				nodeEdges.append(str(costDict[rows[row+1][col]])+" "+str(nodeNum + rowLength))

			for edge in nodeEdges:
				formattedBoard += (edge+':')
			formattedBoard = formattedBoard[:(len(formattedBoard)-1)]
			formattedBoard += ','

			char = rows[row][col]
			if char == '#':
				formattedBoard += "10000,"
			else:	
				formattedBoard += str(findDistanceToGoal(nodeNum,goalNode,rowLength,colLength))+','

			formattedBoard += char +'\n'

	formattedBoard = formattedBoard[:(len(formattedBoard)-1)] #Remove last \n

# ------------ Game -------------------------------

def game():
	print("Game!")

	endNode = dijkstra.dijkstraAlgorithm(formattedBoard)
	#endNode = astar.astarAlgorithm(formattedBoard)

	path = [endNode]
	print("EndNode? ", endNode.end,"total cost: ",endNode.cost)
	tempNode = endNode
	while not tempNode.start:
		tempNode = tempNode.previousNode
		path.append(tempNode)

	path = list(reversed(path))
	for node in path:
		print(node.id,end=",")


boardInit()
game()


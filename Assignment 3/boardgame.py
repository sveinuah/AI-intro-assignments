import astar

goalNode = -1
startNode = -1

fileList = ["boards/board-1-1.txt","boards/board-1-2.txt","boards/board-1-3.txt","boards/board-1-4.txt"]
formattedBoard = ""

def findDistanceToGoal(nodeNum,goalNode,rowLength,colLength):
	goalRow = int(goalNode/rowLength)
	goalCol = int(goalNode%rowLength)
	nodeRow = int(nodeNum/rowLength)
	nodeCol = int(nodeNum%rowLength)

	return abs(goalRow-nodeRow) + abs(goalCol-nodeCol)

def boardInit():
	choice = int(input("Input number between 1-4 to choose a board: "))
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

	rowNum = 0
	colNum = 0

	for row in rows:
		for char in row:
			nodeNum = colNum + (rowNum)*rowLength
			nodeEdges = []
			formattedBoard += (str(nodeNum)+',')
	
			if colNum > 0:
				nodeEdges.append("1 "+str(nodeNum-1))
			if colNum < rowLength-2:
				nodeEdges.append("1 "+str(nodeNum+1))
			if rowNum > 0:
				nodeEdges.append("1 "+str(nodeNum - rowLength))
			if rowNum < colLength-2:
				nodeEdges.append("1 "+str(nodeNum + rowLength))

			for edge in nodeEdges:
				formattedBoard += (edge+':')
			formattedBoard = formattedBoard[:(len(formattedBoard)-1)]
			formattedBoard += ','

			if char == '#':
				formattedBoard += "10000,"
			else:	
				formattedBoard += str(findDistanceToGoal(nodeNum,goalNode,rowLength,colLength))+','

			nodeType = char
			formattedBoard += nodeType+'\n'

			colNum += 1
		rowNum += 1
		colNum = 0
	formattedBoard = formattedBoard[:(len(formattedBoard)-1)] #Remove last \n

# ------------ Game -------------------------------

def game():
	print("Game!")

	shortestPath = astar.astarAlgorithm(formattedBoard)

boardInit()
game()


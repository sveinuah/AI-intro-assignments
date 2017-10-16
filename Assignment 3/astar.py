

def astarAlgorithm(board,startX,startY):
	posX = startX
	posY = startY
	currentNode = board[startX][startY]
	currentNode.cost = 0

	while not currentNode.end:
		for edge in currentNode.edges:
			for child in edge.connectedNodes:
				if child != currentNode.self:
					if (edge.cost + currentNode.cost) < child.cost:
						child.cost = edge.cost + currentNode.cost
						child.previousNode = self


	return 0
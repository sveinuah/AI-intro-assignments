# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):

    # maxValue is only called for pacMan, maximizing score. currentRecursionDepth is added to provide boudaries to the recursion.
    def maxValue(self, state, currentRecursionDepth):
        if state.isWin() or state.isLose() or currentRecursionDepth >= self.depth:
            return scoreEvaluationFunction(state)

        v = -100000
        for action in state.getLegalActions(0):
            v = max(v,self.minValue(state.generateSuccessor(0,action), 1, currentRecursionDepth+1))

        return v

    # minValue is called for every ghost, but the recursion-depth is only incremented when minValue is called from maxValue.
    # This is done to assure the right recursion depth required in the autograding.
    # unit parameter is added to track which ghost's turn it is.
    def minValue(self, state, unit, currentRecursionDepth):
        if state.isWin() or state.isLose(): 
            return scoreEvaluationFunction(state)

        v = 100000
        for action in state.getLegalActions(unit):
            if unit == state.getNumAgents() - 1:    
                v = min(v, self.maxValue(state.generateSuccessor(unit,action), currentRecursionDepth))
            else:
                v = min(v, self.minValue(state.generateSuccessor(unit,action), unit+1, currentRecursionDepth)) 

        return v

    # getAction holds the logic to convert from value to actionm, as well as starting the minimax algorithm.
    def getAction(self, gameState):

        chosenAction = Directions.STOP
        currentMaxValue = -100000
        for action in gameState.getLegalActions(0):
            checkedActionValue = self.minValue(gameState.generateSuccessor(0,action),1,1)
            if checkedActionValue > currentMaxValue:
                currentMaxValue = checkedActionValue
                chosenAction = action

        return chosenAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def maxValue(self, state, currentRecursionDepth, alpha, beta):
        if state.isWin() or state.isLose() or currentRecursionDepth >= self.depth:
            return scoreEvaluationFunction(state)

        v = -10000
        for action in state.getLegalActions(0):
            v = max(v, self.minValue(state.generateSuccessor(0,action), 1,currentRecursionDepth+1,alpha,beta))
            if v > beta:
                return v
            alpha = max(alpha,v)

        return v

    def minValue(self, state, unit, currentRecursionDepth, alpha, beta):
        if state.isWin() or state.isLose(): 
            return scoreEvaluationFunction(state)
            
        v = 10000
        for action in state.getLegalActions(unit):
            if unit == state.getNumAgents() - 1:    
                v = min(v, self.maxValue(state.generateSuccessor(unit,action), currentRecursionDepth,alpha,beta))
            else:
                v = min(v, self.minValue(state.generateSuccessor(unit,action), unit+1, currentRecursionDepth,alpha,beta))
            
            if v < alpha: return v
            beta = min(beta,v)

        return v


    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        chosenAction = Directions.STOP
        currentMaxValue = -100000
        for action in gameState.getLegalActions(0):
            checkedActionValue = self.minValue(gameState.generateSuccessor(0,action),1,1,-10000,10000)
            if checkedActionValue > currentMaxValue:
                currentMaxValue = checkedActionValue
                chosenAction = action

        return chosenAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction


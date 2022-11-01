import heapq as hq
import copy
import time

level_1 = [[1,2,3],[4,5,6],[7,8,0]] # depth 0
level_2 = [[1,2,3],[4,5,6],[0,7,8]] # depth 2
level_3 = [[1,2,3],[5,0,6],[4,7,8]] # depth 4
level_4 = [[1,3,6],[5,0,2],[4,7,8]] # depth 8
level_5 = [[1,3,6],[5,0,7],[4,8,2]] # depth 12
level_6 = [[1,6,7],[5,0,3],[4,8,2]] # depth 16
level_7 = [[7,1,2],[4,8,5],[6,3,0]] # depth 20
level_8 = [[0,7,2],[4,6,1],[3,5,8]] # depth 24

levels = [level_1, level_2, level_3, level_4, level_5, level_6, level_7, level_8]

goal_state = [[1,2,3],[4,5,6],[7,8,0]]

visitedStates = [] # list of nodes we have visited
exploreStates = [] # list of nodes we have to visit

nodesExpanded = 0
maxQueueSize = 0

class Node:
    def __init__(self, board, level, f, parent):
        self.board = board # ex. [[1,2,3], [4,5,6], [7,8,0]]
        self.level = level # the depth of the node in the tree
        self.f = f # f(n) value for the node
        self.parent = parent # keeps reference to parent node
        self.g = 0
        self.h = 0

    # self.level, or g, is the cost, which is always the level in this case bc the cost of "moving" the tile for this problem is always 1
    # h is the heurisitc value, which is either Manhattan Distance or Misplaced Tiles, or 0 for UCS
    def fn(self, g, h=0):
        return g + h

    # this is to calculate h value for fn function, using Misplaced Tiles heuristic
    def calcMisplacedTiles(self):
        misplacedTiles = 0
        counter = 1
        for i in range(0, len(self.board)):
            for j in range(0, len(self.board)):
                if self.board[i][j] != 0 and self.board[i][j] != counter:
                    misplacedTiles += 1
                counter += 1
        return misplacedTiles

    # this is to calculate h value for fn function, using Manhattan Distance heuristic
    def calcManhattanDistance(self, goal_state):
        manhattanDistance = 0
        for i in range(0, len(self.board)):
            for j in range(0, len(self.board)):
                if goal_state[i][j] != 0:
                    x1, y1 = self.getCoordinates(self.board[i][j])
                    x2, y2 = self.getCoordinates(goal_state[i][j])
                    manhattanDistance += abs(x1-x2) + abs(y1-y2)
        return manhattanDistance

    # expand potential children to eventually traverse down tree
    def exploreMoves(self, heuristic, goal_state):
        x, y = self.getCoordinates(0)
        possibleMoves = [[x-1, y], [x+1, y], [x, y-1], [x, y+1]]
        actualMoves = self.isValid(possibleMoves)
        
        for m in actualMoves:
            # ex. m = [1,2]
            child = copy.deepcopy(self)

            temp = child.board[m[0]][m[1]]
            child.board[m[0]][m[1]] = child.board[x][y]
            child.board[x][y] = temp
            
            newNode = Node(child.board, self.level + 1, 0, self)
            newNode.g = self.level+1

            if heuristic == 1:
                fn = self.fn(self.level+1)
            elif heuristic == 2:
                hn = self.calcMisplacedTiles()
                fn = self.fn(self.level+1, hn)
                newNode.h = hn
                newNode.f = fn
            else:
                hn = self.calcManhattanDistance(goal_state)
                fn = self.fn(self.level+1, self.calcManhattanDistance(goal_state))
                newNode.h = hn
                newNode.f = fn


            visitedBoards = [n.board for n in visitedStates]

            if newNode.board not in visitedBoards:
                hq.heappush(exploreStates, newNode)
                global maxQueueSize
                if len(exploreStates) > maxQueueSize:
                    maxQueueSize += 1

    # checks to see if move is a valid move within the board
    def isValid(self, possibleMoves):
        actualMoves = []
        for move in possibleMoves:
            if move[0] >= 0 and move[0] < len(self.board) and move[1] >= 0 and move[1] < len(self.board):
                actualMoves.append(move)
        return actualMoves

    # gets position of value on the board
    def getCoordinates(self, value):
        for i in range(0, len(self.board)):
            for j in range(0, len(self.board)):
                if self.board[i][j] == value:
                    return i, j

    # helper function to nicely print board in 3x3 shape
    ''' ex
    [1, 2, 3]
    [4, 5, 6]
    [7, 8, 0]
    '''
    def printNicely(self):
        for i in self.board:
            print(i)
        print("-------------------")

    # need this wrapper for hq.heappush() call
    def __lt__(self, other):
        return self.f < other.f

class Puzzle:
    def __init__(self, goal_state, n=3):
        self.goal_state = goal_state
        self.n = n

    # solves the puzzle
    def solve(self, heuristic):
        # deque from exploreStates
        # if node == goal state, done
        # else, explore children and run again

        while len(exploreStates) != 0:
            node = hq.heappop(exploreStates)
            # print("Level:", node.level)
            hq.heappush(visitedStates, node)

            if node.board == goal_state:
                self.printSolution(node)
                return node.level

            # check children
            global nodesExpanded
            nodesExpanded += 1
            node.exploreMoves(heuristic, goal_state)

    # function to print the solution given final board
    def printSolution(self, endNode):
        if len(exploreStates) == 0:
            n = Node(level_1, 0, 0, None)
            n.printNicely()
        else:
            nodes = []
            while endNode.parent:
                nodes.append(endNode)
                endNode = endNode.parent

            nodes = nodes[::-1]
            print(f"The best state to expand with a g(n) = {nodes[0].g-1} and h(n) = {nodes[0].h} is")
            nodes[0].parent.printNicely()
            for n in nodes:
                print(f"The best state to expand with a g(n) = {n.g} and h(n) = {n.h} is")
                n.printNicely()

            print("Goal state!")

    # need this wrapper for hq.heappush() call
    def __lt__(self, node1, node2):
        return node1.f < node2.f

            
if __name__ == "__main__":

    heuristic = int(input("1 for UCS, 2 for Misplaced Tiles, 3 for Manhattan "))

    option = int(input("enter 1 to solve a predefined puzzle or 2 to input your own "))

    if option == 1:
        difficulty = int(input("select diffuclty, enter one number between 1 and 8, with 1 being the easiest, 8 being the hardest "))
        goal_state = [[1,2,3], [4,5,6], [7,8,0]]
        puzzle = Puzzle(goal_state)
        node = Node(levels[difficulty-1], 0, 0, None)

        # give starting node a starting f(n) value
        if heuristic == 1:
            node.f = node.fn(0)
        if heuristic == 2:
            node.f = node.fn(0, node.calcMisplacedTiles())
        elif heuristic == 3:
            node.f = node.fn(0, node.calcManhattanDistance(goal_state))            

        hq.heappush(exploreStates, node)
        start = time.time()
        answer = puzzle.solve(heuristic)
    else:
        dimension = int(input("enter 1 number for dimension of board "))
        puzzle = Puzzle(dimension)
        print('''
            Enter your puzzle, using a zero to represent the blank. 
            Please only enter valid 8-puzzles. 
            Enter the puzzle delimiting the numbers with a space
        ''')
        board = []
        goal_state = []
        # used to fill values of goal_state
        current = 1

        # properly take user input and convert it into list of lists
        for i in range(0, dimension):
            print(f"enter row of {dimension} values: ")
            row = input().split()
            row = [int(x) for x in row]

            board.append(row)
            goal_state.append([num for num in range(current, current+dimension)])
            current += dimension

        node = Node(board, 0, 0, None)
        # specify last cell in last row should be blank spot
        goal_state[-1][-1] = 0
        hq.heappush(exploreStates, node)

        start = time.time()
        puzzle.goal_state = goal_state
        answer = puzzle.solve(heuristic)

    print("solution depth was:", answer)
    print("solution took",  time.time() - start, "seconds")
    print("number of nodes expanded: ", nodesExpanded)
    print("max queue size: ", maxQueueSize)
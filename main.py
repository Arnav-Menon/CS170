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

goal_state = [[1,2,3],[4,5,6],[7,8,0]]

visitedStates = [] # list of nodes we have visited
exploreStates = [] # list of nodes we have to visit

class Node:
    def __init__(self, board, level, f, parent):
        self.board = board # [[1,2,3], [4,5,6], [7,8,0]]
        self.level = level # the depth of the node in the tree
        self.f = f # f(n) value for the node
        self.parent = parent # keeps reference to parent node

    # g is the cost, which is always the level in this case bc the cost of "moving" the tile for this problem is always 1
    # h is the heurisitc value, which is either Manhattan Distance or Misplaced Tiles
    def fn(self, g, h=0):
        return self.g() + h

    def g(self):
        return self.level

    def exploreMoves(self):
        x, y = self.findBlank()
        possibleMoves = [[x-1, y], [x+1, y], [x, y-1], [x, y+1]]
        actualMoves = self.isValid(possibleMoves)
        
        print("VALID MOVES:", actualMoves)
        
        for m in actualMoves:
            # m = [1,2]
            child = copy.deepcopy(self)

            temp = child.board[m[0]][m[1]]
            child.board[m[0]][m[1]] = child.board[x][y]
            child.board[x][y] = temp

            newNode = Node(child.board, self.level + 1, 0, self)

            visitedBoards = [n.board for n in visitedStates]

            if newNode.board not in visitedBoards:
                hq.heappush(exploreStates, newNode)

    def isValid(self, possibleMoves):
        actualMoves = []
        for move in possibleMoves:
            if move[0] >= 0 and move[0] < len(self.board) and move[1] >= 0 and move[1] < len(self.board):
                actualMoves.append(move)
        return actualMoves

    def findBlank(self):
        for i in range(0, len(self.board)):
            for j in range(0, len(self.board)):
                if self.board[i][j] == 0:
                    return i, j

    def printNicely(self):
        for i in self.board:
            print(i)
        print("-------------------")

    def __lt__(self, other):
        return self.f < other.f

class Puzzle:
    def __init__(self, n=3):
        self.n = n

    def solve(self):
        # deque from exploreNodes
        # if node == goal state, done
        # else, do stuff

        while len(exploreStates) != 0:
            node = hq.heappop(exploreStates)
            print("Level:", node.level)
            hq.heappush(visitedStates, node)
            node.printNicely()

            # if node.level == 8:
                # return 2

            if node.board == goal_state:
                # write function that prints path to solution from root
                # use parent to backwards traverse
                return node.level

            # check children
            node.exploreMoves()

    def __lt__(self, node1, node2):
        return node1.f < node2.f

            
if __name__ == "__main__":
    start = time.time()

    puzzle = Puzzle(3)

    node = Node(level_4, 0, 0, None)
    hq.heappush(exploreStates, node)

    answer = puzzle.solve()

    print("DEPTH:", answer)
    print("Solution took",  time.time() - start, "seconds")
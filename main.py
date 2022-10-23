import heapq as hq
import copy

level_1 = [[1,2,3],[4,5,6],[7,8,0]] # depth 0
level_2 = [[1,2,3],[4,5,6],[0,7,8]] # depth 2
level_3 = [[1,2,3],[5,0,6],[4,7,8]] # depth 4
level_4 = [[1,3,6],[5,0,2],[4,7,8]] # depth 8
level_5 = [[1,3,6],[5,0,7],[4,8,2]] # depth 12
level_6 = [[1,6,7],[5,0,3],[4,8,2]] # depth 16
level_7 = [[7,1,2],[4,8,5],[6,3,0]] # depth 20
level_8 = [[0,7,2],[4,6,1],[3,5,8]] # depth 24

goal_state = [[1,2,3],[4,5,6],[7,8,0]]

visitedStates = []
exploreStates = []

class Node:
    def __init__(self, board, level, f):
        self.board = board # [[], [], []]
        self.level = level
        self.f = f
        hq.heappush(visitedStates, self.board)

    def fn(self, g, h=0):
        return g + h

    def g(self):
        return self.level

    def exploreMoves(self):
        x, y = self.findBlank()
        possibleMoves = [[x-1, y], [x+1, y], [x, y-1], [x, y+1]]
        actualMoves = self.isValid(possibleMoves)
        # print(actualMoves)
        for m in actualMoves:
            # m = [1,2]
            child = copy.deepcopy(self.board)
            temp = child[m[0]][m[1]]
            child[m[0]][m[1]] = child[x][y]
            child[x][y] = temp
            newNode = Node(child, 0, 0)
            hq.heappush(exploreStates, newNode)
            newNode.printNicely()

    def solve(self):
        # deque from exploreNodes
        # if node == goal state, done
        # else, do stuff

        while len(exploreStates) != 0:
            node = hq.heappop(exploreStates)
            hq.heappush(visitedStates, node)

            # check children
            node.exploreMoves()


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

    def solve():
        pass

if __name__ == "__main__":
    n = Node(level_1, 0, -1)
    n.f = n.fn(n.level)

    n.exploreMoves()
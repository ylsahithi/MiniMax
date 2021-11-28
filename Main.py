from Design_game_grid import Grid
import numpy as np
import Helper_functions
from random import randint
import time
import matplotlib.pyplot as plt
import numpy

initialTiles = 2
(Agent, Opponent) = (0, 1)
possibleDirections = {0: "UP", 1: 'DOWN', 2: 'LEFT', 3: 'RIGHT'}
timeLimit = 1
prob = 0.9
max_tiles_array = []


class Opp():
    def getMove(self, grid):
        cells = grid.getEmptytiles()
        if cells:
            return cells[randint(0, len(cells) - 1)]
        else:
            None


class Player():
    def getMove(self, grid):
        copygrid = []
        for i in range(4):
            copygrid.extend(grid.map[i])
        [child, moves] = Helper_functions.getChildren(copygrid)
        maxpath = -np.inf
        direction = 0
        for i in range(len(child)):
            c = child[i]
            m = moves[i]
            highest_value = -np.inf
            maxdepth = 4
            # highest_value = Minimax.calculate(c, maxdepth, False)
            highest_value = AlphaBetaPrune.calculate(c, maxdepth, -np.inf, np.inf, False)
            if m == 0 or m == 2:
                highest_value += 10000
            if highest_value > maxpath:
                direction = m
                maxpath = highest_value

        return direction


class Minimax():
    def calculate(grid, depth, isMax):
        if depth == 0:
            return Helper_functions.heuristic(grid)
        if not Helper_functions.isValidMove(grid):
            return Helper_functions.heuristic(grid)
        if isMax:
            bestValue = -np.inf
            [child, moving] = Helper_functions.getChildren(grid)
            for ch in child:
                bestValue = max(bestValue, Minimax.calculate(ch, depth - 1, False))
            return bestValue
        else:
            cells = [i for i, x in enumerate(grid) if x == 0]
            child = []
            bestValue = np.inf
            for c in cells:
                temp = list(grid)
                temp[c] = 2
                child.append(temp)
                temp = list(grid)
                temp[c] = 4
                child.append(temp)
            for ch in child:
                bestValue = min(bestValue, Minimax.calculate(ch, depth - 1, True))
            return bestValue


class AlphaBetaPrune():
    def calculate(grid, depth, alpha, beta, isMax):
        if depth == 0:
            return Helper_functions.heuristic(grid)
        if not Helper_functions.isValidMove(grid):
            return Helper_functions.heuristic(grid)
        if isMax:
            bestValue = -np.inf
            [child, moving] = Helper_functions.getChildren(grid)
            for ch in child:
                bestValue = max(bestValue, AlphaBetaPrune.calculate(ch, depth - 1, alpha, beta, False))
                if bestValue >= beta:
                    return bestValue
                alpha = max(alpha, bestValue)
            return bestValue
        else:
            cells = [i for i, x in enumerate(grid) if x == 0]
            child = []
            for c in cells:
                temp = list(grid)
                temp[c] = 2
                child.append(temp)
                temp = list(grid)
                temp[c] = 4
                child.append(temp)
            bestValue = np.inf
            for ch in child:
                bestValue = min(bestValue, AlphaBetaPrune.calculate(ch, depth - 1, alpha, beta, True))
                if bestValue <= alpha:
                    return bestValue
                beta = min(beta, bestValue)
            return bestValue


class Game2048:
    def __init__(self, size=4):
        self.grid = Grid(size)
        self.possibleTileValue = [2, 4]
        self.prob = prob
        self.initialTiles = initialTiles
        self.opponent = None
        self.agent = None
        self.end = False

    def setAgent(self, agent):
        self.agent = agent

    def setOpponent(self, opponent):
        self.opponent = opponent

    def setClock(self, time):
        if time - self.prevTime > timeLimit + 0.1:
            self.end = True
        else:
            self.prevTime = time

    def isGameCompleted(self):
        return not self.grid.Check_for_possiblity_move()

    def insertRandonTile(self):
        tile = self.getNextTile()
        cells = self.grid.getEmptytiles()
        cell = cells[randint(0, len(cells) - 1)]
        self.grid.map[cell[0]][cell[1]] = tile

    def getNextTile(self):
        if randint(0, 99) < 100 * self.prob:
            return self.possibleTileValue[0]
        else:
            return self.possibleTileValue[1];

    def start(self):
        for i in range(self.initialTiles):
            self.insertRandonTile()

        self.Display(self.grid)

        turn = Agent
        highestTile = 0

        self.prevTime = time.perf_counter()
        itr = 0
        while not self.isGameCompleted() and not self.end:
            itr = itr + 1
            temp = self.grid.Make_a_copy()
            move = None

            if turn == Agent:
                print("Agent is playing")
                move = self.agent.getMove(temp)

                if move != None and move >= 0 and move < 4:
                    if self.grid.Check_for_possiblity_move([move]):
                        self.grid.move(move)
                        highestTile = self.grid.getHighestTile()
                    # print(highestTile)
                    else:
                        print("Wrong Move")
                        self.end = True
                else:
                    print("Wrong Move - 1")
                    self.end = True
            else:
                print("Opponent is playing")
                move = self.opponent.getMove(temp)
                if move and self.grid.checkInsertion(move):
                    # self.grid.setCellValue(move, self.getNextTile())
                    self.grid.map[move[0]][move[1]] = self.getNextTile()
                # print(self.getNextTile())
                else:
                    print("Wrong move")
                    self.end = True

            if not self.end:
                print(itr)
            # self.Display(self.grid)
            self.setClock(time.perf_counter())
            turn = 1 - turn
        max_tiles_array.append(highestTile)
        print("Highest Score for this game:", highestTile)

    def Display(self, grid):
        for i in range(grid.size):
            for j in range(grid.size):
                print("%6d  " % grid.map[i][j], end="")
            print("")
        print("")
        print("")


def driver():
    game = Game2048()
    agent = Player()
    opponent = Opp()
    game.setAgent(agent)
    game.setOpponent(opponent)
    game.start()


if __name__ == '__main__':
    # numofGames = 50
    numofGames = 50
    for i in range(numofGames):
        print("--------------------------Iteration :", i + 1, "--------------------------------------")
        driver()
    Array_of_2 = [32, 64, 128, 256, 512, 1024, 2048]
    y = []
    mylabels = []
    print("Max tiles array", max_tiles_array)
    for i in range(len(Array_of_2)):
        if (max_tiles_array.count(Array_of_2[i]) != 0):
            y.append(max_tiles_array.count(Array_of_2[i]))
            mylabels.append(
                str(Array_of_2[i]) + '\n' + str((max_tiles_array.count(Array_of_2[i]) / numofGames) * 100) + "%")
    result = numpy.array(y)
    print('Result', result)
    print('Labels', mylabels)
    print("Percentage of 32's", (max_tiles_array.count(32) / numofGames) * 100)
    print("Percentage of 64's", (max_tiles_array.count(64) / numofGames) * 100)
    print("Percentage of 128's", (max_tiles_array.count(128) / numofGames) * 100)
    print("Percentage of 256's", (max_tiles_array.count(256) / numofGames) * 100)
    print("Percentage of 512's", (max_tiles_array.count(512) / numofGames) * 100)
    print("Percentage of 1024's", (max_tiles_array.count(1024) / numofGames) * 100)
    print("Percentage of 2048's", (max_tiles_array.count(2048) / numofGames) * 100)
    plt.plot(result, mylabels)
    # plt.pie(result,labels=mylabels)
    plt.title("Percentage of Occurances:")
    plt.xlabel('result')
    plt.ylabel('label')
    plt.show()

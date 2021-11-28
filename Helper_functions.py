import math

def getChildren(grid):
    possibleMoves = [0,1,2,3]
    children = []
    moving = []
    for eachmove in possibleMoves:
        gridcopy = list(grid)
        moved = move(gridcopy, eachmove)
        if moved == True:
            children.append(gridcopy)
            moving.append(eachmove)
    return [children,moving]

def Merge(cells):
    if len(cells) <= 1:
        return cells
    count = 0
    while count < len(cells)-1:
        if cells[count] == cells[count+1]:
            cells[count] *= 2
            del cells[count+1]
        count += 1

def move(grid, dir):
    hasMoved = False
    if dir == 0:

        for i in range(4):
            cells = []

            for j in range(i,i+13,4):
                cell = grid[j]
                if cell != 0:
                    cells.append(cell)
            Merge(cells)
            for j in range(i,i+13,4):
                value = cells.pop(0) if cells else 0
                if grid[j] != value:
                    hasMoved = True
                grid[j] = value
        return hasMoved
    elif dir == 1:
        for i in range(4):
            cells = []
            for j in range(i+12,i-1,-4):
                cell = grid[j]
                if cell != 0:
                    cells.append(cell)
            Merge(cells)
            for j in range(i+12,i-1,-4):
                value = cells.pop(0) if cells else 0
                if grid[j] != value:
                    hasMoved = True
                grid[j] = value
        return hasMoved
    elif dir == 2:
        for i in [0,4,8,12]:
            cells = []
            for j in range(i,i+4):
                cell = grid[j]
                if cell != 0:
                    cells.append(cell)
            Merge(cells)
            for j in range(i,i+4):
                value = cells.pop(0) if cells else 0
                if grid[j] != value:
                    hasMoved = True
                grid[j] = value
        return hasMoved
    elif dir == 3:
        for i in [3,7,11,15]:
            cells = []
            for j in range(i,i-4,-1):
                cell = grid[j]
                if cell != 0:
                    cells.append(cell)
            Merge(cells)
            for j in range(i,i-4,-1):
                value = cells.pop(0) if cells else 0
                if grid[j] != value:
                    hasMoved = True
                grid[j] = value
        return hasMoved

def isValidMove(grid):
    if 0 in grid:
        return True
    for i in range(16):
        if (i+1)%4!=0:
            if grid[i]==grid[i+1]:
                return True
        if i<12:
            if grid[i]==grid[i+4]:
                return True
    return False

def heuristic(grid):
    emptyTiles = len([i for i, x in enumerate(grid) if x == 0])
    highestTile = max(grid)
    Order = 0
    weights = [65536,32768,16384,8192,512,1024,2048,4096,256,128,64,32,2,4,8,16]
    # weights = [2048, 1024, 512, 256, 128, 64, 32, 2, 4, 8, 16]
    if highestTile == grid[0]:
        Order += (math.log(grid[0])/math.log(2))*weights[0]
    for i in range(16):
    # for i in range(11):
        if grid[i] >= 8:
            Order += weights[i]*(math.log(grid[i])/math.log(2))
        # return Order / (11 - emptyTiles)
    return Order/(16-emptyTiles)

    mainGrid = [[0] * 4 for i in xrange(4)]
    k = 0
    for i in range(4):
        for j in range(4):
            mainGrid[i][j] = grid[k]
            k += 1
    sm = 0
    for i in range(4):
        for j in range(4):
            if mainGrid[i][j] != 0:
                val = math.log(mainGrid[i][j])/math.log(2)
                for k in range(3-j):
                    nextright = mainGrid[i][j+k+1]
                    if nextright != 0:
                        rightval = math.log(nextright)/math.log(2)
                        if rightval != val:
                            sm -= math.fabs(rightval - val)
                            break
                for k in range(3-i):
                    nextdown = mainGrid[i+k+1][j]
                    if nextdown != 0:
                        downval = math.log(nextdown)/math.log(2)
                        if downval != val:
                            sm -= math.fabs(downval - val)
                            break
    mn = 0
    up = 0
    down = 0
    left = 0
    right = 0
    for i in range(4):
        j = 0
        k = j+1
        while k < 4:
            if mainGrid[i][k] == 0:
                k += 1
            else:
                if mainGrid[i][j] == 0:
                    curr = 0
                else:
                    curr = math.log(mainGrid[i][j])/math.log(2)
                nextval = math.log(mainGrid[i][k])/math.log(2)
                if curr > nextval:
                    up += nextval - curr
                elif nextval > curr:
                    down += curr - nextval
            j = k
            k += 1
    for j in range(4):
        i = 0
        k = i+1
        while k < 4:
            if mainGrid[j][k] == 0:
                k += 1
            else:
                if mainGrid[j][i] == 0:
                    curr = 0
                else:
                    curr = math.log(mainGrid[j][i])/math.log(2)
                nextval = math.log(mainGrid[j][k])/math.log(2)
                if curr > nextval:
                    left += nextval - curr
                elif nextval > curr:
                    right += curr - nextval
            i = k
            k += 1
    nm = max(up,down) + max(left,right)
    return 0.1*sm+mn+math.log(highestTile)/math.log(2)+ emptyTiles

# Assignment 5 - Problem 2 - Taffy Tangle
# Abdullah Khan - 30074457 - Tutorial 1
# Afnan Imran Chaudhry - 30077054 - Tutorial 10

import random, stddraw, picture, math
from itertools import groupby
from color import Color
from time import sleep

bg = Color(35, 35, 35)

# all the possible game pieces
shapes = ["triangle", "circle", "parallelogram", "diamond", "star", "pentagon"]

# set up the canvas
stddraw.setXscale(0.0, 16.0)
stddraw.setYscale(0.0, 20.0)
stddraw.setCanvasSize(750, 900)

globalScore = []
grid = [[],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        []]
centerCoordinatesX = []
centerCoordinatesY = []

# append shapes to the 2D grid (while taking care of three-in-a-row cases)
for outerIndex in range(len(grid)):
    for index in range(len(grid) - 2):
        randomShape = str(random.choice(shapes))
        # append the indices to create a coordinates list
        if outerIndex == 0:
            centerCoordinatesX.append((index + 1) * 2)
            # the y-coordinates are just the reverse of the x-coordinates with the addition of 16 & 18
            #centerCoordinatesY = centerCoordinatesX[::-1] + [16, 18]
            centerCoordinatesY = [18, 16] + centerCoordinatesX[::-1]
        # append the first two shapes no matter if they are equal
        if len(grid[outerIndex]) < 2:
            grid[outerIndex].append(randomShape)
        # check for equals now, starting from the third hape (horizontal only)
        elif len(grid[outerIndex]) >= 2:
            if randomShape == grid[outerIndex][index - 1] and randomShape == grid[outerIndex][index - 2] and grid[outerIndex][index - 2] == grid[outerIndex][index - 1]:
                # make a copy of the shapes list and then remove the duplicate hape from the new list
                # replace the duplicate hape on the grid with a random hape from the new list, then empty the new list
                shapesExcludingDuplicate = shapes.copy()
                shapesExcludingDuplicate.remove(randomShape)
                grid[outerIndex].append(random.choice(shapesExcludingDuplicate))
                del shapesExcludingDuplicate[:]
            else:
                grid[outerIndex].append(randomShape)

# create a reversed version of the original grid (to check for verticals)
# when iterated over, the original grid's shapes corresponded to the wrong indices for some reason, which is why this step is crucial
reversedGrid = grid[::-1]

# replace vertical duplicates (the same hape more than two-in-a-row) in all columns with other shapes
column = 0
for outerIndex in range(7):
    for index in range(len(reversedGrid)):
        # check for vertical equals starting from the third hape in the column
        if index >= 1:
            if reversedGrid[index][column] == reversedGrid[index - 1][column] and reversedGrid[index][column] == reversedGrid[index - 2][column]:
                shapesExcludingDuplicate = shapes.copy()
                shapesExcludingDuplicate.remove(reversedGrid[index][column])
                reversedGrid[index][column] = random.choice(shapesExcludingDuplicate)
                del shapesExcludingDuplicate[:]
    column += 1

stddraw.setPenColor(Color(220, 220, 220))

rectCoordinates = []
indices = []
shapesClickedOn = []

# creates the highlight around a selected piece
def drawNavigator(mouseX, mouseY):
    # get the closest center value from the list of center coordinates
    # aka finding the coordinates with the minimum distance from the mouse coordinates
    x = min(centerCoordinatesX, key=lambda x:abs(x - mouseX))
    y = min(centerCoordinatesY, key=lambda y:abs(y - mouseY))
    rectCoordinates.append((x - 0.875, y - 0.875))
    stddraw.rectangle(rectCoordinates[len(rectCoordinates) - 1][0], rectCoordinates[len(rectCoordinates) - 1][1], 1.75, 1.75)

    # to get the indices of the clicked shape
    indices.append((int(abs((y / 2) - 9)), int(x / 2) - 1))
    # get the shape using the indices above
    shapesClickedOn.append(reversedGrid[indices[len(indices) - 1][0]][indices[len(indices) - 1][1]])
    swapShapes()

def swapShapes():
    global boardGrid
    for index in range(len(indices) - 1):
        if (index) % 2 == 0 and len(rectCoordinates) % 2 == 0:
            # get the last elements in the indices list (the two indices which need to be swapped)
            swapIndices = indices[-3:]
            # check if the shapes that need to be swapped are adjacent before swapping
            #if ((abs(abs(indices[index][1]) - abs(indices[index - 1][1])) == 1 and (abs(indices[index][0] - indices[index - 1][0]) == 0)) or (abs(abs(indices[index][0] - abs(indices[index - 1][0])) == 1) and (abs(indices[index][1] - indices[index - 1][1]) == 0))) and not (abs(indices[index][1]) == abs(indices[index - 1][1]) and abs(indices[index][0]) == abs(indices[index - 1][0])):
            if ((abs(abs(indices[index][1]) - abs(indices[index - 1][1])) == 1 and (abs(indices[index][0] - indices[index - 1][0]) == 0)) or (abs(abs(indices[index][0] - abs(indices[index - 1][0])) == 1) and (abs(indices[index][1] - indices[index - 1][1]) == 0))) and not (abs(indices[index][1]) == abs(indices[index - 1][1]) and abs(indices[index][0]) == abs(indices[index - 1][0])):
                #Swap
                reversedGrid[swapIndices[index - 1][0]][swapIndices[index - 1][1]], reversedGrid[swapIndices[index][0]][swapIndices[index][1]] = reversedGrid[swapIndices[index][0]][swapIndices[index][1]], reversedGrid[swapIndices[index - 1][0]][swapIndices[index - 1][1]]
                boardGrid = reversedGrid[::-1]
                if checkForEquals():
                    removeEquals()
                    showBoard(boardGrid)
                else:
                    reversedGrid[swapIndices[index - 1][0]][swapIndices[index - 1][1]], reversedGrid[swapIndices[index][0]][swapIndices[index][1]] = reversedGrid[swapIndices[index][0]][swapIndices[index][1]], reversedGrid[swapIndices[index - 1][0]][swapIndices[index - 1][1]]
                    boardGrid = reversedGrid[::-1]
                del swapIndices[:]
                del indices[:]
            else:
                del swapIndices[:]
                del indices[:]


# reverse the reversed grid to bring it back to normal
boardGrid = reversedGrid[::-1]

reversedBoardGrid = boardGrid[::-1]
def checkForEquals():
    global globalScore
    verticalColumn = 0
    # sleep(0.5)
    for outerIndex in range(len(reversedBoardGrid)):
        consecutiveTaffies = [sum(1 for _ in group) for _, group in groupby(reversedBoardGrid[outerIndex])]
        for index in range(len(consecutiveTaffies)):
            if consecutiveTaffies[index] >= 3:
                # print("equal (horizontal), at indices", outerIndex + 1, index + 1)
                # Append score to globalScore then check if there are any more consecutive taffies
                # return at end of loop
                globalScore.append(consecutiveTaffies[index])
                return True
    for outerIndex in range(7):
        for index in range(len(reversedBoardGrid)):
            if index > 1:
                if (reversedBoardGrid[index][verticalColumn] == reversedBoardGrid[index - 1][verticalColumn] and
                reversedBoardGrid[index][verticalColumn] == reversedBoardGrid[index - 2][verticalColumn]):
                    globalScore.append(3)
                    return True
            elif index > 2:
                if (reversedBoardGrid[index][verticalColumn] == reversedBoardGrid[index - 1][verticalColumn] and
                reversedBoardGrid[index][verticalColumn] == reversedBoardGrid[index - 2][verticalColumn] and
                reversedBoardGrid[index][verticalColumn] == reversedBoardGrid[index - 2][verticalColumn] == reversedBoardGrid[index - 3][verticalColumn]):
                    globalScore.append(4)
                    return True
            elif index > 3:
                if (reversedBoardGrid[index][verticalColumn] == reversedBoardGrid[index - 1][verticalColumn] and
                reversedBoardGrid[index][verticalColumn] == reversedBoardGrid[index - 2][verticalColumn] and
                reversedBoardGrid[index][verticalColumn] == reversedBoardGrid[index - 2][verticalColumn] == reversedBoardGrid[index - 3][verticalColumn] and
                reversedBoardGrid[index][verticalColumn] == reversedBoardGrid[index - 2][verticalColumn] == reversedBoardGrid[index - 3][verticalColumn] == reversedBoardGrid[index - 4][verticalColumn]):
                    globalScore.append(5)
                    return True
        verticalColumn += 1

def fillEmptyTiles():
    for i in range(len(reversedBoardGrid[0])):
        for j in range(len(reversedBoardGrid)):
            if reversedBoardGrid[j][i] == "":
                temp = j
                while temp > 0:
                    reversedBoardGrid[temp][i] = reversedBoardGrid[temp - 1][i]
                    temp -= 1
                reversedBoardGrid[0][i] = random.choice(shapes)

def removeEquals():
    #Horizontal check
    for i in range(len(reversedBoardGrid)):
        for j in range(len(reversedBoardGrid[i]) - 2):
            count = 0
            for k in range(j, len(reversedBoardGrid[i])):
                if reversedBoardGrid[i][k] == reversedBoardGrid[i][j]:
                    count += 1
                else:
                    break
            if count >= 3:
                for k in range(j, j + count):
                    reversedBoardGrid[i][k] = ""

                fillEmptyTiles()
                stddraw.clear(bg)
                showBoard(boardGrid)
                stddraw.show(2000)
                removeEquals()
    #Vertical check
    for i in range(len(reversedBoardGrid[0])):
        for j in range(len(reversedBoardGrid) - 2):
            count = 0
            for k in range(j, len(reversedBoardGrid) - 2):
                if reversedBoardGrid[k][i] == reversedBoardGrid[j][i]:
                    count += 1
                else:
                    break
            if count >= 3:
                for k in range(j, j + count):
                    reversedBoardGrid[k][i] = ""

                fillEmptyTiles()
                stddraw.clear(bg)
                showBoard(boardGrid)
                stddraw.show(500)
                removeEquals()

    # Vertical check
    for i in range(len(reversedBoardGrid[0])):
        for j in range(len(reversedBoardGrid) - 2):
            count = 0
            for k in range(j, len(reversedBoardGrid) - 2):
                if reversedBoardGrid[k][i] == reversedBoardGrid[j][i]:
                    count += 1
                else:
                    break
            if count >= 3:
                for k in range(j, j + count):
                    reversedBoardGrid[k][i] = ""
                fillEmptyTiles()
                stddraw.clear(bg)
                stddraw.show(100)
                showBoard(boardGrid)
                removeEquals()

def showBoard(board):
    stddraw.setPenColor(Color(190, 190, 190))
    stddraw.setFontSize(30)
    stddraw.text(3, 19.25, "Taffy Tangle")
    if len(globalScore) > 0:
        stddraw.text(10, 19.25, "Score: {}".format(sum(globalScore)))
    else:
        stddraw.text(10, 19.25, "Score: 0")
    pictureGrid = []
    for index in range(len(grid)):
        for innerIndex in range(len(grid[index])):
            if board[index][innerIndex] == "":
                pictureGrid.append("empty")
            else:
                pictureGrid.append(board[index][innerIndex])
    pictureIndex = 0
    for outerIndex in range(1, len(grid) + 1):
        for index in range(1, len(grid[outerIndex - 1]) + 1):
            pictureIndex += 1
            if not pictureGrid[pictureIndex - 1] == pictureGrid[pictureIndex - 2] == pictureGrid[pictureIndex - 3]:
                stddraw.picture(picture.Picture(pictureGrid[pictureIndex - 1] + ".png"), index * 2, (outerIndex * 2) - 0)
            else:
                stddraw.picture(picture.Picture(pictureGrid[pictureIndex - 5] + ".png"), index * 2, (outerIndex * 2) - 0)
            if len(rectCoordinates) == 0:
                stddraw.show(20)
stddraw.clear(bg)
while True:
    showBoard(boardGrid)
    if stddraw.mousePressed():
        if len(rectCoordinates) >= 1:
            showBoard(boardGrid)
            stddraw.clear(bg)
        drawNavigator(stddraw.mouseX(), stddraw.mouseY())
    stddraw.show(100)

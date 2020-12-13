#!/usr/bin/python

import os, sys
import json
import numpy as np
import re
import copy

"""
Name:   Irish Senthilkumar
ID:     16342613
Github: 

I have included manual implementations of 5 different problems. The copy library was used to create a deep copy of the
input grid.
"""

### YOUR CODE HERE: write at least three functions which solve
### specific tasks by transforming the input x and returning the
### result. Name them according to the task ID as in the three
### examples below. Delete the three examples. The tasks you choose
### must be in the data/training directory, not data/evaluation.

# This is an exception that will allow us to break from nested loops
class BreakLoop(Exception): pass

def solve_0a938d79(inputGrid):
    """
     - Transformation Process:
        The input matrix has 2 coloured cells on an edge/s of the matrix. In the output matrix, these cells are extended
        up to the opposite edge, forming a procedural pattern up to the end of the matrix.

    - Analysis:
        All training and testing grids were solved correctly.
    """
    # Note: This was the first one that I did, and I can admit that this can be programmed more efficiently. I wanted
    #       to get back to this one and fix the inefficiency but I ran out of time. There is too much repetition in this
    #       function and that could be removed easily!

    # The grids are layed out using (y,x,colour) as the coordinates.
    seeds = []

    # Create a deep copy of the input grid
    output = copy.deepcopy(inputGrid)

    # Store the size of the input grid
    gridXSize = len(inputGrid[0])
    gridYSize = len(inputGrid)
    coloursOnYAxis = True

    # Loop through the edges of the grid and find the 'seeds' which are the coloured cells
    try:
        for xIndex in range(gridXSize):
            # Represents the opposite edges on the x axis
            possibleColourIndexes = [0, gridYSize - 1]

            # Find the seeds on each edge (if they exist on both edges)
            for yIndex in range(len(possibleColourIndexes)):
                colourValue = inputGrid[yIndex][xIndex]
                # If we find a seed
                if colourValue != 0:
                    seeds.append([0, xIndex, colourValue])

                    # Find the remaining seed
                    for yIndex2 in possibleColourIndexes:
                        for xIndex2 in range(gridXSize):
                            colourValue = inputGrid[yIndex2][xIndex2]
                            if colourValue != 0 and xIndex2 != xIndex:
                                seeds.append([gridYSize - 1, xIndex2, colourValue])

                                # Once we find both seeds, specify which axis the coloured bars will be (perpendicular
                                # to the x axis here), and break from the nested loop
                                coloursOnYAxis = True
                                raise BreakLoop

        for yIndex in range(gridYSize):
            # Represents the opposite edges on the y axis
            possibleColourIndexes = [0, gridXSize - 1]

            # Find the seeds on each edge (if they exist on both edges)
            colourValue = inputGrid[yIndex][0]
            for xIndex in possibleColourIndexes:
                # If we find a seed
                if colourValue != 0:
                    seeds.append([yIndex, xIndex, colourValue])

                    # Find the remaining seed
                    for xIndex2 in possibleColourIndexes:
                        for yIndex2 in range(gridYSize):
                            colourValue = inputGrid[yIndex2][xIndex2]
                            if colourValue != 0 and yIndex2 != yIndex:
                                seeds.append([yIndex2, gridYSize - 1, colourValue])

                                # Once we find both seeds, specify which axis the coloured bars will be (perpendicular
                                # to the y axis here), and break from the nested loop
                                coloursOnYAxis = False
                                raise BreakLoop
    except BreakLoop:
        pass

    # Find out how far to extend the lines
    gridConstraint = gridXSize
    if coloursOnYAxis is False:
        seeds[0] = [seeds[0][1], seeds[0][0], seeds[0][2]]
        seeds[1] = [seeds[1][1], seeds[1][0], seeds[1][2]]
        gridConstraint = gridYSize
    # The gap between the lines
    barGap = seeds[0][1] - seeds[1][1]
    # The details of the current line we are painting
    currentPaintAxisValueDetails = [0, 0, 0]

    # Find out which line to draw first
    if barGap < 0:
        currentPaintAxisValueDetails = [seeds[0][1], seeds[0][2], seeds[1][2]]
    elif barGap > 0:
        currentPaintAxisValueDetails = [seeds[1][1], seeds[1][2], seeds[0][2]]

    # A count of how many lines we have drawn so far
    count = 0
    while currentPaintAxisValueDetails[0] < gridConstraint:
        if coloursOnYAxis is True:
            # Draw the line for the first colour
            if count % 2 == 0:
                output[:, currentPaintAxisValueDetails[0]] = currentPaintAxisValueDetails[1]
            # Draw the line for the second colour
            else:
                output[:, currentPaintAxisValueDetails[0]] = currentPaintAxisValueDetails[2]
        else:
            # Draw the line for the first colour
            if count % 2 == 0:
                output[currentPaintAxisValueDetails[0], :] = currentPaintAxisValueDetails[1]
            else:
                # Draw the line for the second colour
                output[currentPaintAxisValueDetails[0], :] = currentPaintAxisValueDetails[2]

        # Set up the 'painter' to draw the next line, taking the gap between the lines into account
        currentPaintAxisValueDetails[0] += abs(barGap)
        count += 1

    return output

def solve_5c0a986e(inputGrid):
    """
     - Transformation Process:
        The input grid has a 2x2 red square and a 2x2 blue square. A bottom-right facing diagonal line trails off from
        the red square, while a top-left facing diagonal line trials off from the blue square. Adding these trails
        gives us the output matrix.

    - Analysis:
        All training and testing grids were solved correctly.
    """
    # Create a deep copy of the input grid
    output = copy.deepcopy(inputGrid)

    # Store the size of the input grid
    gridXSize = len(inputGrid[0])
    gridYSize = len(inputGrid)

    # The important corner of the blue and red squares, and the colours of the diagonal lines which emanate from them
    blueSeed = []
    redSeed = []
    colours = [1, 2]

    try:
        # Loop through the grid
        for yIndex in range(gridYSize):
            for xIndex in range(gridXSize):
                # Finding the top left blue block in the 2x2 blue square
                if inputGrid[yIndex][xIndex] == 1 and blueSeed == []:
                    blueSeed = [yIndex, xIndex]

                # Finding the bottom right red block in the 2x2 blue square
                if inputGrid[yIndex][xIndex] == 2 and redSeed == []:
                    redSeed = [yIndex + 1, xIndex + 1]

                # If we have found both the red and blue squares, we can stop our search
                if redSeed != [] and blueSeed != []:
                    raise BreakLoop
    except BreakLoop:
        pass

    nextIndexes = [[point - 1 for point in blueSeed], [point + 1 for point in redSeed]]
    # Repeat this for both squares
    for i in range(2):
        # Repeat until the diagonal line hits an edge
        while (nextIndexes[i][0] < gridYSize) and (nextIndexes[i][0] >= 0) and \
                (nextIndexes[i][1] < gridXSize) and (nextIndexes[i][1] >= 0):

            output[nextIndexes[i][0]][nextIndexes[i][1]] = colours[i]
            if i == 0:
                nextIndexes[0] = [point - 1 for point in nextIndexes[0]]
            if i == 1:
                nextIndexes[1] = [point + 1 for point in nextIndexes[1]]

    return output

def solve_363442ee(inputGrid):
    """
    - Transformation Process:
        The input grid is seperates by a grey line. The top 3x3 square to the left of the grey line has a specific
        pattern if colours, and we store this pattern. To the right of the grey line, there are a number of blue cells.
        Each blue cell represents a centre point on which the pattern should be applied, therefore we paste the pattern
        onto the blue cells such that a blue cell is in the middle of the 3x3 pattern. This gives us the output matrix.

    - Analysis:
        All training and testing grids were solved correctly.
    """

    # Create a deep copy of the input grid
    output = copy.deepcopy(inputGrid)

    # Store the pattern and the input grid size
    pattern = inputGrid[0:3, 0:3]
    gridXSize = len(inputGrid[0])
    gridYSize = len(inputGrid)

    # Locate the grey line which separates the input grid
    seperatorXIndex = 0
    for xIndex in range(gridXSize):
        if inputGrid[0][xIndex] == 5:
            seperatorXIndex = xIndex
            break
    # Only keep the right hand side of the grey line
    gridXSize = gridXSize - seperatorXIndex

    # Paste the pattern on top of the blue cells, centred on the blue cells
    for yIndex in range(gridYSize):
        for xIndex in range(gridXSize):
            if inputGrid[yIndex][xIndex + seperatorXIndex] == 1:
                output[(yIndex - 1):(yIndex + 2), (xIndex + seperatorXIndex- 1):(xIndex + seperatorXIndex + 2)] = pattern

    return output

def solve_868de0fa(inputGrid):
    """
    - Transformation Process:
        In the input grid, there are a set of 'hollow' squares. In the output, these same 'hollow' squares are filled
        with either a red or orange colour. If the number of cells in one side of the square is even, then the square
        is filled with a red colour. If the number of cells in one side of the square is odd, then the square os filled
        with an orange colour.

    - Analysis:
        All training and testing grids were solved correctly.
    """
    # Create a deep copy of the input grid
    output = copy.deepcopy(inputGrid)

    # Store the size of the input grid
    gridXSize = len(inputGrid[0])
    gridYSize = len(inputGrid)

    discoveredPerimeters = []   # This stores the locations of the cells (y,x) that we already have worked on
    possibleColours = [2, 7]    # The possible colour codes of the filled squares

    # Loop through the grid
    for yIndex in range(gridYSize):
        for xIndex in range(gridXSize):
            # If search through the grid by going from left to right, then going down a row, and repeating this process,
            # the first not previously encountered blue cell is always going to be the top left corner of an
            # undiscovered 'hollow' square
            if (inputGrid[yIndex][xIndex] == 1) and ([yIndex, xIndex] not in discoveredPerimeters):
                topLeft = [yIndex, xIndex]
                currentCoordinate = [yIndex, xIndex]

                # If we go diagonally downwards from this top left blue cell, the next blue cell that we encounter
                # is the bottom right corner of the 'hollow' square. An index error is thrown if we search past the
                # bounds of the grid, and this occurs when the 'hollow' square is up against an edge of the grid
                try:
                    while inputGrid[currentCoordinate[0] + 1][currentCoordinate[1] + 1] != 1:
                        currentCoordinate[0] += 1
                        currentCoordinate[1] += 1
                except IndexError:
                    pass

                bottomRight = [currentCoordinate[0] + 1, currentCoordinate[1] + 1]
                # Store the 'hollow' square itself, and the space within this square that is going to be filled
                # with colour
                zone = inputGrid[topLeft[0]:(bottomRight[0] + 1), topLeft[1]:(bottomRight[1] + 1)]
                internalZone = inputGrid[(topLeft[0] + 1):bottomRight[0], (topLeft[1] + 1):bottomRight[1]]

                # Fill the 'hollow' square with the correct colour
                output[(topLeft[0] + 1):bottomRight[0], (topLeft[1] + 1):bottomRight[1]] = \
                    internalZone + possibleColours[len(zone) % 2]

                # Add every cell in this filled square to the list of cells that we have worked on, so we can
                # ignore this cells in future searches
                for zoneYIndex in range(len(zone)):
                    for zoneXIndex in range(len(zone[0])):
                        discoveredPerimeters.append([zoneYIndex + topLeft[0], zoneXIndex + topLeft[1]])

    return output

def solve_ac0a08a4(inputGrid):
    """
    - Transformation Process:
        We store every unique colour in the input, and create an output matrix that has sides x times the length
        of the input matrix, where x is the number of unique colours observed. The coloured zones still remain in
        the same relative positions in the output, but the number of coloured cells is scaled according to the
        number of unique colours in order to accomodate for the larger outpit matrix. So basically this just
        upscales the grid, and the scaling factor is directly proportional to the number of unique colours.

    - Analysis:
        All training and testing grids were solved correctly.
    """
    # Create a deep copy of the input grid
    output = copy.deepcopy(inputGrid)

    # Store the initial size of the grid
    inputGridXSize = len(inputGrid[0])
    inputGridYSize = len(inputGrid)
    seeds = []  # The seed format is (y position, x position, colour)

    # Loop through the input grid to find the unique colours
    for yIndex in range(inputGridYSize):
        for xIndex in range(inputGridXSize):
            if inputGrid[yIndex][xIndex] != 0:
                seeds.append([yIndex, xIndex, inputGrid[yIndex][xIndex]])

    # Initialise the output grid. This output grid is numberOfUniqueColours times larger than the input grid
    output = np.zeros([inputGridXSize * len(seeds), inputGridYSize * len(seeds)])

    # Upscale the coloured cells
    for seed in seeds:
        output[(seed[0] * len(seeds)):(seed[0] * len(seeds) + len(seeds)),
               (seed[1] * len(seeds)):(seed[1] * len(seeds) + len(seeds))] = seed[2]

    return output

def main():
    # Find all the functions defined in this file whose names are
    # like solve_abcd1234(), and run them.

    # regex to match solve_* functions and extract task IDs
    p = r"solve_([a-f0-9]{8})" 
    tasks_solvers = []
    # globals() gives a dict containing all global names (variables
    # and functions), as name: value pairs.
    for name in globals(): 
        m = re.match(p, name)
        if m:
            # if the name fits the pattern eg solve_abcd1234
            ID = m.group(1) # just the task ID
            solve_fn = globals()[name] # the fn itself
            tasks_solvers.append((ID, solve_fn))

    for ID, solve_fn in tasks_solvers:
        # for each task, read the data and call test()
        directory = os.path.join("..", "data", "training")
        json_filename = os.path.join(directory, ID + ".json")
        data = read_ARC_JSON(json_filename)
        test(ID, solve_fn, data)
    
def read_ARC_JSON(filepath):
    """Given a filepath, read in the ARC task data which is in JSON
    format. Extract the train/test input/output pairs of
    grids. Convert each grid to np.array and return train_input,
    train_output, test_input, test_output."""
    
    # Open the JSON file and load it 
    data = json.load(open(filepath))

    # Extract the train/test input/output grids. Each grid will be a
    # list of lists of ints. We convert to Numpy.
    train_input = [np.array(data['train'][i]['input']) for i in range(len(data['train']))]
    train_output = [np.array(data['train'][i]['output']) for i in range(len(data['train']))]
    test_input = [np.array(data['test'][i]['input']) for i in range(len(data['test']))]
    test_output = [np.array(data['test'][i]['output']) for i in range(len(data['test']))]

    return (train_input, train_output, test_input, test_output)

def test(taskID, solve, data):
    """Given a task ID, call the given solve() function on every
    example in the task data."""
    print(taskID)
    train_input, train_output, test_input, test_output = data
    print("Training grids")
    for x, y in zip(train_input, train_output):
        yhat = solve(x)
        show_result(x, y, yhat)
    print("Test grids")
    for x, y in zip(test_input, test_output):
        yhat = solve(x)
        show_result(x, y, yhat)

def show_result(x, y, yhat):
    print("Input")
    print(x)
    print("Correct output")
    print(y)
    print("Our output")
    print(yhat)
    print("Correct?")
    # if yhat has the right shape, then (y == yhat) is a bool array
    # and we test whether it is True everywhere. if yhat has the wrong
    # shape, then y == yhat is just a single bool.
    print(np.all(y == yhat))

if __name__ == "__main__": main()

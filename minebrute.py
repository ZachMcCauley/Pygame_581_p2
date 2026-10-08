from board import Board
from math import factorial
import itertools

# This is taken from ai_solver.py.
#this function returns every valid row/col touching a cell, this mirrors the Board._neighbors() function
#I wanted to have our own copy here so the AI can use it since it should be private from the Board class
def get_neighbors(board, r, c):
    neighbors = []
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue   #skip the actual cell itself, I only need 8 adjacent cells around it
            nr, nc = r + dr, c + dc
            if 0 <= nr < board.size and 0 <= nc < board.size:
                neighbors.append((nr, nc))
    return neighbors

class Minebrute:
    def __init__(self, board):
        if not isinstance(board, Board):
            raise TypeError("board is not a Board!")
        self.board = board
        # Get a list of positions we know that there must be mines by medium rules:
        # Note that this isn't used in the output value, since we assume that every tile is a mine and safe
        # until proved otherwise there.
        # Don't think about it too hard.
        self._knownMineLocationCache = self.knownMineLocations()

    # board is a Board object, and position is a tuple of two ints.
    # Returns a tuple (clicks, flags)
    # clicks - A set of positions where it is DEFINITELY safe to click
    # flags - A set of positions where there is DEFINITELY a mine
    def minebrute(self, position, maxCombinations = 10):
        # Type checking
        # We love short-circuit functionality in our logical statements.
        # Without it, this expression could cause errors.
        if not (isinstance(position, tuple) and len(position) == 2 and isinstance(position[0], int) and isinstance(position[1], int)):
            raise TypeError("Position must be a 2-tuple of integers!")
        if not isinstance(maxCombinations, int):
            raise TypeError("maxCombinations is not an integer!")
        elif maxCombinations < 0:
            raise ValueError("maxCombinations cannot be negative!")
        # Case : Tile at position is not revealed
        # Also case : tile is a "revealed 0"
        if not self.board.revealed[position[0]][position[1]] or self.board.counts[position[0]][position[1]] == 0:
            # In this case, we conclude nothing.
            return set(), set()
        # Get a list of positions for mines to check in a 3x3 area
        adjacentPos = set()
        minePositions = set()
        safePositions = set()
        for r in range(position[0] - 1, position[0] + 2):
            for c in range(position[1] - 1, position[1] + 2):
                # Check for OOB
                flag1 = r < 0 or r >= self.board.size or c < 0 or c >= self.board.size
                # Check for revealed tiles
                flag2 = None
                try:
                    flag2 = self.board.revealed[r][c]
                except IndexError:
                    flag2 = False
                if flag1 or flag2:
                    continue
                # Add possible location to locations
                adjacentPos.add((r, c))
                minePositions.add((r, c))
                safePositions.add((r, c))
        # Calculate how many combinations without replacement the mines can have in the 3x3 area.
        adjMines = self.board.counts[position[0]][position[1]]
        combinations = int(factorial(len(minePositions)) / (factorial(adjMines) * factorial(len(minePositions) - adjMines)))
        if combinations > maxCombinations:
            raise RuntimeError(f"Maximum combinations ({combinations}) of mines exceeded {maxCombinations}!")
        # Actually calculate and iterate through all of those combinations
        calculatedCombinations = list(itertools.combinations(list(minePositions), adjMines))
        for combo in calculatedCombinations:
            combo = set(combo)
            # The set of all adjacent tiles that we are proposing don't have mine
            antiCombo = adjacentPos.difference(combo)
            # Of course, if we know that there is a mine in antiCombo, this combo is automatically invalid.
            if len(antiCombo.intersection(self._knownMineLocationCache)) > 0:
                continue
            # Determine if this breaks any tile's mine count in a 5x5 area.
            validConfiguration = True
            for r in range(position[0] - 2, position[0] + 3):
                for c in range(position[1] - 2, position[1] + 3):
                    try:
                        validConfiguration = not self.breaksRule((r, c), combo, antiCombo)
                    except IndexError:
                        continue
                    if not validConfiguration:
                        break
                if not validConfiguration:
                    break
            # If the configuration is plausible, we can operate on it:
            if validConfiguration:
                minePositions = minePositions.intersection(combo)
                safePositions = safePositions.difference(combo)
        # Assert that there is no overlap between minePositions and safePositions
        if len(minePositions.intersection(safePositions)) > 0:
            raise RuntimeError("Somehow, a tile is confirmed to both have and not have a mine. This is scary.")
        """
        While this check was made in good faith, it was removed because the cached mine locations included locations outside the scope of the area being checked.
        
        if len(self._knownMineLocationCache.difference(minePositions)) > 0:
            raise RuntimeError("A mine that would be found by the medium AI was not found by the hard AI!") 
        """
        # Return the values
        return safePositions, minePositions

    # A rule is defined to be broken if the number of mines in a 3x3 area exceeds the center space's number,
    # And the tile is revealed.
    # If the number of mines is less than the tile's number, it is still plausible since there may be mines we don't know about yet.
    # In addition, if it's impossible to have enough mines to satisfy the number on the tile, that is also illegal.
    def breaksRule(self, position, mines, notMines):
        # Type checking
        if not (isinstance(position, tuple) and len(position) == 2 and isinstance(position[0], int) and isinstance(position[1], int)):
            raise TypeError("Position must be a 2-tuple of integers!")
        if not isinstance(mines, set):
            raise TypeError("Mines should be a proposed set of mine positions!")
        if position[0] < 0 or position[1] < 0 or position[0] >= self.board.size or position[1] >= self.board.size:
            raise IndexError("Position out of bounds!")
        # We can't break a rule for a tile we don't know
        if not self.board.revealed[position[0]][position[1]]:
            return False
        expectedAdjacentMines = self.board.counts[position[0]][position[1]]
        actualMines = 0
        possibleMines = 0
        # Iterate through adjacent spaces
        for r in range(position[0] - 1, position[0] + 2):
            for c in range(position[1] - 1, position[1] + 2):
                # OOB - Continue
                if r < 0 or r >= self.board.size or c < 0 or c >= self.board.size:
                    continue
                # Mine detected - Increment added mines.
                mineContradiction = (r, c) in notMines
                if not mineContradiction and ((r, c) in self._knownMineLocationCache or (r, c) in mines):
                    actualMines += 1
                    possibleMines += 1
                elif not mineContradiction and not self.board.revealed[r][c]:
                    possibleMines += 1
        return (actualMines > expectedAdjacentMines) or (possibleMines < expectedAdjacentMines)

    # Get the set of positions on the board which are known to contain mines for sure.
    # We use this instead of flags, as it is more reliable than trusting something the user can control.
    def knownMineLocations(self):
        toReturn = set()
        for r in range(self.board.size):
            for c in range(self.board.size):
                if not self.board.revealed[r][c] or self.board.counts[r][c] == 0:
                    continue
                unrevealedSpaces = set()
                neighbors = get_neighbors(self.board, r, c)
                for neighbor in neighbors:
                    if not self.board.revealed[neighbor[0]][neighbor[1]]:
                        unrevealedSpaces.add(neighbor)
                if self.board.counts[r][c] == len(unrevealedSpaces):
                    toReturn = toReturn.union(unrevealedSpaces)
        return toReturn
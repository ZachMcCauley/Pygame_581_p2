"""
AI Solver Module

This module is my implementation of the AI Solver for the other Group's Minesweeper game. 
I started by creating a version of the easy-AI mode, so I could build upon it and make the medium-AI mode.
The hard-AI mode is still under development, and I wanted to talk to other group members before moving on.

The AI doesn't touch pygame ore the mouse at all, it just calls the same Board methods a real player's click would trigger
like the reveal/toggle flag, using row/col cords actions

Author: Jett Viduya
"""

import random

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


#function to return every row/col the AI will be allowed to use/click on
#any cell that isn't already opened and doesn't have a flag on it will be considered valid for the AI to click on

def get_valid_moves(board):
    valid_moves = []
    for r in range(board.size):
        for c in range(board.size):
            if not board.revealed[r][c] and not board.flagged[r][c]:
                valid_moves.append((r, c))
    return valid_moves


#easy difficulty AI: no strategy, just picks random legal cell and opens it.
#returns the row/col of the chosen cell, or none if the board is finished/every cell is flagged

def ai_easy_move(board):
    valid_moves = get_valid_moves(board)
    if not valid_moves:
        return None

    r, c = random.choice(valid_moves)
    board.reveal(r,c)
    return (r, c)


#medium difficulty AI: this has the basic strategy  of the two logic rules from the spec before falling back to a random click
#rule 1 = look at a revealed #. If the # of hidden neighbors = equals that #, every one of those should be a mine --> so just flag all of it
#rule 2 = look at a revealed #. If the # of flagged neighbors = that #, every other hidden neighbor should be safe --> so just reveal all of them

#we only read board.counts for the cells that are already revealed. Reading that # on a hidden cell would sorta be cheating and the player can't see that
#returns true if the AI made a move either normal/random, false if there were no legal moves left

#scan the board looking a revealed # and the AI applies the two rules

def ai_medium_move(board):
    for r in range(board.size):
        for c in range(board.size):
            if not board.revealed[r][c]:
                continue  #skip hidden cells, we only apply rules to revealed numbers

            number = board.counts[r][c]
            if number == 0:
                continue  #skip cells with 0, they have no useful information for the AI

            neighbors = get_neighbors(board, r, c)
            hidden_neighbors = [(nr, nc) for nr, nc in neighbors if not board.revealed[nr][nc]]
            flagged_neighbors = [(nr, nc) for nr, nc in neighbors if board.flagged[nr][nc]]
            unflagged_neighbors = [(nr, nc) for nr, nc in hidden_neighbors if not board.flagged[nr][nc]]

            #nothing left to do if there are no hidden neighbors
            if not unflagged_neighbors:
                continue

            #rule 1: if the number of hidden neighbors equals the number on the cell, flag all hidden neighbors
            if len(hidden_neighbors) == number:
                for nr, nc in unflagged_neighbors:
                    board.toggle_flag(nr, nc)
                return True  # rule 1 applied successfully


            #rule 2: enough flags around a revealed number means all other hidden neighbors are safe to reveal
            if len(flagged_neighbors) == number:
                for nr, nc in unflagged_neighbors:
                    board.reveal(nr, nc)
                    if board.game_over:
                        return True  # stop early if that move ended the game
                return True  # rule 2 applied successfully

    #if we get here, no rules could be applied, so fall back to a random move
    return ai_easy_move(board) is not None




            
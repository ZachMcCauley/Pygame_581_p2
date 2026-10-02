"""
AI Solver Test Script 

this script tests the AI solver by running multiple games and recording the outcomes.

Author: Jett Viduya
"""
from board import Board
from ai_solver import ai_medium_move    #CHANGE THIS IMPORT TO SWITCH AI DIFFICULTY

NUM_GAMES = 100
wins =  0
losses = 0
crashes = 0

for i in range(NUM_GAMES):
    board = Board(10, 15)  #create a new board/game
    moves = 0
    try:
        while not board.game_over and moves < 200:
            ai_medium_move(board) #CHANGE THIS TO SWITCH AI DIFFICULTY
            moves += 1
    except Exception as e:
        crashes += 1
        print(f"Game {i} crashed with the error: {e}")
        continue

    if board.won:
        wins += 1
    else:
        losses += 1

print(f"\nOut of {NUM_GAMES} games:")
print(f"Wins: {wins}")
print(f"Losses: {losses}")
print(f"Crashes: {crashes}")
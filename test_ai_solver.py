"""
AI Solver Test Script 

this script tests the AI solver by running multiple games and recording the outcomes.

Author: Jett Viduya
"""
from board import Board
from ai_solver import ai_easy_move, ai_medium_move, ai_hard_move    #CHANGE THIS IMPORT TO SWITCH AI DIFFICULTY
from sys import argv

NUM_GAMES = 100
wins =  0
losses = 0
crashes = 0

difficulty = None
try:
    match argv[1]:
        case "easy":
            difficulty = 0
        case "medium":
            difficulty = 1
        case "hard":
            difficulty = 2
        case _:
            difficulty = 1
            print("Disambiguating difficulty to medium.")
except IndexError:
    print("Disambiguating difficulty to medium.")
    difficulty = 1

for i in range(NUM_GAMES):

    board = Board(10, 15)  #create a new board/game
    moves = 0
    try:
        while not board.game_over and moves < 200:
            match difficulty:
                case 0:
                    ai_easy_move(board)
                case 1:
                    ai_medium_move(board)
                case 2:
                    ai_hard_move(board)
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
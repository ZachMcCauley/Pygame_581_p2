# EECS 581 Project 1: Minesweeper
---
## Group 22
**Project Manager:** Nathan Richardson

**Game Logic:** Aidan Prather, Dillon Figueredo

**UI/Input Handling:** Maxwell Phachanla, Warren Tan

**Testing:** Fabrizio Gonzalez

**Documentation:** Cyn Tran

---
## Overview
This project implements the classic Minesweeper game using the Pygame module for Python. Users can play on a 10x10 grid with a slected amount of mines ranging from 10 to 20. Main.py handles the creation of UI elements and handles the input of users, button.py is the class file of the rectnagle elements that makeup the UI, and board.py is the actually game logic.

A more extensive explanation of the code can be found in the Architecture Documentation file under Documents and Logs. The test cases used during testing can be found in minesweeper_testing_documentation.pdf. Requirements.txt contains the necessary dependancies to run this program.

---
## Documentation
- Architecture Documentation: Contains an in-depth overview of the system architecture including the system components, data flow, and key data structures.
- Meeting Logs: Contains the notes for each weekly sprint meeting with clearly defined roles and goals.
- Tickets + Activity Log: Breaks the project down to specific tasks, and tracks who has completed what tasks and how long it took them. Due to the simplicity of the project, a simple time estimation was calculated by the respective claimant rather than using traditional story points.

---
## Installation
This program requires pygame to be installed. Note that pygame is not compatible with 3.14.x or any release past that. Pygame can be installed regularly, or through a virtual environment as shown below:
1. Clone the repository using the terminal: `git clone insertRepoLink`
2. Once you are in the directory, create a virtual environment using `py -3.13 -m venv .venv` for windows or for linux `python3 -m venv .venv`
3. Activate the virtual environment using `.\.venv\Scripts\Activate.ps1` for windows or for linux `source .venv/bin/activate`
4. Now your terminal begins with something akin to `(.venv) PS C:\Users\YourName\pygame-game>` and `python --version` is 3.13.x
5. Install the dependencies through `python -m pip install -r requirements.txt` or `python -m pip install pygame`
6. Run the program with `Python main.py`

The interface to play the game wil pop-up, and you can start the game by selecting the amount of mines and using left-click to reveal a tile, and right-click to flag a tile.

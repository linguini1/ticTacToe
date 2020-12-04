# Matteo Golin
# Tic Tac Toe Game with AI

# Imports
import random

# Difficulty easy by default
difficulty = "1"

# Global variables
pOneScore = 0
pTwoScore = 0
lastMove = (0, 0)

# PvP or PvC selection
while True:

    PvP = input("Will you play against another player using the keyboard (1) or against the computer (2): ")

    if PvP == "1":
        PvP = True  # PvP is selected
        break

    elif PvP == "2":
        PvP = False  # PvC is selected

        # Difficulty selection
        while True:

            difficulty = input("Select easy (1), medium (2) or hard (3) mode: ")

            if difficulty not in ["1", "2", "3"]:  # Must be valid option
                print("You must select option 1, 2 or 3.")

            else:
                break

        break

    else:
        print("You must select option 1 or option 2.")  # Wrong input, try again

# How many rounds
while True:

    roundCount = input("Number of rounds you want to play: ")

    try:
        roundCount = int(roundCount)  # Converting to an integer so the game logic works
    except ValueError:  # User gave a non-integer input
        print("You must select a valid integer!")

    if roundCount < 1:
        print("You need a number greater than zero, genius!")  # User gave an integer less than one
    else:
        break

# Initial instructions
if PvP:  # Changing p1 and p2 names based on who is the opponent
    pOne = "Player 1"
    pTwo = "Player 2"
else:
    pOne = "You"
    pTwo = "The Computer"

print(f"""
{pOne} will use the letter X.
{pTwo} will use the letter O.

Each column corresponds to a number. Input your numbers together with no spaces (12, 32, 23, etc.).
                                        
                                           1   2   3
                                        
                                     1   | X | O | X |
                                         -------------
                                     2   | O | X | O |
                                         -------------
                                     3   | X | O | X |

For example, there is an X at spot 11, 13, 22, 31 and 33.
""")


# Function for printing board
def board_printer(board):

    print("-------------")  # Initial row cap

    # Printing the values for each spot of every row
    for row in range(3):
        for column in board[row]:
            print(f"| {column} ", end="")
        print("|\n-------------")  # Ending row with the final vertical line and printing the last horizontal bar

    print("")  # Ending with a line break


# Function for making moves
def make_move(player, board):

    # Getting player name for customization
    if player:
        name = "Player 1"
    else:
        name = "Player 2"

    # Getting coordinates
    while True:

        coOrds = input(f"Coordinates for {name}'s move: ")

        if coOrds not in ['11', '12', '13',  # Coordinates must be one of these values
                          '21', '22', '23',
                          '31', '32', '33']:
            print("You did not input a valid set of coordinates!")
        else:
            # Formatting coordinates
            row = int(coOrds[0]) - 1  # Makes this start at index 0
            column = int(coOrds[1]) - 1  # Makes this start at index 0
            global lastMove
            lastMove = (row, column)  # Recording last move

            # Checking if the spot is already full
            if board[row][column] != " ":
                print("Oops, this space is already filled! Try again!")
            else:
                break

    # Adding move to board
    if player:  # Player one
        board[row][column] = "X"

    else:  # Player two
        board[row][column] = "O"

    # Printing board
    board_printer(board)


# Function for AI moves
def computer_move(diff, board):

    # Easy
    if diff == "1":

        # Looping until computer selects a valid move
        while True:
            # Randomly selecting a coordinate
            coOrds = random.choice([[0, 0], [0, 1], [0, 2],
                                    [1, 0], [1, 1], [1, 2],
                                    [2, 0], [2, 1], [2, 2]])

            # Checking if space is filled
            if board[coOrds[0]][coOrds[1]] != " ":
                pass
            else:
                board[coOrds[0]][coOrds[1]] = "O"
                break

        # Printing results of move
        print(f"The Computer selected the spot {coOrds[0] + 1}{coOrds[1] + 1}.")
        board_printer(board)

    # Medium
    elif diff == "2":

        # Assuming no spot was selected
        spotSelected = False

        # Trying to find an open spot in the diagonal
        leftDiagonal = [(0, 0), (1, 1), (2, 2)]  # Left diagonal coordinates
        rightDiagonal = [(0, 2), (1, 1), (2, 0)]  # Right diagonal coordinates

        if lastMove in leftDiagonal:  # If the last move looks like a left diagonal play

            for spot in leftDiagonal:  # Occupying a remaining left diagonal space
                if board[spot[0]][spot[1]] == " ":  # Checking to make sure space is empty
                    board[spot[0]][spot[1]] = "O"  # Filling space
                    coOrds = spot  # Recording the final spot
                    spotSelected = True  # Recording that a spot was chosen
                    break
                else:
                    spotSelected = False

        elif lastMove in rightDiagonal:  # If the last move looks like a right diagonal play

            for spot in rightDiagonal:  # Occupying a remaining right diagonal space
                if board[spot[0]][spot[1]] == " ":
                    board[spot[0]][spot[1]] = "O"
                    coOrds = spot
                    spotSelected = True
                    break
                else:
                    spotSelected = False

        # Diagonal spot not possible
        if not spotSelected:

            # Selecting whether to occupy a space in the same row or column
            rowOrColumn = random.randint(1, 2)

            if rowOrColumn == 1:  # Row

                for index in range(3):  # Looping through indexes from 0-2
                    # Trying to find an open spot in the same row
                    try:
                        if board[lastMove[0]][lastMove[1] + index] == " ":
                            board[lastMove[0]][lastMove[1] + index] = "O"
                            spotSelected = True
                            coOrds = (lastMove[0], lastMove[1] + index)
                            break
                        else:
                            pass
                    except IndexError:
                        pass

            else:  # Column

                for index in range(3):  # Looping through indexes from 0-2
                    # Trying to find an open spot in the same column
                    try:
                        if board[lastMove[0] + index][lastMove[1]] == " ":
                            board[lastMove[0] + index][lastMove[1]] = "O"
                            spotSelected = True
                            coOrds = (lastMove[0] + index, lastMove[1])
                            break
                        else:
                            pass
                    except IndexError:
                        pass

        # Neither diagonal nor row/column worked
        if not spotSelected:

            # Looping until computer selects a valid move
            while True:
                # Randomly selecting a coordinate
                coOrds = random.choice([[0, 0], [0, 1], [0, 2],
                                        [1, 0], [1, 1], [1, 2],
                                        [2, 0], [2, 1], [2, 2]])

                # Checking if space is filled
                if board[coOrds[0]][coOrds[1]] != " ":
                    pass
                else:
                    board[coOrds[0]][coOrds[1]] = "O"
                    break

        # Printing results
        print(f"The Computer selected the spot {coOrds[0] + 1}{coOrds[1] + 1}.")
        board_printer(board)

    # Hard
    else:
        pass


# Logic for detecting win
def win_detect(board):

    # Assume no win
    win = False
    winner = None

    # Checking straight wins
    for index in range(3):

        # Checking for horizontal win
        if board[index][0] == board[index][1] == board[index][2] != " ":
            win = True
            winner = board[index][0]
            break

        # Checking for vertical win
        elif board[0][index] == board[1][index] == board[2][index] != " ":
            win = True
            winner = board[0][index]
            break

    # Checking for diagonal win
    if board[0][0] == board[1][1] == board[2][2] != " ":
        win = True
        winner = board[0][0]
    elif board[0][2] == board[1][1] == board[2][0] != " ":
        win = True
        winner = board[1][1]

    # Returning the win and winner

    if win:
        # Customizing output to match the player who one
        if winner == "X":
            print(f"The winner was {pOne}!\n")
            global pOneScore
            pOneScore += 1
        else:
            print(f"The winner was {pTwo}!\n")
            global pTwoScore
            pTwoScore += 1

    return win


# While loop to keep the game going for the number of rounds specified
while roundCount > 0:

    # Initializing empty board for each new round
    gameBoard = [[" ", " ", " "],
                 [" ", " ", " "],
                 [" ", " ", " "]]

    # Dividing line
    for _ in range(100):
        print("-", end="")
    print("\n")  # 2 new lines

    # Printing the start board
    print(f"Game {roundCount} has started!")  # Round number
    board_printer(gameBoard)

    # Max moves variable to determine when game must stop
    maxMoves = 9

    # Getting moves
    while maxMoves > 0:

        # Player two is second, so they will always play when the number of moves left is even
        if maxMoves % 2 == 0:
            if PvP:  # PvP logic
                make_move(False, gameBoard)

            else:  # PvC logic
                computer_move(difficulty, gameBoard)

        else:  # Player one is first, so they will always play when the number of moves left is odd
            make_move(True, gameBoard)

        # Reducing the number of remaining moves
        maxMoves -= 1

        # Checking for winner
        if win_detect(gameBoard):
            print("Score Update")
            print(f"{pOne}: {pOneScore}")  # Printing p1 score
            print(f"{pTwo}: {pTwoScore}\n")  # Printing p2 score
            break  # Starts next round
        else:
            pass  # Continues game with no win

    # If game ends as a tie
    if maxMoves == 0:
        print("This game was a tie!\n")
        print("Score Update")
        print(f"{pOne}: {pOneScore}")  # Printing p1 score
        print(f"{pTwo}: {pTwoScore}\n")  # Printing p2 score

    # Reducing round count after game finishes
    roundCount -= 1

# Displaying final scores
print("Final Scores")
print(f"{pOne}: {pOneScore}")
print(f"{pTwo}: {pTwoScore}\n")

# Checking for winner overall
if pOneScore > pTwoScore:
    finalWinner = pOne  # p1 wins
else:
    finalWinner = pTwo  # p2 wins

# Printing overall winner
print(f"Final winner is {finalWinner}!")

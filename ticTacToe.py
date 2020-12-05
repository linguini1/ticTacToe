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
roundCount = 3
scoreCap = 2

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

The default rules use a game of {roundCount} rounds and {scoreCap} victories to win.
""")

# Rule selection
while True:

    changeRules = input("Use the default rules (1) or set custom rules (2): ")

    if changeRules not in ["1", "2"]:  # Invalid selection
        print("Pick option 1 or 2.")

    else:  # Valid selection

        if changeRules == "1":  # Keep the default rules
            break

        else:  # Change rules
            while True:  # Looping for input

                roundCount = input("Number of rounds (must be odd): ")

                try:
                    roundCount = int(roundCount)  # Attempt to convert input to integer

                    if roundCount <= 0:  # Zero or less
                        print("Number of rounds must be above 0!")

                    if roundCount % 2 == 0:  # Even
                        print("Number of rounds must be odd!")

                    else:  # Odd
                        scoreCap = round(roundCount / 2 + 0.5)

                        # Singular or plural depending on score cap
                        if scoreCap > 1:
                            victory = "victories"
                        else:
                            victory = "victory"

                        # Printing user set rules
                        print(f"Your game will have {roundCount} rounds "
                              f"and require {scoreCap} {victory} to win.")
                        break

                except ValueError:  # User didn't give an integer
                    print("You must input an integer!")

            break


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
        diagonals = [leftDiagonal, rightDiagonal]

        for _ in range(2):

            if lastMove in diagonals[_] and not spotSelected:  # If the last move looks like a diagonal play

                for spot in leftDiagonal:  # Occupying a remaining diagonal space
                    if board[spot[0]][spot[1]] == " ":  # Checking to make sure space is empty
                        board[spot[0]][spot[1]] = "O"  # Filling space
                        coOrds = spot  # Recording the final spot
                        spotSelected = True  # Recording that a spot was chosen
                        break
                    else:
                        spotSelected = False

        # Diagonal spot not possible
        if not spotSelected:

            # Selecting whether to occupy a space in the same row or column
            rowOrColumn = random.randint(1, 2)

            for index in range(3):  # Looping through indexes from 0-2

                if rowOrColumn == 1:  # Row
                    row = lastMove[0]
                    column = lastMove[1] + index

                else:  # Column
                    row = lastMove[0] + index
                    column = lastMove[1]

                # Trying to find an open spot in the same line
                try:
                    if board[row][column] == " ":
                        board[row][column] = "O"
                        spotSelected = True
                        coOrds = (row, column)
                        break
                    else:
                        pass
                except IndexError:
                    pass

        # Neither diagonal nor row/column worked
        if not spotSelected:
            computer_move("1", board)
        else:
            # Printing results
            print(f"The Computer selected the spot {coOrds[0] + 1}{coOrds[1] + 1}.")
            board_printer(board)

    # Hard
    else:

        # The crucial first move
        if maxMoves == 8:

            if lastMove == (1, 1):  # If center space is chosen, pick a corner
                coOrds = (0, 2)
                board[0][2] = "O"
                spotFound = True

            else:  # If any other space is chosen, pick center
                coOrds = (1, 1)
                board[1][1] = "O"
                spotFound = True

        # After the first move
        else:

            # Checking for two Xs/Os in a line to block or get win
            spotFound = False  # Assuming no spot found

            # Arrays for O count
            oCountRows = [0, 0, 0]
            oCountColumns = [0, 0, 0]
            oCountDiagonals = [0, 0]

            # Arrays for X count
            xCountRows = [0, 0, 0]
            xCountColumns = [0, 0, 0]
            xCountDiagonals = [0, 0]

            # Diagonal coordinates
            leftDiagonal = [(0, 0), (1, 1), (2, 2)]
            rightDiagonal = [(0, 2), (1, 1), (2, 0)]
            diagonals = [leftDiagonal, rightDiagonal]

            # Actually counting Xs/Os

            for _ in range(2):  # Starting to check for wins with Os, and then block the Xs as a second priority

                if _ == 0:  # For Os
                    rowCount = oCountRows
                    columnCount = oCountColumns
                    diagonalCount = oCountDiagonals
                    character = "O"
                else:  # For Xs
                    rowCount = xCountRows
                    columnCount = xCountColumns
                    diagonalCount = xCountDiagonals
                    character = "X"

                # Counting characters in rows
                for row in range(3):
                    for column in board[row]:
                        if column == character:
                            rowCount[row] += 1

                # Counting characters in columns
                for row in range(3):
                    for column in range(3):
                        if board[column][row] == character:
                            columnCount[row] += 1

                # Counting characters in diagonals
                for _ in range(2):  # 0 = left diagonal, 1 = right diagonal | loops through both
                    for coSet in diagonals[_]:
                        if board[coSet[0]][coSet[1]] == character:
                            diagonalCount[_] += 1

                # Filling spaces

                # Filling row if there's 2 Os
                for row in range(3):  # Each row
                    if rowCount[row] == 2 and not spotFound:  # If there's 2 Xs/Os and no spot has been filled yet
                        for column in range(3):  # Each column of the row

                            if board[row][column] == " ":  # If there's an empty space
                                board[row][column] = "O"  # Occupy it
                                coOrds = (row, column)  # Record move
                                spotFound = True  # Spot has been found
                                break  # We're done

                # Filling column if there's 2 Xs
                for column in range(3):  # Each column
                    if columnCount[column] == 2 and not spotFound:  # If there's 2 Xs/Os and no spot has been filled yet
                        for row in range(3):  # Each row of the column

                            if board[row][column] == " ":  # If there's an empty spot
                                board[row][column] = "O"  # Occupy it
                                coOrds = (row, column)  # Record move
                                spotFound = True  # Spot has been found
                                break  # We're done

                # Filling diagonal if there's 2 Os
                for index in range(2):  # Selecting left diagonal (0) or right diagonal (1)

                    if diagonalCount[index] == 2 and not spotFound:  # If there's 2 Xs/Os and we haven't found a spot
                        for coSet in diagonals[index]:  # For coordinates in the selected diagonal

                            if board[coSet[0]][coSet[1]] == " ":  # If there's an empty space
                                board[coSet[0]][coSet[1]] = "O"  # Occupy it
                                coOrds = (coSet[0], coSet[1])  # Record move
                                spotFound = True  # Spot has been found
                                break  # We're done

        if not spotFound:
            computer_move("2", board)
        else:
            # Printing results
            print(f"The Computer selected the spot {coOrds[0] + 1}{coOrds[1] + 1}.")
            board_printer(board)


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
while roundCount > 0 and pOneScore < scoreCap and pTwoScore < scoreCap:

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

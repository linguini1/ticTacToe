# Matteo Golin
# Tic Tac Toe Game with AI

# Imports
import random
import time

# Difficulty easy by default
difficulty = "1"

# Global variables
pOneScore = 0
pTwoScore = 0
lastMove = (0, 0)
lastCompMove = (0, 0)
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

            difficulty = input("Select easy (1), medium (2), hard (3) or impossible (4) mode: ")

            if difficulty not in ["1", "2", "3", "4"]:  # Must be valid option
                print("You must select option 1, 2, 3 or 4.")

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

Each row and column corresponds to a number.
Input your numbers in the format [row][column] together with no spaces (12, 32, 23, etc.)

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


# Function for animation
def play_animation(frames):

    # Animation while player registers the computer's winning move
    index = 0  # Indexing variable for tracking frames
    animation = ["| Loading...", "/ Loading...", "- Loading...", "\\ Loading..."]  # Actual animation

    while index < frames:  # 0.1s x frames = # of seconds
        print(animation[index % len(animation)], end="\r")  # Printing next animation frame based on cycle
        index += 1  # Increasing index
        time.sleep(0.1)  # Waiting 0.1 seconds before next frame


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

    # Finding Xs and Os in a line function, for blocking or getting a winning line
    def block_and_win():

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
                if rowCount[row] == 2:  # If there's 2 Xs/Os and no spot has been filled yet
                    for column in range(3):  # Each column of the row

                        if board[row][column] == " ":  # If there's an empty space
                            board[row][column] = "O"  # Occupy it
                            coOrds = (row, column)  # Record move
                            return True, coOrds  # Spot found

            # Filling column if there's 2 Xs
            for column in range(3):  # Each column
                if columnCount[column] == 2:  # If there's 2 Xs/Os and no spot has been filled yet
                    for row in range(3):  # Each row of the column

                        if board[row][column] == " ":  # If there's an empty spot
                            board[row][column] = "O"  # Occupy it
                            coOrds = (row, column)  # Record move
                            return True, coOrds  # Spot found

            # Filling diagonal if there's 2 Os
            for index in range(2):  # Selecting left diagonal (0) or right diagonal (1)

                if diagonalCount[index] == 2:  # If there's 2 Xs/Os and we haven't found a spot
                    for coSet in diagonals[index]:  # For coordinates in the selected diagonal

                        if board[coSet[0]][coSet[1]] == " ":  # If there's an empty space
                            board[coSet[0]][coSet[1]] = "O"  # Occupy it
                            coOrds = (coSet[0], coSet[1])  # Record move
                            return True, coOrds  # Spot found

        return False, (0, 0)
    
    # Last computer move variable
    global lastCompMove

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
        lastCompMove = coOrds  # Saving last computer move
        board_printer(board)

    # Medium
    elif diff == "2":

        # Assuming no spot was selected
        spotFound = False
        
        if not spotFound:
            (spotFound, coOrds) = block_and_win()  # Checking for 2 Xs/Os in a row to block or win

        # Trying to find an open spot in the diagonal
        leftDiagonal = [(0, 0), (1, 1), (2, 2)]  # Left diagonal coordinates
        rightDiagonal = [(0, 2), (1, 1), (2, 0)]  # Right diagonal coordinates
        diagonals = [leftDiagonal, rightDiagonal]

        for _ in range(2):

            if lastMove in diagonals[_] and not spotFound:  # If the last move looks like a diagonal play

                for spot in leftDiagonal:  # Occupying a remaining diagonal space
                    if board[spot[0]][spot[1]] == " ":  # Checking to make sure space is empty
                        board[spot[0]][spot[1]] = "O"  # Filling space
                        coOrds = spot  # Recording the final spot
                        spotFound = True  # Recording that a spot was chosen
                        break
                    else:
                        spotFound = False

        # Diagonal spot not possible
        if not spotFound:

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
                        spotFound = True
                        coOrds = (row, column)
                        break
                    else:
                        pass
                except IndexError:
                    pass

        # Neither diagonal nor row/column worked
        if not spotFound:
            computer_move("1", board)
        else:
            # Printing results
            print(f"The Computer selected the spot {coOrds[0] + 1}{coOrds[1] + 1}.")
            lastCompMove = coOrds  # Saving last computer move
            board_printer(board)

    # Hard
    elif diff == "3":

        (spotFound, coOrds) = block_and_win()  # Check if 2 Xs/Os in a row to block or win

        if not spotFound:  # If a move still isn't made, it checks to do a corner block

            corners = [(0, 0), (0, 2), (2, 0), (2, 2)]  # Corner coordinates

            for spot in corners:  # All corner spaces

                xFoundRow = False  # X in row boolean reset to false for every iteration
                xFoundColumn = False  # X in column boolean reset to false for every iteration

                for _ in range(3):  # Coordinates from 0-2 for iterating

                    if board[spot[0]][_] == "X" and spot[0] != _:  # X found in the row of corner space
                        xFoundRow = True

                    if board[_][spot[0]] == "X" and spot[0] != _:  # X found in the column of corner space
                        xFoundColumn = True

                # Tracking Os in the center row and column
                oCountCenterRow = 0
                oCountCenterColumn = 0

                # Don't skip the corner block
                skip = False

                # Counting Os in the center rows and columns
                for _ in range(3):  # Iterating coordinates

                    if board[1][_] == "O":  # Rows
                        oCountCenterRow += 1

                    if board[_][1] == "O":  # Columns
                        oCountCenterColumn += 1

                if oCountCenterColumn == 2 or oCountCenterRow == 2:  # If win scenario possible, skip corner block
                    skip = True  # This sends us to the next part of the algorithm which creates an inevitable win

                if lastMove in corners:  # This avoids the triple corner trap
                    skip = True

                # Condition to save space for next if statement
                condition = xFoundRow and xFoundColumn and not skip and board[spot[0]][spot[1]] == " "

                if condition:  # X found in lines that intersect at specified corner, and win scenario set-up impossible
                    board[spot[0]][spot[1]] = "O"  # Place an O
                    spotFound = True  # Spot has been found
                    coOrds = (spot[0], spot[1])  # Record coordinates
                    break  # Stop searching

        if not spotFound:  # If move still not made, it checks to set up a win scenario

            for _ in range(3):

                if board[lastCompMove[0]][_] == " ":  # If there's a space in the row
                    board[lastCompMove[0]][_] = "O"
                    spotFound = True
                    coOrds = (lastCompMove[0], _)
                    break

                if board[_][lastCompMove[1]] == " ":  # If there's a space in the column
                    board[_][lastCompMove[1]] = "O"
                    spotFound = True
                    coOrds = (_, lastCompMove[1])
                    break

        if not spotFound:  # If none of the above works, use the medium difficulty algorithm
            computer_move("2", board)

        else:  # Printing the results only if the hard mode HAS found a spot in order to avoid recursive printing
            # Printing results
            print(f"The Computer selected the spot {coOrds[0] + 1}{coOrds[1] + 1}.")
            lastCompMove = coOrds  # Saving last computer move
            board_printer(board)

    # Impossible
    else:

        # The crucial first move
        if maxMoves == 8:

            if lastMove == (1, 1):  # If center space is chosen, pick a corner
                coOrds = (0, 2)
                board[0][2] = "O"

            else:  # If any other space is chosen, pick center
                coOrds = (1, 1)
                board[1][1] = "O"

            # Printing results
            print(f"The Computer selected the spot {coOrds[0] + 1}{coOrds[1] + 1}.")
            lastCompMove = coOrds  # Saving last computer move
            board_printer(board)

        # After the first move
        else:
            computer_move("3", board)  # Calling the hard difficulty


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


# Setting originalRoundCount equal to the original roundCount selected by user
originalRoundCount = roundCount

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
    print(f"Game {originalRoundCount + 1 - roundCount} has started!")  # Round number
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
            play_animation(30)
            print("Score Update")
            print(f"{pOne}: {pOneScore}")  # Printing p1 score
            print(f"{pTwo}: {pTwoScore}\n")  # Printing p2 score
            break  # Starts next round
        else:
            pass  # Continues game with no win

    # If game ends as a tie
    if maxMoves == 0:
        play_animation(30)
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
elif pOneScore == pTwoScore:
    finalWinner = "no one because the game ended in a draw"  # Draw
else:
    finalWinner = pTwo  # p2 wins

# Printing overall winner
print(f"Final winner is {finalWinner}!")

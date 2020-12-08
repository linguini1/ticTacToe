# Tic Tac Toe v2.0 (ticTacToe.py)

## How to play
There are two modes to this game: PvP and PvC. You can choose between these modes at the beginning of the game.

If you select PvP, you and the other player will share the keyboard to make moves. If you select PvC, there are three
game modes to choose from: easy, medium and hard. Player One will always use *X* and Player Two or The Computer will always
use *O*.

All the squares on the board are accessed by number coordinates. The first row being 1, second being 2 and third being 3. 
The columns are indexed in the same way, from 1-3. Rows are indexed from top to bottom, columns indexed from left to right.
You must input your move in the format [row][column]. There will be an example displayed at the begging of the game.

The rounds function as a competition of "best of", where one player only has to win the majority of the rounds to take the
ultimate victory. The default mode uses a best of 3 game format, but you can also set the number of rounds you want to play at 
the game's start. You can only choose an odd number of rounds in order to comply with the "best of" format.

## Display
After each round, the program will announce the winner and provide a short loading animation for the user to study the board.
This is because there's no strikethrough animation when a player wins, so the winning line may not be as clear, especially
when the computer is victorious because its plays are instant.

After the pause, a score update is displayed before starting the next round. After all the rounds are completed, a final
tally is shown, and the "ultimate winner" announced.

## How it works

<h4>Easy Mode</h4>
The computer randomly selects a spot on the board and fills it.

<h4>Medium Mode</h4>
The computer will look at the player's last move, and place an O in the same row or column as the last X. It randomly 
selects whether to place an O in the column or the row. 

If it's not possible to do either, the algorithm will recursively call the easy difficulty mode to make a move.

<h4>Hard Mode</h4>
The computer will take the center space on its first move, and if the center is already occupied, it takes a corner space.

Following the first move, the algorithm has a priority list of moves. First it checks for two Xs in a row, column, or diagonal
and then places an O in the remaining space to prevent a win. If there are two Os in a row, column, or diagonal, it will
place another O in the remaining space to take a win.

If none of the above scenarios are true, the computer will check to see if two lines with an X in them intersect at an
empty corner, and then fills the corner with an O. This prevents a move where the player places their Xs in an L-shape,
and then occupies the opposite corner (see example below). There are two scenarios which will cause this step to be
skipped.

<!-- language: lang-none -->
    |   |   | X |  <-- Final move (anticipated by computer)             | The L shape can be seen by tracing |
    -------------                                                       | down from the first move, and then |
    |   |   | X |  <-- First move                                       | moving left from the corner until  |
    -------------                                                       | the second move.                   |
    | X |   |   |
      ^
      |
      Second move (computer should block here before the final move)

However, if the last player move was in a corner spot, the algorithm will skip the above step and move on to the next 
step below, placing an O next to its previous move, forcing X to block and thus avoiding the triple corner trap which
looks like this:

<!-- language: lang-none -->
    |   |   | X |  <-- First move
    -------------
    | A | O |   |
    -------------
    | X |   | X |  <-- Final move (computer should anticipate this and place an O in space A)
      ^
      |
    Second move

If there are two Os in the center column or center row, the computer will also skip the above step and move on to the
next step below, which will set up a win scenario.

<!-- language: lang-none -->
    |   | O |   |  Two Os in the center column              |   |   |   |  Two Os in the center row
    -------------                                           -------------
    |   | O |   |                                           | O | O |   |
    -------------                                           -------------
    |   |   |   |                                           |   |   |   |

The next step, which is skipped to if the above two scenarios are true, or is selected in order of priority, checks if
there's a space in the same row or column of the computer's last move. If there is, it places an O. This sets up a win
scenario where a win can be gleaned from either a diagonal placement or a straight placement (either horizontal or
vertical). Here are the same two layouts but with Xs filled in, and the final move shown.

<!-- language: lang-none -->
    | A | O |   |  <-- An O would be placed here            | A | X | B |  X could block A or B, but
    -------------                                           -------------  O would still win by being
    | X | O | X |  X could block A or B, but                | O | O | X |  placed in the remaining space.
    -------------  O would still win by being               -------------
    | B | X |   |  placed in the remaining space.           |   | X |   |
                                                              ^
                                                              |
                                                              O would be placed here
If none of the above scenarios are in play, the algorithm will recursively call the medium difficulty mode to make a
decision.

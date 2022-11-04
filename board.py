############################################################################################################
# NAME: BINAIRO Creator
# AUTHOR: Christophe Van den Eynde
# FUNCTION: creates a random solvable Binairo-type puzzle
# USAGE python binairo_creator.py
############################################################################################################

# PACKAGES =================================================================================================
import random
# ==========================================================================================================

# FUNCTIONS ================================================================================================
# Print Board ----------------------------------------------------------------------------------------------
def PrintBoard(BoardState):
    row_count = 0
    for row in range(len(BoardState)):
        line = []
        char_count = 0
        # Print board middle separator (horizontal)
        if row_count == len(BoardState) / 2:
            print("{0}|{0}".format("-" * int(len(BoardState) + 1)))
        # loop through row & print values
        for char in BoardState[row]:
            #Add extra space in front of each line
            if char_count == 0:
                print(' ', end="")
            # Print board middle separator (vertical)
            if char_count == len(BoardState) / 2:
                print("| ", end="")
            # Print values
            print("{} ".format(char), end="")
            char_count += 1
        # Print end of line
        print()
        row_count += 1
    # Add empty line after each printed board
    print()

# Transpose board to get columns ---------------------------------------------------------------------------
def TransposeBoard(BoardState):
    columns = []
    for column_nr in range(len(BoardState)):
        line = ''
        for row in BoardState:
            line += row[column_nr]
        columns.append(line)
    return columns

# Find empty -----------------------------------------------------------------------------------------------
def CountEmpty(BoardState):
    empty = 0
    for line in range(len(BoardState)):
        for char in BoardState[line]:
            if char == ".":
                empty += 1
    return empty

# Find certain values --------------------------------------------------------------------------------------
def Certain(BoardState):
    for line in range(len(BoardState)):
        for i in range(0, 2):
            if i == 0:
                if ".00" in BoardState[line]:
                    return (1, (line, BoardState[line].index(".00")))
                elif "0.0" in BoardState[line]:
                    return (1, (line, BoardState[line].index("0.0") + 1))
                elif "00." in BoardState[line]:
                    return (1, (line, BoardState[line].index("00.") + 2))
                elif (BoardState[line].count(str(i)) == len(BoardState) / 2) and "." in BoardState[line]:
                    return (1, (line, BoardState[line].index(".")))
            elif i == 1:
                if ".11" in BoardState[line]:
                    return (0, (line, BoardState[line].index(".11")))
                elif "1.1" in BoardState[line]:
                    return (0, (line, BoardState[line].index("1.1") + 1))
                elif "11." in BoardState[line]:
                    return (0, (line, BoardState[line].index("11.") + 2))
                elif BoardState[line].count(str(i)) == len(BoardState) / 2 and "." in BoardState[line]:
                    return (0, (line, BoardState[line].index(".")))

# Update board ---------------------------------------------------------------------------------------------
def UpdateBoard(BoardState, update):
    # Define variables
    line = []
    new_line = ""
    # create a list of all characters in the line that needs updating
    for char in BoardState[update[1][0]]:
        line.append(char)
    # Update line with the found value at the correct position
    line[update[1][1]] = update[0]
    # convert line back to string
    for char in line:
        new_line += str(char)
    return new_line

# Update board with certain values
def UpdateCertain(BoardState):
        # Counter for ammount of certain values -------------------------------------------------------------------
    count_certain = 0

    # Find certain values & update board with them ------------------------------------------------------------
    while CountEmpty(BoardState) != 0:
        # Rows
        row_value = Certain(BoardState)
        if row_value:
            count_certain +=1
            BoardState[row_value[1][0]] = UpdateBoard(BoardState, row_value)
        # Columns
        col_value = Certain(TransposeBoard(BoardState))   
        if col_value:
            count_certain +=1
            col_value = (col_value[0], (col_value[1][1], col_value[1][0]))
            BoardState[col_value[1][0]] = UpdateBoard(BoardState, col_value) 
        # End loop if no cetain values where found
        if not row_value and not col_value:
            return BoardState, count_certain
    return BoardState, count_certain

# Check for duplicate rows/ columns ------------------------------------------------------------------------
def Identical(BoardState):
    for i in range(len(BoardState)):
        for row in BoardState:
            if BoardState[i] == row and BoardState.index(row) != i and not '.' in row:
                return False
    return True

# Brute force ----------------------------------------------------------------------------------------------
def BruteForce(BoardState):
    # Look for empty spots ---------------------------------------------------------------------------------
    if CountEmpty(BoardState) == 0:
        return BoardState
    else:
        for row in range(len(BoardState)):
            if "." in BoardState[row]:
                empty = (row, BoardState[row].index("."))
                original_row = BoardState[row]
                break
    # Try solution -----------------------------------------------------------------------------------------
    for value in random.choice([[0, 1], [1, 0]]):
        # Create new rows to test if the suggested value is valid
        new_row = UpdateBoard(BoardState, (value, empty))
        new_col = UpdateBoard(TransposeBoard(BoardState), (value, (empty[1], empty[0])))
        # Test if suggested value is valid
        if not "000" in new_row and not "111" in new_row and not "000" in new_col and not "111" in new_col:
            if not new_row.count(str(value)) > len(BoardState) / 2 and not new_col.count(str(value)) > len(BoardState) / 2:
                # Create test board to test for identical rows/ columns
                test_board = BoardState
                test_board[empty[0]] = new_row
                # Test for identical rows/ columns
                if Identical(test_board) and Identical(TransposeBoard(test_board)):
                    BoardState[empty[0]] = new_row
                    # try a value in the next empty position if a valid value was inserted, return true if value is possible
                    if BruteForce(BoardState):
                        return True
                    # reset value if next empty has no valid number
                    BoardState[row] = original_row
    # required for recursive, says that next empty has no valid number
    return False

# Calculate the current percentage of empty values in the board --------------------------------------------
def Percentage(BoardState):
    Percentage = int(CountEmpty(BoardState) / (len(BoardState) * len(BoardState)) * 100)
    return Percentage
# ==========================================================================================================

# INPUT ====================================================================================================
# Board size -----------------------------------------------------------------------------------------------
board_size = input("Size of the board (needs to be an even number): ")
while not board_size.isdigit() or int(board_size) % 2 != 0:
    if board_size.isdigit():
        if int(board_size) % 2 != 0:
            print("[ERROR] board size must be an even number")
    else:
        print("[ERROR] Non-numeric characters found. Board size must be an even number")
    board_size = input("Size of the board (needs to be an even number): ")
board_size = int(board_size)
# ===========================================================================================================

# CREATE RANDOM SOLVED BOARD ================================================================================
# Create empty placeholder board ----------------------------------------------------------------------------
RandomBoard = []
for row in range(board_size):
    RandomBoard.append("{}".format('.'*board_size))

# Message ---------------------------------------------------------------------------------------------------
print("\nCreating a random board. Please wait, this might take a while depending on the size of the board.\n")

# Create random solved board --------------------------------------------------------------------------------
BruteForce(RandomBoard)
# ===========================================================================================================

# REMOVE VALUES FROM BOARD ==================================================================================
# Create list of coordinates in board -----------------------------------------------------------------------
coords = []
for row in range(len(RandomBoard)):
    for char in range(len(RandomBoard[row])):
        coords.append((row, char))

# Create duplicate boards for testing -----------------------------------------------------------------------
EmptiedBoard = []
for i in RandomBoard:
    EmptiedBoard.append(i)

# Loop through coordinates and see if removal of value at coord still gives same solution of board ----------
while len(coords) != 0:
    # Choose a random position out of coordinates & index of said position in the list of coordinates
    position = random.choice(coords)
    index = coords.index(position)

    # Create duplicate of the emptied board (used for solving and comparing solution to original solution)
    TestBoard = []
    for i in EmptiedBoard:
        TestBoard.append(i)

    # Update testboard with empty value
    TestBoard[position[0]] = UpdateBoard(TestBoard, (".", position))

    # Test if solution of board is still the same (stop board from having multiple solutions)
    TestBoard, count = UpdateCertain(TestBoard)
    
    if TestBoard == RandomBoard:
        EmptiedBoard[position[0]] = UpdateBoard(EmptiedBoard, (".", position))

    # Remove tested position out of coordinates list
    del coords[index]
    
# Return final board ----------------------------------------------------------------------------------------
PrintBoard(EmptiedBoard)
# ===========================================================================================================

# SHOW SOLUTION =============================================================================================
if input("Show solution? (y/n): ").lower() == "y":
    print()
    PrintBoard(RandomBoard)
# ===========================================================================================================
import copy
import itertools

poss_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]


# The starting function for the program, gets user input
def start():
    preset = input("Would you like to use a preset board [Y/N]? ")
    if preset == "Y" or preset == "y":
        board = [
            [9, "x", "x", "x", "x", 1, "x", "x", 4],
            ["x", 2, "x", "x", "x", 8, "x", "x", "x"],
            ["x", "x", "x", 2, "x", "x", 7, "x", 5],
            [1, "x", 3, "x", "x", 6, 9, "x", "x"],
            ["x", 5, "x", "x", 2, "x", "x", 3, "x"],
            ["x", "x", "x", "x", "x", "x", "x", "x", "x"],
            [6, "x", 1, "x", "x", "x", 4, "x", 9],
            [2, "x", "x", 4, "x", "x", 8, "x", "x"],
            ["x", "x", 5, "x", 7, "x", "x", "x", "x"]
,
        ]
        """board = [
                ["x", 9, "x", 6, "x", "x", "x", "x", 2],
                ["x", "x", 6, "x", "x", 2, "x", "x", 3],
                [5, "x", 8, "x", "x", "x", "x", "x", "x"],
                [4, "x", "x", "x", "x", "x", "x", "x", "x"],
                ["x", "x", 1, "x", 7, "x", "x", "x", "x"],
                ["x", 6, "x", 3, "x", "x", "x", 8, "x"],
                ["x", "x", "x", 8, 9, "x", 6, "x", "x"],
                ["x", "x", 2, 1, "x", 5, "x", "x", "x"],
                ["x", "x", "x", "x", 3, "x", 5, "x", 4]
                ]"""
    elif preset == "N" or preset == "n":
        print()
        # TODO - Write board input
    else:
        print("Invalid input! Try again...")
        start()
    return board


# Prints board b in a clean way
def print_board(b):
    print("\n-----------------------------------------")
    for ind, row in enumerate(b):
        for col, num in enumerate(row):
            if col % 3 == 0:
                print("|| ", end="")
            else:
                print("| ", end="")
            print(str(num), end=" ")
        print("||", end="")
        if (ind + 1) % 3 == 0:
            print("\n-----------------------------------------")
        else:
            print()


# Removes possibilities from the row, column, and sub-square of the input value
def remove_possibilities(board_poss, row, col, value):
    # Remove the number as a possibility from the row
    for col_ind in range(len(board_poss[row])):
        if isinstance(board_poss[row][col_ind], list) and value in board_poss[row][col_ind]:
            # Make sure the empty cell doesn't just have one possibility in it and we don't remove the only possibility
            if len(board_poss[row][col_ind]) > 1:
                board_poss[row][col_ind].remove(value)

    # Remove the number as a possibility from the column
    col_nums = [r[col] for r in board_poss]
    for row_ind in range(len(col_nums)):
        if isinstance(board_poss[row_ind][col], list) and value in board_poss[row_ind][col]:
            if len(board_poss[row_ind][col]) > 1:
                board_poss[row_ind][col].remove(value)

    # Remove the number as a possibility from the sub-square
    for row_ind in range(row // 3 * 3, row // 3 * 3 + 3):
        for col_ind in range(col // 3 * 3, col // 3 * 3 + 3):
            if isinstance(board_poss[row_ind][col_ind], list) and value in board_poss[row_ind][col_ind]:
                # Make sure the empty cell doesn't just have one possibility in it and we don't remove the only possibility
                if len(board_poss[row_ind][col_ind]) > 1:
                    board_poss[row_ind][col_ind].remove(value)

    return board_poss


# Performs intersection on 3 lists, recursively also applying iit to sublists
def recursive_intersection(l1, l2, l3):
    intersection = []

    for row in range(9):
        r = []
        for col in range(9):
            if isinstance(l1[row][col], list):
                r.append(list(set(l1[row][col]) & set(l2[row][col]) & set(l3[row][col])))
            else:
                r.append(l1[row][col])
        intersection.append(r)
    return intersection


# Simplifies empty cells in which only one value is possible to that value
def simplify_board(board_to_simplify):
    for row, row_nums in enumerate(board_to_simplify):
        for col, cell in enumerate(row_nums):
            if isinstance(cell, list) and len(cell) == 1:
                board_to_simplify[row][col] = cell[0]
                print(f"SOLVER: Simplified cell at row {row + 1} column {col + 1} to {cell[0]} as it was the only possible value for that cell")

    return board_to_simplify


# Counts the number of instances of a number possibility in a subsection (row, column, or subsquare). Returns 0 if the number is already in the subsection
def count_subsection(ss, num, is_1d):
    count = 0
    if is_1d:
        for cell in ss:
            if isinstance(cell, list):
                if num in cell:
                    count += 1
    else:
        for row in ss:
            for cell in row:
                if isinstance(cell, list):
                    if num in cell:
                        count += 1
    return count


# Checks board for naked singles. Takes a board and a board of possibilities as input and returns an updated board and board of possibilities
def naked_singles(board, board_poss):
    print("SOLVER: Searching board for naked singles...")
    for r_num, row in enumerate(board_poss):
        for c_num, cell in enumerate(row):
            if isinstance(cell, list):
                if len(cell) == 1:
                    num = cell[0]
                    board[r_num][c_num] = num
                    board_poss[r_num][c_num] = num
                    board_poss = remove_possibilities(board_poss, r_num, c_num, num)
                    print(f"SOLVER: Naked single {str(num)} found in row {str(r_num + 1)} column {str(c_num + 1)} of board")

    return board, board_poss


# Performs the hidden singles strategy on rows, columns, and sub-squares. Takes a board and a board of possibilities as input and returns an updated board and board of possibilities
def hidden_singles(board, board_poss):

    # Get the columns of board_poss
    board_poss_columns = [[row[i] for row in board_poss] for i in range(len(board_poss[0]))]

    print("\nSOLVER: Checking all rows for any hidden singles...\n")

    for row_num, row in enumerate(board_poss):
        # print("ROW " + str(row_num + 1) + ": " + str(row))
        for poss_num in poss_nums:
            if count_subsection(row, poss_num, True) == 1:
                # print(str(poss_num) + " - ROW (" + str(count_subsection(row, poss_num)) + ") - " + str(row))
                col = -1
                for c_num, s in enumerate(row):
                    if isinstance(s, list) and poss_num in s:
                        col = c_num
                if col != -1:
                    board[row_num][col] = poss_num

                # Update possibilities
                board_poss[row_num][col] = poss_num
                board_poss = remove_possibilities(board_poss, row_num, col, poss_num)
                board_poss_columns[col][row_num] = poss_num
                board_poss_columns = remove_possibilities(board_poss_columns, col, row_num, poss_num)

                print(
                    f"\nSOLVER: Filled in row {row_num + 1} column {col + 1} of board with {poss_num} as it was only possible in that cell of the row")

    print("\nSOLVER: Checking all columns for any hidden singles...\n")

    for col_num, col in enumerate(board_poss_columns):
        # print("COL " + str(col_num + 1) + ": " + str(col))
        for poss_num in poss_nums:
            if count_subsection(col, poss_num, True) == 1:
                row = -1
                for r_num, s in enumerate(col):
                    if isinstance(s, list) and poss_num in s:
                        row = r_num
                board[row][col_num] = poss_num

                # Update possibilities
                board_poss[row][col_num] = poss_num
                board_poss = remove_possibilities(board_poss, row, col_num, poss_num)
                board_poss_columns[col_num][row] = poss_num
                board_poss_columns = remove_possibilities(board_poss_columns, col_num, row, poss_num)

                print(
                    f"\nSOLVER: Filled in row {row + 1} column {col_num + 1} of board with {poss_num} as it was only possible in that cell of the column")
                break

    print("\nSOLVER: Checking all sub-squares for any hidden singles...\n")

    poss_sub_squares = []

    # Create sub squares of board_poss and place them in poss_sub_squares
    for square in range(0, 9):
        sub_square = [[], [], []]
        start_row = (square // 3) * 3
        start_col = (square % 3) * 3

        for r in range(0, 3):
            for c in range(0, 3):
                sub_square[r].append(board_poss[start_row + r][start_col + c])
        poss_sub_squares.append(sub_square)

    # print(str(poss_sub_squares))

    #print("SS1:\n\n"+str(poss_sub_squares[0]))

    # Iterate through possible sub squares and search for hidden singles
    for ss_num, ss in enumerate(poss_sub_squares):
        for poss_num in poss_nums:
            if count_subsection(ss, poss_num, False) == 1:
                for r_num, row in enumerate(ss):
                    for c_num, col in enumerate(row):
                        if isinstance(col, list) and poss_num in col:
                            board_row = (ss_num // 3) * 3 + r_num
                            board_col = (ss_num % 3) * 3 + c_num
                            print(
                                f"\nSOLVER: Filled in row {board_row + 1} column {board_col + 1} of board with {poss_num} as it was only possible in that cell of the sub-square")
                            board[board_row][board_col] = poss_num
                            board_poss[board_row][board_col] = poss_num
                            board_poss = remove_possibilities(board_poss, board_row, board_col, poss_num)
                            break

    return board, board_poss


# Checks for naked and hidden singles and continues checking for them while they can still be found
def check_singles(board, board_poss):
    print("SOLVER: Checking for naked singles and hidden singles...")
    pre_board = copy.deepcopy(board)
    post_board, post_board_poss = naked_singles(board, board_poss)
    post_board, post_board_poss = hidden_singles(post_board, post_board_poss)
    # If the board has changed after searching for naked and hidden singles, search for them again
    while pre_board != post_board:
        pre_board = copy.deepcopy(post_board)
        pre_board_poss = copy.deepcopy(post_board_poss)
        print("SOLVER: Board changed from finding naked/hidden singles, checking naked singles and hidden singles again...")
        post_board, post_board_poss = naked_singles(pre_board, pre_board_poss)
        post_board, post_board_poss = hidden_singles(post_board, post_board_poss)
    return post_board, post_board_poss


# A function to find naked sets in rows, columns, and sub-squares, starting at size max_setsize and decrementing to size min_setsize. Returns an updated board_poss
def find_naked_sets(board_poss, min_setsize, max_setsize):
    # Define dictionary for matching numbers to names of sets of that size (for printing output)
    set_name = {2: "pair", 3: "triple", 4: "quad", 5: "quintet", 6: "sextet", 7: "septet", 8: "octet"}

    # Search for larger sets first
    for set_size in range(max_setsize, (min_setsize - 1), -1):
        # For rows
        print(f"\n\nSOLVER: Searching rows for naked {set_name[set_size]}s...")
        for r_num, row in enumerate(board_poss):
            candidates = []
            # Add possible candidates that can make up sets for row
            for cell in row:
                if isinstance(cell, list):
                    if len(cell) <= set_size:
                        for n in cell:
                            if n not in candidates:
                                candidates.append(n)

            # Create possible sets using the possible candidates in the row
            possible_sets = itertools.combinations(candidates, set_size)

            # Iterate through the possible sets
            for s in possible_sets:
                cols = []
                for col, cell in enumerate(row):
                    # If the cell isn't already solved
                    if isinstance(cell, list):
                        # If all the candidates in the cell are all in the set
                        if all(n in s for n in cell):
                            cols.append(col)

                # If there are as many cells with only the set candidates as the set size
                if len(cols) == set_size:
                    #set_cells = [ind for ind, cell in enumerate(row) if isinstance(cell, list) if all(n in s for n in cell)]
                    cols_to_remove = []
                    for col, cell in enumerate(row):
                        if isinstance(cell, list):
                            if any(n in cell for n in s) and col not in cols:
                                cols_to_remove.append(col)
                    if not cols_to_remove:
                        # If the cells that make up the naked set are the only ones that contain the set's candidates in the row
                        print(f"SOLVER: Naked {set_name[set_size]} {str(s)} found in columns {str({(c + 1) for c in cols})} of row {r_num + 1}, but since those are the only cells in the column with the {set_name[set_size]} candidates in the row, nothing was changed")
                        continue
                    else:
                        # Else, remove the candidates that are from the set in the row
                        print(f"SOLVER: Naked {set_name[set_size]} {str(s)} found in columns {str({(c + 1) for c in cols})} of row {r_num + 1}, removing those candidates from other cells in the row")

                    # Remove the candidates of the set from other cells in the row
                    for cell_col, cell in enumerate(board_poss[r_num]):
                        if cell_col not in cols and isinstance(cell, list):
                            for n in s:
                                if n in cell:
                                    board_poss[r_num][cell_col].remove(n)

        # For columns
        print(f"\nSOLVER: Searching columns for naked {set_name[set_size]}s...")
        candidates = []
        for c_num in range(9):
            board_col = [r[c_num] for r in board_poss]
            for cell in board_col:
                if isinstance(cell, list):
                    if len(cell) <= set_size:
                        for n in cell:
                            if n not in candidates:
                                candidates.append(n)

            # Create possible sets using the possible candidates in the column
            possible_sets = itertools.combinations(candidates, set_size)

            # Iterate through the possible sets
            for s in possible_sets:
                rows = []
                for row, cell in enumerate(board_col):
                    # If the cell isn't already solved
                    if isinstance(cell, list):
                        # If all the candidates in the cell are all in the set
                        if all(n in s for n in cell):
                            rows.append(row)
                # If there are as many cells with only the set candidates as the set size
                if len(rows) == set_size:
                    #set_cells = [ind for ind, cell in enumerate(board_col) if isinstance(cell, list) if all(n in s for n in cell)]
                    rows_to_remove = []
                    for row, cell in enumerate(board_col):
                        if isinstance(cell, list):
                            if any(n in cell for n in s) and row not in rows:
                                rows_to_remove.append(row)
                    if not rows_to_remove:
                        # If the cells that make up the naked set are the only ones that contain the set's candidates in the column
                        print(f"SOLVER: Naked {set_name[set_size]} {str(s)} found in rows {str({(r + 1) for r in rows})} of column {c_num + 1}, but since those are the only cells in the column with the set candidates in the column, nothing was changed")
                        continue
                    else:
                        # Else, remove the candidates that are from the set in the column
                        print(f"SOLVER: Naked {set_name[set_size]} {str(s)} found in rows {str({(r + 1) for r in rows})} of column {c_num + 1}, removing those candidates from other cells in the column")
                    # Remove the candidates of the set from other cells in the column
                    for cell_row in range(9):
                        if cell_row not in rows and isinstance(board_poss[cell_row][c_num], list):
                            for n in s:
                                if n in board_poss[cell_row][c_num]:
                                    board_poss[cell_row][c_num].remove(n)




        # For sub-squares
        print(f"\nSOLVER: Searching sub-squares for naked {set_name[set_size]}s...")
        # Iterate through each sub-square
        for ss_index in range(9):
            # Find the starting row and column indices of that sub-square
            start_row = ss_index // 3 * 3
            start_col = ss_index % 3 * 3
            # Use those indices to select the sub-square and place it in variable sub_square
            sub_square = [r[start_col:(start_col + 3)] for r in board_poss[start_row:(start_row + 3)]]
            # Iterate through the cells in the sub-square and append the candidates of cells with numbers of candidates at most the set size to candidates list
            candidates = []
            for row in sub_square:
                for cell in row:
                    if isinstance(cell, list):
                        if len(cell) <= set_size:
                            for n in cell:
                                if n not in candidates:
                                    candidates.append(n)

            # Create possible sets using the possible candidates in the column
            possible_sets = itertools.combinations(candidates, set_size)

            # Iterate through the possible sets
            for s in possible_sets:
                inds = []
                for row_num, row in enumerate(sub_square):
                    for col_num, cell in enumerate(row):
                        # If the cell isn't already solved
                        if isinstance(cell, list):
                            # If all the candidates in the cell are all in the set
                            if all(n in s for n in cell):
                                inds.append(((row_num + start_row), (col_num + start_col)))

                # If there are as many cells with only the set candidates as the set size
                if len(inds) == set_size:
                    #set_cells = [(r, c) for r, row_nums in enumerate(sub_square) for c, cell in enumerate(row_nums) if isinstance(cell, list) if all(n in s for n in cell)]
                    inds_to_remove = []
                    for row_num, row in enumerate(sub_square):
                        for col_num, cell in enumerate(row):
                            if isinstance(cell, list):
                                ind_to_remove = (row_num, col_num)
                                if any(n in cell for n in s) and ind_to_remove not in inds:
                                    inds_to_remove.append(ind_to_remove)

                    if not inds_to_remove:
                        # If the cells that make up the naked set are the only ones that contain the set's candidates in the sub-square
                        print(f"SOLVER: Naked {set_name[set_size]} {str(s)} found at", end="")
                        for i, ind in enumerate(inds):
                            if i == len(inds) - 2:
                                print(" row " + str(ind[0] + 1) + " column " + str(ind[1] + 1), end=", and")
                            elif i == len(inds) - 1:
                                print(" row " + str(ind[0] + 1) + " column " + str(ind[1] + 1) + " of sub-square " + str(ss_index + 1), end=", but since those are the only cells in the sub-square with the set candidates in the sub-square, nothing was changed")
                            else:
                                print(" row " + str(ind[0] + 1) + " column " + str(ind[1] + 1), end=",")
                        continue
                    else:
                        # Else, remove the candidates that are from the set in the column
                        print(f"SOLVER: Naked {set_name[set_size]} {str(s)} found at", end="")
                        for i, ind in enumerate(inds):
                            if i == len(inds) - 2:
                                print(" row " + str(ind[0] + 1) + " column " + str(ind[1] + 1), end=", and")
                            elif i == len(inds) - 1:
                                print(" row " + str(ind[0] + 1) + " column " + str(ind[1] + 1) + " of sub-square " + str(ss_index + 1), end=", removing those candidates from other cells in the sub-square")
                            else:
                                print(" row " + str(ind[0] + 1) + " column " + str(ind[1] + 1), end=",")
                        # Remove the candidates of the set from other cells in the sub-square
                        for cell_row in range(start_row, (start_row + 3)):
                            for cell_col in range(start_col, (start_col + 3)):
                                if (cell_row, cell_col) not in inds and isinstance(board_poss[cell_row][c_num], list):
                                    for n in s:
                                        if n in board_poss[cell_row][c_num]:
                                            board_poss[cell_row][c_num].remove(n)


    return board_poss


# Checks board_poss for pointing pairs and triplets. Takes board_poss as input and returns the updated board_poss
def pointing_pair_triplets(board_poss):
    poss_sub_squares = []

    # Create sub squares of board_poss and place them in poss_sub_squares
    for square in range(0, 9):
        sub_square = [[], [], []]
        start_row = (square // 3) * 3
        start_col = (square % 3) * 3

        for r in range(0, 3):
            for c in range(0, 3):
                sub_square[r].append(board_poss[start_row + r][start_col + c])
        poss_sub_squares.append(sub_square)

    # Iterate through every sub-square in board_poss
    for ss_num, ss in enumerate(poss_sub_squares):
        # For every possible number
        for poss_num in poss_nums:
            # If there are 2 of the number in the sub-square
            if count_subsection(ss, poss_num, False) == 2:

                # Get the indices of the 2 instances of the number in the sub-square
                pair_ind = []
                for r_num, r in enumerate(ss):
                    for c_num, c in enumerate(r):
                        if isinstance(c, list):
                            if poss_num in c:
                                pair_ind.append((r_num, c_num))

                # If the numbers are in a row, remove every other instance of the number possibility in the row
                if pair_ind[0][0] == pair_ind[1][0]:
                    print(f"\nSOLVER: Pointing pair found in row of sub-square {str(ss_num)}, removing possibility of number {str(poss_num)} from row {str(pair_ind[0][0] + 1)}")
                    for cell_ind, cell in enumerate(board_poss[pair_ind[0][0]]):
                        if isinstance(cell, list):
                            if poss_num in cell and cell_ind != pair_ind[0][1] and cell_ind != pair_ind[1][1]:
                                if len(board_poss[pair_ind[0][0]][cell_ind]) > 1:
                                    board_poss[pair_ind[0][0]][cell_ind].remove(poss_num)

                # If the numbers are in a column, remove every other instance of the number possibility in the column
                if pair_ind[0][1] == pair_ind[1][1]:
                    print(f"\nSOLVER: Pointing pair found in column of sub-square {str(ss_num)}, removing possibility of number {str(poss_num)} from column {str(pair_ind[0][1] + 1)}")
                    for cell_ind, cell in enumerate([r[pair_ind[0][1]] for r in board_poss]):
                        if isinstance(cell, list):
                            if poss_num in cell and cell_ind != pair_ind[0][0] and cell_ind != pair_ind[1][0]:
                                if len(board_poss[cell_ind][pair_ind[0][1]]) > 1:
                                    board_poss[cell_ind][pair_ind[0][1]].remove(poss_num)

            # If there are 3 of the number in the sub-square
            if count_subsection(ss, poss_num, False) == 3:
                # Get the indices of the 3 instances of the number in the sub-square
                triad_ind = []
                for r_num, r in enumerate(ss):
                    for c_num, c in enumerate(r):
                        if isinstance(c, list):
                            if poss_num in c:
                                triad_ind.append((r_num, c_num))

                # If the numbers are in a row, remove every other instance of the number possibility in the row
                if triad_ind[0][0] == triad_ind[1][0] == triad_ind[2][0]:
                    print(f"\nSOLVER: Pointing triplet found in row of sub-square {str(ss_num)}, removing possibility of number {str(poss_num)} from row {str(triad_ind[0][0] + 1)}")
                    for cell_ind, cell in enumerate(board_poss[triad_ind[0][0]]):
                        if isinstance(cell, list):
                            if poss_num in cell and cell_ind != triad_ind[0][1] and cell_ind != triad_ind[1][1] and cell_ind != triad_ind[2][1]:
                                board_poss[triad_ind[0][0]][cell_ind].remove(poss_num)

                # If the numbers are in a column, remove every other instance of the number possibility in the column
                if triad_ind[0][1] == triad_ind[1][1] == triad_ind[2][1]:
                    print(f"\nSOLVER: Pointing triplet found in column of sub-square {str(ss_num)}, removing possibility of number {str(poss_num)} from row {str(triad_ind[0][1] + 1)}")
                    for cell_ind, cell in enumerate([r[triad_ind[0][1]] for r in board_poss]):
                        if isinstance(cell, list):
                            if poss_num in cell and cell_ind != triad_ind[0][0] and cell_ind != triad_ind[1][0] and cell_ind != triad_ind[2][0]:
                                board_poss[cell_ind][triad_ind[0][1]].remove(poss_num)

    return board_poss


# Performs the box-line reduction strategy on board_poss. Takes board_poss as input and returns the updated board_poss
def box_line_reduction(board_poss):
    # Iterate through rows searching for potential box-line reduction rows
    print("SOLVER: Searching in rows for possible box-line reductions...")
    for row_num, row in enumerate(board_poss):
        # Iterate through every possible number
        for poss_num in poss_nums:
            num_count = sum([l.count(poss_num) if isinstance(l, list) else 1 if l == poss_num else 0 for l in row])
            # If there are 2 of the number in the row of the sub-square
            if num_count == 2:
                num_cols = [i for i, item in enumerate(row) if
                            (isinstance(item, list) and poss_num in item) or item == poss_num]
                ss_num = (row_num // 3) * 3 + num_cols[0] // 3
                # If the 2 numbers are in the same sub-square
                if (num_cols[0] // 3) == (num_cols[1] // 3):
                    for r in range(3):
                        for c in range(3):
                            board_row = (ss_num // 3) * 3 + r
                            board_col = (ss_num % 3) * 3 + c
                            if isinstance(board_poss[board_row][board_col], list) and poss_num in board_poss[board_row][
                                board_col] and board_col not in num_cols:
                                print(
                                    f"SOLVER: Since there were only 2 possibilities of {str(poss_num)} in row {str(row_num + 1)} of sub-square {str(ss_num + 1)}, as per box-line reduction strategy, eliminated possibility of {str(poss_num)} from rest of sub-square {str(ss_num + 1)}")
                                board_poss[board_row][board_col].remove(poss_num)

            # If there are only 3 of the number in the row of the sub-square
            if num_count == 3:
                num_cols = [i for i, item in enumerate(row) if
                            (isinstance(item, list) and poss_num in item) or item == poss_num]
                ss_num = (row_num // 3) * 3 + num_cols[0] // 3
                # If the 3 numbers are in the same row and in the same sub-square
                if ((num_cols[0] // 3) == (num_cols[1] // 3)) and ((num_cols[1] // 3) == (num_cols[2] // 3)):
                    for r in range(3):
                        for c in range(3):
                            board_row = (ss_num // 3) * 3 + r
                            board_col = (ss_num % 3) * 3 + c
                            if isinstance(board_poss[board_row][board_col], list) and poss_num in board_poss[board_row][
                                board_col] and board_col not in num_cols:
                                print(
                                    f"SOLVER: Since there were only 3 possibilities of {str(poss_num)} in row {str(row_num + 1)} of sub-square {str(ss_num + 1)}, as per box-line reduction strategy, eliminated possibility of {str(poss_num)} from rest of sub-square {str(ss_num + 1)}")
                                board_poss[board_row][board_col].remove(poss_num)

    # Get the columns of board_poss
    board_poss_columns = [[row[i] for row in board_poss] for i in range(len(board_poss[0]))]

    # Iterate through columns searching for potential box-line reduction rows
    print("SOLVER: Searching in columns for possible box-line reductions...")
    for col_num, col in enumerate(board_poss_columns):
        # Iterate through every possible number
        for poss_num in poss_nums:
            num_count = sum([l.count(poss_num) if isinstance(l, list) else 1 if l == poss_num else 0 for l in col])
            # If there is 2 of the number in the column
            if num_count == 2:
                num_rows = [i for i, item in enumerate(col) if
                            (isinstance(item, list) and poss_num in item) or item == poss_num]
                ss_num = (num_rows[0] // 3) * 3 + col_num // 3
                # If the 2 numbers are in the same row and in the same sub-square
                if num_rows[1] - num_rows[0] <= 2 and ((num_rows[0] // 3) == (num_rows[1] // 3)):
                    for r in range(3):
                        for c in range(3):
                            board_row = (ss_num // 3) * 3 + r
                            board_col = (ss_num % 3) * 3 + c
                            if isinstance(board_poss[board_row][board_col], list) and poss_num in board_poss[board_row][
                                board_col] and board_row not in num_rows:
                                print(
                                    f"SOLVER: Since there were only 2 possibilities of {str(poss_num)} in column {str(col_num + 1)} of sub-square {str(ss_num + 1)}, as per box-line reduction strategy, eliminated possibility of {str(poss_num)} from rest of sub-square {str(ss_num + 1)}")
                                board_poss[board_row][board_col].remove(poss_num)

        # If there are only 3 of the number in the column of the sub-square
        if num_count == 3:
            num_rows = [i for i, item in enumerate(col) if
                        (isinstance(item, list) and poss_num in item) or item == poss_num]
            ss_num = (num_rows[0] // 3) * 3 + col_num // 3
            # If the 3 numbers are in the same row and in the same sub-square
            if num_rows[2] - num_rows[0] <= 2 and ((num_rows[0] // 3) == (num_rows[1] // 3)) and (
                    (num_rows[1] // 3) == (num_rows[2] // 3)):
                for r in range(3):
                    for c in range(3):
                        board_row = (ss_num // 3) * 3 + r
                        board_col = (ss_num % 3) * 3 + c
                        if isinstance(board_poss[board_row][board_col], list) and poss_num in board_poss[board_row][
                            board_col] and board_row not in num_rows:
                            print(
                                f"SOLVER: Since there were only 3 possibilities of {str(poss_num)} in column {str(col_num + 1)} of sub-square {str(ss_num + 1)}, as per box-line reduction strategy, eliminated possibility of {str(poss_num)} from rest of sub-square {str(ss_num + 1)}")
                            board_poss[board_row][board_col].remove(poss_num)

    return board_poss


# A function to find hidden sets in rows, columns, and sub-squares, starting at size min_setsize and incrementing to size max_setsize. Returns an updated board_poss
def find_hidden_sets(board_poss, min_setsize, max_setsize):
    # Define dictionary for matching numbers to names of sets of that size (for printing output)
    set_name = {2: "pair", 3: "triple", 4: "quad", 5: "quintet", 6: "sextet", 7: "septet", 8: "octet"}

    # Search for smaller hidden sets first
    for set_size in range(min_setsize, (max_setsize + 1)):

        # For rows
        print(f"\n\nSOLVER: Searching rows for hidden {set_name[set_size]}s...")
        candidates = []

        # Find possible candidates that can make up sets in row
        for r_num, row in enumerate(board_poss):
            for cell in row:
                if isinstance(cell, list):
                    for n in cell:
                        if n not in candidates:
                            candidates.append(n)

            # Create possible sets based on candidates
            possible_sets = itertools.combinations(candidates, set_size)

            # Iterate through possible sets
            for s in possible_sets:
                occ = {}
                # Add the indices where number n occurs in a row to list inds
                for n in s:
                    inds = []
                    for c_num, cell in enumerate(row):
                        if isinstance(cell, list):
                            if n in cell:
                                inds.append((r_num, c_num))
                    # Map those indices to n in dictionary occ
                    occ[n] = inds

                """# Take the union of occ's values
                inds_union = set()
                for value in occ.values():
                    for num in value:
                        inds_union.add(num)

                set_inds = list(inds_union)"""

                set_inds = list(set.intersection(*[set(inds) for inds in list(occ.values())]))

                # If the number of indices is the set size
                if len(set_inds) == set_size and all([count_subsection(row, num, True) == set_size for num in s]):
                    print(f"SOLVER: Hidden {set_name[set_size]} {str(s)} found in columns {str(list((i[1] + 1) for i in set_inds))} of row {str(r_num + 1)}, removing all numbers from the cell that aren't part of the {set_name[set_size]}\n\rinds: {str(set_inds)}")
                    # Remove every number from the cells except for numbers in the set
                    for ind in set_inds:
                        for num in board_poss[ind[0]][ind[1]]:
                            if num not in s:
                                board_poss[ind[0]][ind[1]].remove(num)


        # For columns
        print(f"\n\nSOLVER: Searching columns for hidden {set_name[set_size]}s...")

        for c_num in range(9):
            board_col = [r[c_num] for r in board_poss]
            candidates = []

            # Find possible candidates that can make up sets in column
            for cell in board_col:
                if isinstance(cell, list):
                    for n in cell:
                        if n not in candidates:
                            candidates.append(n)

            # Create possible sets based on candidates
            possible_sets = itertools.combinations(candidates, set_size)

            # Iterate through possible sets
            for s in possible_sets:
                occ = {}
                # Add the indices where number n occurs in a row to list inds
                for n in s:
                    inds = []
                    for r_num, cell in enumerate(board_col):
                        if isinstance(cell, list):
                            if all(n in cell for n in s):
                                inds.append((r_num, c_num))
                occ[n] = inds

                """"# Take the union of occ's values
                inds_union = set()
                for value in occ.values():
                    for num in value:
                        inds_union.add(num)

                set_inds = list(inds_union)"""

                set_inds = list(set.intersection(*[set(inds) for inds in list(occ.values())]))

                # If the number of indices is the set size
                if len(set_inds) == set_size and all([count_subsection(board_col, num, True) == set_size for num in s]):
                    print(f"SOLVER: Hidden {set_name[set_size]} {str(s)} found in rows {str(list((t[0] + 1) for t in set_inds))} of column {str(c_num + 1)}, removing all numbers from the cell that aren't part of the {set_name[set_size]}")
                    # Remove every number from the cells except for numbers in the set
                    for ind in set_inds:
                        for num in board_poss[ind[0]][ind[1]]:
                            if num not in s:
                                board_poss[ind[0]][ind[1]].remove(num)



        # For sub-squares
        print(f"\n\nSOLVER: Searching for hidden {set_name[set_size]} in sub-squares...")
        for ss_index in range(9):
            # Create sub-square
            start_row = ss_index // 3 * 3
            start_col = ss_index % 3 * 3
            sub_square = [r[start_col:(start_col + 3)] for r in board_poss[start_row:(start_row + 3)]]

            # Find possible candidates that can make up sets in sub-square
            candidates = []
            for row in sub_square:
                for cell in row:
                    if isinstance(cell, list):
                        for n in cell:
                            if n not in candidates:
                                candidates.append(n)

            # Create possible sets based on candidates
            possible_sets = itertools.combinations(candidates, set_size)

            # Iterate through possible sets
            for s in possible_sets:
                occ = {}
                inds = []
                for r_num, row in enumerate(sub_square):
                    for c_num, cell in enumerate(row):
                        if isinstance(cell, list):
                            if all(n in cell for n in s):
                                inds.append(((r_num + start_row), (c_num + start_col)))
                occ[n] = inds

                """# Take the union of occ's values
                inds_union = set()
                for value in occ.values():
                    for num in value:
                        inds_union.add(num)

                set_inds = list(inds_union)"""

                set_inds = list(set.intersection(*[set(inds) for inds in list(occ.values())]))

                # If the number of indices is the set size
                if len(set_inds) == set_size and all([count_subsection(sub_square, num, False) == set_size for num in s]):
                    print(f"SOLVER: Hidden {set_name[set_size]} {str(s)} found at indices {str([(r + 1, c + 1) for r, c in set_inds])} in the sub-square {str(ss_index + 1)}, removing all numbers from the cells that aren't part of the {set_name[set_size]}")
                    # Remove every number from the cells except for numbers in the set
                    for ind in set_inds:
                        for num in board_poss[ind[0]][ind[1]]:
                            if num not in s:
                                board_poss[ind[0]][ind[1]].remove(num)


    return board_poss


# Solves the sudoku board using a series of rules
def solve_board(board):
    # Inserting board sub squares into 1D list
    sub_squares = []
    for square in range(0, 9):
        sub_square = [[], [], []]
        start_row = (square // 3) * 3
        start_col = (square % 3) * 3

        for r in range(0, 3):
            for c in range(0, 3):
                sub_square[r].append(board[start_row + r][start_col + c])
        sub_squares.append(sub_square)

    cols = []
    for c in range(9):
        cols.append([x[c] for x in board])

    # Build board of possible numbers

    # Based on rows
    board_poss_rows = copy.deepcopy(board)
    for row, rownums in enumerate(board):
        for col, num in enumerate(rownums):
            if num == "x":
                x_poss = [i for i in poss_nums if i not in rownums]
                board_poss_rows[row][col] = x_poss

    # Based on columns
    board_poss_cols = copy.deepcopy(board)
    for col, colnums in enumerate(cols):
        for row, num in enumerate(colnums):
            if num == "x":
                x_poss = [i for i in poss_nums if i not in colnums]
                board_poss_cols[row][col] = x_poss

    # Based on sub-squares
    board_poss_ss = copy.deepcopy(board)
    for square, ss in enumerate(sub_squares):
        start_row = (square // 3) * 3
        start_col = (square % 3) * 3
        for r in range(3):
            for c in range(3):
                row = start_row + r
                col = start_col + c
                num = ss[r][c]
                if num == "x":
                    x_poss = [i for i in poss_nums if all(i not in r for r in ss)]
                    board_poss_ss[row][col] = x_poss

    # Create board of possibilities for each cell
    board_poss = recursive_intersection(board_poss_rows, board_poss_cols, board_poss_ss)

    print("CURRENT BOARD OF POSSIBILITIES:")
    print_board(board_poss)

    # Rule 1 and 2 - check for naked singles then hidden singles until none can be found anymore

    board, board_poss = check_singles(board, board_poss)

    if board_solved(board):
        print("SOLVER: Board is solved!")
        return board
    else:
        print("SOLVER: Board is not solved, continuing...")
        print("Current board:\n")
        print_board(board)

    print("CURRENT BOARD OF POSSIBILITIES:")
    print_board(board_poss)

    # Rule 3 - naked pairs/triplets

    #board_poss = naked_pairs(board_poss)
    board_poss = find_naked_sets(board_poss, 2, 3)

    print("CURRENT BOARD OF POSSIBILITIES:")
    print_board(board_poss)

    # Check for naked singles and hidden singles

    board, board_poss = check_singles(board, board_poss)

    print("CURRENT BOARD OF POSSIBILITIES:")
    print_board(board_poss)

    # After each rule is applied, check if the board is solved
    print("SOLVER: Checking if board is solved...\n")

    if board_solved(board):
        print("SOLVER: Board is solved!")
        return board
    else:
        print("SOLVER: Board is not solved, continuing...")
        print("\nCurrent board:\n")
        print_board(board)

    # Rule 4 - hidden pairs/triplets

    board_poss = find_hidden_sets(board_poss, 2, 3)

    # Check for naked singles and hidden singles

    board, board_poss = check_singles(board, board_poss)

    print("CURRENT BOARD OF POSSIBILITIES:")
    print_board(board_poss)

    # After each rule is applied, check if the board is solved
    print("SOLVER: Checking if board is solved...\n")

    if board_solved(board):
        print("SOLVER: Board is solved!")
        return board
    else:
        print("SOLVER: Board is not solved, continuing...")
        print("\nCurrent board:\n")
        print_board(board)

    # Rule 5 - pointing pairs/triplets

    board_poss = pointing_pair_triplets(board_poss)

    # Check for naked and hidden singles again

    board, board_poss = check_singles(board, board_poss)

    # After each rule is applied, check if the board is solved
    print("SOLVER: Checking if board is solved...\n")

    if board_solved(board):
        print("SOLVER: Board is solved!")
        return board
    else:
        print("SOLVER: Board is not solved, continuing...")
        print("\nCurrent board:\n")
        print_board(board)

    # Rule 6 - box-line reduction

    board_poss = box_line_reduction(board_poss)

    # Check for naked and hidden singles again

    board, board_poss = check_singles(board, board_poss)

    # After each rule is applied, check if the board is solved
    print("SOLVER: Checking if board is solved...\n")

    if board_solved(board):
        print("SOLVER: Board is solved!")
        return board
    else:
        print("SOLVER: Board is not solved, continuing...")
        print("\nCurrent board:\n")
        print_board(board)

    # Rule 7 - x-wing

    # Rule 8 - swordfish

    # Rule 9 - forced chains

    # Do rules 1 to 9 again before resorting to brute force

    # Rule 10 - backtracking brute force

    return board


# Checks if theoretical_board is a valid Sudoku board
def check_valid(board):
    print()
    # TODO: Write function that checks if every row, column, and sub-square in theoretical_board is legal and returns True or False - USED FOR BACKTRACKING


# Checks if the input board is solved
def board_solved(board):
    for row in board:
        for col in row:
            if "x" == col:
                return False
    return True


# Driver code
if __name__ == "__main__":
    sudoku_board = []
    while sudoku_board == []:
        sudoku_board = start()
    print("\nBoard before solving:")
    print_board(sudoku_board)

    print("\nSolving details:")
    solved_board = solve_board(sudoku_board)

    print("\nBoard after solving:")
    print_board(solved_board)

    #print("\nBoard possibilities:")
    #board = board_poss
    #print_board()
import copy

poss_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# The starting function for the program, gets user input
def start():
    preset = input("Would you like to use a preset board [Y/N]? ")
    if preset == "Y" or preset == "y":
        # board = [["x", 7, "x", "x", 9, 2, "x", 1, "x"], [4, "x", "x", 8, "x", 5, "x", 6, 3],
        #         [5, "x", 1, "x", "x", "x", "x", "x", 8], [8, 3, "x", 9, 4, "x", "x", "x", 7],
        #         ["x", 9, "x", "x", "x", 3, 2, "x", "x"], [7, "x", 5, 1, 2, "x", 3, "x", "x"],
        #         [9, "x", "x", 3, "x", "x", 6, 7, 2], [2, "x", 7, 4, "x", 9, "x", "x", "x"],
        #         [6, "x", "x", "x", "x", 7, 5, 4, "x"]]
        #board = [[3, 7, 8, "x", 9, 2, "x", 1, "x"], [4, 2, 9, 8, "x", 5, "x", 6, 3],
        #         [5, "x", 1, "x", "x", "x", "x", "x", 8], [8, 3, "x", 9, 4, "x", "x", "x", 7],
        #         ["x", 9, "x", "x", "x", 3, 2, "x", "x"], [7, "x", 5, 1, 2, "x", 3, "x", "x"],
        #         [9, "x", "x", 3, "x", "x", 6, 7, 2], [2, "x", 7, 4, "x", 9, "x", "x", "x"],
        #         [6, "x", "x", "x", "x", 7, 5, 4, "x"]]
        #board = [["x","x","x","x","x","x","x","x", 2], ["x","x","x","x", 9, 5, 4, "x", "x"],
        #         ["x", "x", 6, 8, "x", "x", "x", "x", "x"], ["x", 8, 5, "x", 2, "x", 9, 4, 1],
        #         ["x", "x", "x", 1, "x", 9, 7, 3, 8], [1, "x", "x", "x", "x", "x", 2, 5, 6],
        #         [8, 9, 3, "x", 1, "x", "x", "x", "x"], ["x", "x", "x", 9, "x", "x", "x", "x", 4],
        #         ["x", "x", 7, 6, "x", "x", 3, "x", "x"]]
        #board = [["x","x","x","x","x","x",5,"x","x"],
        #         [1, 6, "x", 9, "x", "x", "x", "x", "x"],
        #         ["x", "x", 9, "x", 6, 4, "x", "x", "x"],
        #         ["x", "x", "x", "x", "x", "x", "x", "x", 4],
        #         [4, "x", "x", "x", 2, "x", 1, "x", "x"],
        #         ["x", "x", "x", 3, "x", "x", "x", 5, "x"],
        #         ["x", "x", 2, "x", 8, 9, "x", "x", "x"],
        #         ["x", "x", "x", 2, 5, "x", "x", 3, "x"],
        #         [7, "x", "x", 1, "x", "x", "x", "x", 9]]
        board = [[2,5,1,3,4,8,7,9,6],
             ["x","x","x",9,1,7,2,"x","x"],
             ["x","x",7,2,5,6,"x","x","x"],
             ["x","x","x","x",6,"x",8,3,2],
             ["x","x","x","x","x","x","x",7,"x"],
             ["x","x",8,"x","x","x",9,"x","x"],
             ["x","x","x",6,2,"x","x","x",8],
             [8,"x","x",7,"x","x","x","x","x"],
             ["x","x",2,5,"x",1,6,4,"x"]]
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

# Returns the sub-square at index ss_num
def get_sub_square(board_poss, ss_num):
    row_ind = ss_num // 3 * 3
    col_ind = ss_num % 3 * 3

    ss = [l[col_ind:(col_ind + 3)] for l in board_poss[row_ind:(row_ind + 3)]]
    return ss

# Removes possibilities from the row, column, and sub-square of the input value
def remove_possibilities(board_poss, row, col, value):
    # Build the sub-squares of board_poss
    poss_sub_squares = []
    for poss_square in range(0, 9):
        poss_sub_square = [[], [], []]
        s_row = (poss_square // 3) * 3
        s_col = (poss_square % 3) * 3

        for r in range(0, 3):
            for c in range(0, 3):
                poss_sub_square[r].append(board_poss[s_row + r][s_col + c])
        poss_sub_squares.append(poss_sub_square)

    # Remove the number as a possibility from the row
    for col_ind in range(len(board_poss[row])):
        if isinstance(board_poss[row][col_ind], list) and value in board_poss[row][col_ind]:
            try:
                board_poss[row][col_ind].remove(value)
            except ValueError:
                pass

    # Remove the number as a possibility from the column
    col_nums = [r[col] for r in board_poss]
    for row_ind in range(len(col_nums)):
        if isinstance(board_poss[row_ind][col], list) and value in board_poss[row_ind][col]:
            try:
                board_poss[row_ind][col].remove(value)
            except ValueError:
                pass

    # Remove the number as a possibility from the sub-square
    for row_ind in range(row // 3 * 3, row // 3 * 3 + 3):
        for col_ind in range(col // 3 * 3, col // 3 * 3 + 3):
            if isinstance(board_poss[row_ind][col_ind], list) and value in board_poss[row_ind][col_ind]:
                try:
                    board_poss[row_ind][col_ind].remove(value)
                except ValueError:
                    pass

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


# Merges 2 boards, also merging sublists in the board
def merge_boards(b1, b2):
    new_board = []

    for row_ind in range(9):
        row = []
        for tile_ind in range(9):
            tile1, tile2 = b1[row_ind][tile_ind], b2[row_ind][tile_ind]

            # If both tiles are lists
            if isinstance(tile1, list) and isinstance(tile2, list):
                merged_tile = list(set(tile1 + tile2))

            # If only the first tile is a list
            elif isinstance(tile1, list):
                merged_tile = tile1

            # If only the second tile is a list
            elif isinstance(tile2, list):
                merged_tile = tile2

            # If neither tile is a list
            else:
                merged_tile = tile1 if tile1 == tile2 else [tile1, tile2]

            row.append(merged_tile)

        new_board.append(row)

    return new_board


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
    # Check rows
    print("SOLVER: Checking rows for any naked singles...\n")
    for row_num, row in enumerate(board):
        if row.count("x") == 1:
            x_col = row.index("x")  # Get missing number's column
            num = [i for i in [1, 2, 3, 4, 5, 6, 7, 8, 9] if i not in row]  # Get missing number's value
            if len(num) == 1:
                print(
                    f"SOLVER: Filled in row {row_num + 1} column {x_col + 1} with {num[0]} as {num[0]} was the only number left in row {row_num + 1}")
                board[row_num][x_col] = num[0]

                # Set x_col column of row_num row board to num[0] and remove it as a possibility from the row, column, and sub-square
                board_poss[row_num][x_col] = num[0]
                board_poss = remove_possibilities(board_poss, row_num, x_col, num[0])


    # Check columns
    print("SOLVER: Checking columns for any naked singles...\n")

    for col_num in range(0, 9):
        col = [i[col_num] for i in board]
        if col.count("x") == 1:
            x_row = col.index("x")  # Get missing number's row
            num = [i for i in [1, 2, 3, 4, 5, 6, 7, 8, 9] if i not in col]  # Get missing number's value
            if len(num) == 1:
                print(
                    f"SOLVER: Filled in row {x_row + 1} column {col_num + 1} with {num[0]} as {num[0]} was the only number left in column {col_num + 1}")
                # Fill number in board
                board[x_row][col_num] = num[0]

                # Set col_num column of x_row row board_poss to num[0] and remove it as a possibility from the row, column, and sub-square
                board_poss[x_row][col_num] = num[0]
                board_poss = remove_possibilities(board_poss, x_row, col_num, num[0])

    # Check sub-squares
    for ss in range(9):
        # Create sub-squares
        sub_square = [[], [], []]
        for r in range(3):
            for c in range(3):
                sub_square[r].append(board[(ss // 3) * 3 + r][(ss % 3) * 3 + c])

        # If there's only 1 unfilled square in the sub-square, replace that square with the remaining number
        if any(["x" in r for r in sub_square]) and all([s.count("x") <= 1 for s in sub_square]):
            num = [i for i in [1, 2, 3, 4, 5, 6, 7, 8, 9] if all(i not in r for r in sub_square)]
            num_ind = next((i, j) for i, lst in enumerate(sub_square) for j, x in enumerate(lst) if x == "x")
            if len(num) == 1:
                solved_row = (ss // 3) * 3 + num_ind[0]
                solved_col = (ss % 3) * 3 + num_ind[1]
                print(
                    f"SOLVER: Filled in row {solved_row + 1} column {solved_col + 1} with {num[0]} as {num[0]} was the only number left in sub-square {ss + 1}")

                # Set x_col column of row_num row board to num[0] and remove it as a possibility from the row, column, and sub-square
                board_poss[solved_row][solved_col] = num[0]
                board_poss = remove_possibilities(board_poss, solved_row, solved_col, num[0])

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


# Performs the naked pairs strategy on rows and columns of the board. Takes a board of possibilities as input and returns the updated board of possibilities
def naked_pairs(board_poss):
    # Check for naked pairs in rows
    print("\n\nSOLVER: Searching for naked pairs in rows...")

    # Iterate through rows
    for row_ind, row_nums in enumerate(board_poss):

        # Search for two 2 number lists in a row
        for i in range(len(row_nums)):
            if isinstance(row_nums[i], list) and len(row_nums[i]) == 2 and row_nums.count(row_nums[i]) == 2:
                pair = row_nums[i]
                for num in pair:
                    for j in range(len(row_nums)):
                        if isinstance(row_nums[j], list) and row_nums[j] != pair:
                            try:
                                row_nums[j].remove(num)
                            except ValueError:
                                pass
                            else:
                                print(
                                    f"SOLVER: As per the naked pairs strategy, reduced possibilities in row {row_ind + 1} by numbers {pair[0]} and {pair[1]} as there were already 2 cells with those 2 exact possibilities in the row")

    # Check for naked pairs in columns
    print("SOLVER: Searching for naked pairs in columns...")

    # Get the columns of board_poss
    board_poss_columns = [[row[i] for row in board_poss] for i in range(len(board_poss[0]))]

    for col_ind, col_nums in enumerate(board_poss_columns):
        # Search for two 2 number lists in a column
        for i in range(len(col_nums)):
            if isinstance(col_nums[i], list) and len(col_nums[i]) == 2 and col_nums.count(col_nums[i]) == 2:
                pair = col_nums[i]
                for num in pair:
                    for j in range(len(col_nums)):
                        if isinstance(col_nums[j], list) and col_nums[j] != pair:
                            try:
                                col_nums[j].remove(num)
                            except ValueError:
                                pass
                            else:
                                print(
                                    f"SOLVER: As per the naked pairs strategy, reduced possibilities in column {col_ind + 1} by numbers {pair[0]} and {pair[1]} as there were already 2 cells with those 2 exact possibilities in the column")

    # Check for naked pairs in sub-squares
    print("SOLVER: Searching for naked pairs in sub-squares...")

    # Iterate through sub-squares
    board_poss_subsquares = []
    for square in range(0, 9):
        sub_square = [[], [], []]
        start_row = (square // 3) * 3
        start_col = (square % 3) * 3

        for r in range(0, 3):
            for c in range(0, 3):
                sub_square[r].append(board_poss[start_row + r][start_col + c])
        board_poss_subsquares.append(sub_square)

    for col_ind, col_nums in enumerate(board_poss_columns):

        # Search for two 2 number lists in a column
        for i in range(len(col_nums)):
            if isinstance(col_nums[i], list) and len(col_nums[i]) == 2 and col_nums.count(col_nums[i]) == 2:
                pair = col_nums[i]
                for num in pair:
                    for j in range(len(col_nums)):
                        if isinstance(col_nums[j], list) and col_nums[j] != pair:
                            try:
                                col_nums[j].remove(num)
                            except ValueError:
                                pass
                            else:
                                print(f"SOLVER: As per the naked pairs strategy, reduced possibilities in column {col_ind + 1} by numbers {pair[0]} and {pair[1]} as there were already 2 cells with those 2 exact possibilities in the column")

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

                # print("\n\n-----------" + str(pair_ind) + "----------------\n\n")
                # print(str(ss)+"\n\n")
                # print(str(poss_num)+"\n\n")

                # If the numbers are in a row, remove every other instance of the number possibility in the row
                if pair_ind[0][0] == pair_ind[1][0]:
                    print(
                        f"SOLVER: Pointing pair found in row of sub-square {str(ss_num)}, removing possibility of number {str(poss_num)} from row {str(pair_ind[0][0] + 1)}")
                    for cell_ind, cell in enumerate(board_poss[pair_ind[0][0]]):
                        if isinstance(cell, list):
                            if poss_num in cell and cell_ind != pair_ind[0][1] and cell_ind != pair_ind[1][1]:
                                board_poss[pair_ind[0][0]][cell_ind].remove(poss_num)

                # If the numbers are in a column, remove every other instance of the number possibility in the column
                if pair_ind[0][1] == pair_ind[1][1]:
                    print(
                        f"SOLVER: Pointing pair found in column of sub-square {str(ss_num)}, removing possibility of number {str(poss_num)} from column {str(pair_ind[0][1] + 1)}")
                    for cell_ind, cell in enumerate([r[pair_ind[0][1]] for r in board_poss]):
                        if isinstance(cell, list):
                            if poss_num in cell and cell_ind != pair_ind[0][0] and cell_ind != pair_ind[1][0]:
                                board_poss[cell_ind][pair_ind[0][1]].remove(poss_num)

            # If there are 3 of the number in the sub-square
            if count_subsection(ss, poss_num, False) == 3:
                #yprint("SS:\n\n" + str(ss) + "\n\n" + "poss_num:\n\n" + str(poss_num) + "\n\n")
                # Get the indices of the 3 instances of the number in the sub-square
                triad_ind = []
                for r_num, r in enumerate(ss):
                    for c_num, c in enumerate(r):
                        if isinstance(c, list):
                            if poss_num in c:
                                triad_ind.append((r_num, c_num))

                # If the numbers are in a row, remove every other instance of the number possibility in the row
                if triad_ind[0][0] == triad_ind[1][0] == triad_ind[2][0]:
                    print(f"SOLVER: Pointing triplet found in row of sub-square {str(ss_num)}, removing possibility of number {str(poss_num)} from row {str(triad_ind[0][0] + 1)}")
                    for cell_ind, cell in enumerate(board_poss[triad_ind[0][0]]):
                        if isinstance(cell, list):
                            if poss_num in cell and cell_ind != triad_ind[0][1] and cell_ind != triad_ind[1][1] and cell_ind != triad_ind[2][1]:
                                board_poss[triad_ind[0][0]][cell_ind].remove(poss_num)

                # If the numbers are in a column, remove every other instance of the number possibility in the column
                if triad_ind[0][1] == triad_ind[1][1] == triad_ind[2][1]:
                    print(
                        f"SOLVER: Pointing triplet found in column of sub-square {str(ss_num)}, removing possibility of number {str(poss_num)} from row {str(triad_ind[0][1] + 1)}")
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


# Solves the sudoku board using a series of rules
def solve_board(board):
    poss_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    # Inserting board sub squares into list
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
    #print(str(board_poss))

    #print("Board poss------------:\n")#+str(board_poss)+"\n\n"+str(board)) # For debugging
    #print_board(board_poss)

    #print("\n\nBOARD POSS:\n\n")
    #print_board(board_poss)
    #print(str(board_poss))
    #print("\n\n-------------------------------------------------------------------------------------------------")

    # Rule 1 - naked singles

    board, board_poss = naked_singles(board, board_poss)

    # After each rule is applied, check if the board is solved
    print("\nSOLVER: Checking if board is solved...")

    if board_solved(board):
        print("SOLVER: Board is solved!")
        return board
    else:
        print("SOLVER: Board is not solved, continuing...")
        print("Current board:\n")
        print_board(board)

    # Rule 2 - hidden singles

    board, board_poss = hidden_singles(board, board_poss)

    # After each rule is applied, check if the board is solved
    print("SOLVER: Checking if board is solved...\n")

    if board_solved(board):
        print("SOLVER: Board is solved!")
        return board
    else:
        print("SOLVER: Board is not solved, continuing...")
        print("\nCurrent board:\n")
        print_board(board)

    #print("\n\nBOARD_POSS:\n\n")
    #print_board(board_poss)

    # Rule 3 - naked pairs

    board_poss = naked_pairs(board_poss)

    # Attempt to simplify board
    print("SOLVER: Simplifying board as much as possible...")
    board_poss = simplify_board(board_poss)

    # Check if there are any lists in board_poss
    has_lists = False
    for r in board_poss:
        for c in r:
            if isinstance(c, list):
                has_lists = True
                break
        if has_lists:
            break

    if not has_lists:
        board = board_poss

    print("SOLVER: Checking for naked singles and hidden singles again...")

    # Check for naked singles again

    board, board_poss = naked_singles(board, board_poss)

    # Check for hidden singles again

    board, board_poss = hidden_singles(board, board_poss)

    # After each rule is applied, check if the board is solved
    print("SOLVER: Checking if board is solved...\n")

    if board_solved(board):
        print("SOLVER: Board is solved!")
        return board
    else:
        print("SOLVER: Board is not solved, continuing...")
        print("\nCurrent board:\n")
        print_board(board)

    # Rule 4 - pointing pairs/triplets

    board_poss = pointing_pair_triplets(board_poss)

    # Attempt to simplify board
    print("SOLVER: Simplifying board as much as possible...")
    board_poss = simplify_board(board_poss)

    # Check if there are any lists in board_poss
    has_lists = False
    for r in board_poss:
        for c in r:
            if isinstance(c, list):
                has_lists = True
                break
        if has_lists:
            break

    if not has_lists:
        board = board_poss

    print("SOLVER: Checking for naked singles and hidden singles again...")

    # Check for naked singles again

    board, board_poss = naked_singles(board, board_poss)

    # Check for hidden singles again

    board, board_poss = hidden_singles(board, board_poss)

    # After each rule is applied, check if the board is solved
    print("SOLVER: Checking if board is solved...\n")

    if board_solved(board):
        print("SOLVER: Board is solved!")
        return board
    else:
        print("SOLVER: Board is not solved, continuing...")
        print("\nCurrent board:\n")
        print_board(board)

    # Rule 5 - box-line reduction

    board_poss = box_line_reduction(board_poss)

    # Attempt to simplify board
    print("SOLVER: Simplifying board as much as possible...")
    board_poss = simplify_board(board_poss)

    # Check if there are any lists in board_poss
    has_lists = False
    for r in board_poss:
        for c in r:
            if isinstance(c, list):
                has_lists = True
                break
        if has_lists:
            break

    if not has_lists:
        board = board_poss

    print("SOLVER: Checking for naked singles and hidden singles again...")

    # Check for naked singles again

    board, board_poss = naked_singles(board, board_poss)

    # Check for hidden singles again

    board, board_poss = hidden_singles(board, board_poss)

    # After each rule is applied, check if the board is solved
    print("SOLVER: Checking if board is solved...\n")

    if board_solved(board):
        print("SOLVER: Board is solved!")
        return board
    else:
        print("SOLVER: Board is not solved, continuing...")
        print("\nCurrent board:\n")
        print_board(board)

    # Rule 5 - naked triplets

    # Rule 6 - hidden pairs/triplets

    # Rule 7 - x-wing

    # Rule 8 - swordfish

    # Rule 9 - forced chains

    # Rule 10 - backtracking

    # Simplify board_poss in case there are any cells with only one possibility

    board = simplify_board(board_poss)

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
assignments = []

# constant value
rows = 'ABCDEFGHI'
cols = '123456789'
ASCII_A = 65

def cross(A, B):
    return [s+t for s in A for t in B]


# all box, unit, peer reference variables.
boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

# this is for stroing all boxes belonging to the diagonal lines.
# it creates 2 lists, one for each diagonal line.
diag_units = [[chr(ASCII_A+i) + str(i+1) for i in range(0, 9)], [chr(ASCII_A+i) + str(9-i) for i in range(0, 9)]]

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def check_two_vals_equal(val1, val2):
    """
    comparing two values in two boxes
    each box could have the same values in different order
    """
    count = 0

    if len(val1) is not len(val2):
        return False

    for val in val1:
        if val in val2:
            count += 1

    if count == len(val1):
        return True
    else:
        return False

def naked_twins_square(values, target_box, target_peer):
    """removing duplicate values in a square unit
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
        target_box, target_peer: boxes having the same values
    """
    for square_unit in square_units:
        if target_box in square_unit and target_peer in square_unit:
            for box in square_unit:
                if check_two_vals_equal(values[box], values[target_box]) == False and (len(values[box]) > 1):
                    for value in values[target_box]:
                        assign_value(values, box, values[box].replace(value,''))
            return

def naked_twins_row_col(values, target_box, target_peer, units):
    """removing duplicate values in a square unit
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
        target_box, target_peer: boxes having the same values
        units: either column_unit or row_unit
    """
    for unit in units:
        if (target_peer in unit) and (target_box in unit):
            # perform naked twins technique for row units
            for box in unit:
                if check_two_vals_equal(values[box], values[target_box]) == False and (len(values[box]) > 1):
                    for value in values[target_box]:
                        assign_value(values, box, values[box].replace(value,''))

def naked_twins_diag(values):
    for diag_unit in diag_units:
        found = False
        box1_val = ''
        box2_val = ''

        # find two boxes having the same value
        for box1 in diag_unit:
            if len(values[box1]) == 2:
                for box2 in diag_unit:
                    if (box1 != box2) and check_two_vals_equal(values[box1], values[box2]):
                        found = True
                        box1_val = values[box1]
                        box2_val = values[box2]
                        break

        # if two boxes are found
        if found == True:
            # perform naked twins technique for diagonal units
            for box in diag_unit:
                if check_two_vals_equal(values[box], box1_val) == False and (len(values[box]) > 1):
                    for value in box1_val:
                        assign_value(values, box, values[box].replace(value,''))

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

    # for column and row units
    # going through all boxes
    for box in values:
        # going through all peers of the box
        for peer in peers[box]:
            # if one of the peer has the same value to the box
            if len(values[peer]) is 2 and check_two_vals_equal(values[box], values[peer]):
                # if the box and peer belongs to the same row_units list
                naked_twins_row_col(values, box, peer, row_units)

                # if the box and peer belongs to the same column_units list
                naked_twins_row_col(values, box, peer, column_units)

                # if the box and peer belongs to the same square unit
                naked_twins_square(values, box, peer)

    # for diagonal units
    # for each diagonal direction
    naked_twins_diag(values)

    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    grid_dict = {}

    for box_i in range(0, len(boxes)):
        if grid[box_i] == '.':
            grid_dict[boxes[box_i]] = '123456789'
        else:
            grid_dict[boxes[box_i]] = grid[box_i]

    return grid_dict

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            assign_value(values, peer, values[peer].replace(digit,''))

    # eliminate for diag units
    for units in diag_units:
        solved_values = [box for box in units if len(values[box]) == 1]
        for box in solved_values:
            digit = values[box]
            for unit in units:
                if unit != box and len(values[unit]) != 1:
                    assign_value(values, unit, values[unit].replace(digit,''))

    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)

    # only choice for diag units
    for unit in diag_units:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)

    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # the Eliminate Strategy
        values = eliminate(values)

        # the Naked Twins Strategy
        values = naked_twins(values)

        # the Only Choice Strategy
        values = only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)

    return values

if __name__ == '__main__':
    # diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')

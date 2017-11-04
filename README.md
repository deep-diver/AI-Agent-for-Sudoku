# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Contents
* About the Project
* Questions from Udacity
* Install Guide
* Dependencies
* Resources

# About the Project
This project is a part of AIND(Artificial Intelligence Nanodegree)'s assignment. This project is about building an agent to solve any 'Diagonal Sudoku' problem using 3 techniques, "eliminate", "only one choice", and "naked twins". The agent tries to solve problems by applying the techniques while performing Depth First Search.

# Questions from Udacity
## Question 1 (Naked Twins) - How do we use constraint propagation to solve the naked twins problem?
A: First of all, naked twins problem is applicable when there are 2-digit boxes available. Second, when I come across a 2-digit box while searching all boxes, then I look up its row/column peers. Third, I go through all row/column peers and search for a box having the same 2-digit value. Fourth, if the box is found, I go through row/column peers and remove the 2-digit value from row/column peers. If a peer contain only one digit of the 2-digit value, that one digit will also be deleted.

## Question 2 (Diagonal Sudoku) - How do we use constraint propagation to solve the diagonal sudoku problem?  
A: There are only 2 diagonal lines in Sudoku, so I made a list of box belonging to the lines. Just like for normal Sudoku, the same techniques can be applied to Diagonal Sudoku but with slightly modified version. For eliminate technique, I eliminated all duplicate values of possible digits from boxes belonging to the same diagonal line. Also, I checked if there are boxes with the same 2-digit value so that I could perform naked twins technique for each diagonal lines. Only one choice technique is also modified to support diagonal sudoku to find a box which has the only unique value comparing to other boxes on each diagonal lines.

# Dependencies
* This project requires **Python 3.x**.
* This project optionally requires **Pygame**[here](http://www.pygame.org/download.shtml) for visualization purpose.

# Resources
* `solution.py` - Complete Diagonal Sudoku problem solving logic.
* `test_solution.py` - You can test your solution by running `python -m unittest`.
* `PySudoku.py` - This is code for visualizing your solution.
* `visualize.py` - This is code for visualizing your solution.

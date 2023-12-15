import numpy as np
from main import flood_fill

# Test case 1: Flood fill within matrix boundaries
matrix = np.array([[-1, -1, -1],
                   [-1, -1, -1],
                   [-1, -1, -1]])
label = 1
row = 1
col = 1
width = 3
height = 3
expected_output = np.array([[1, 1, 1],
                           [1, 1, 1],
                           [1, 1, 1]])
flood_fill(matrix, label, row, col, width, height)
assert np.array_equal(matrix, expected_output)

# Test case 2: Flood fill outside matrix boundaries
matrix = np.array([[-1, -1, -1],
                   [-1, -1, -1],
                   [-1, -1, -1]])
label = 1
row = 0
col = 3
width = 3
height = 3
expected_output = np.array([[-1, -1, -1],
                           [-1, -1, -1],
                           [-1, -1, -1]])
flood_fill(matrix, label, row, col, width, height)
assert np.array_equal(matrix, expected_output)

# Test case 3: Flood fill with existing labels
matrix = np.array([[-1, -1, -1],
                   [-1,  1, -1],
                   [-1, -1, -1]])
label = 2
row = 1
col = 1
width = 3
height = 3
expected_output = np.array([[-1, -1, -1],
                           [-1,  1, -1],
                           [-1, -1, -1]])
flood_fill(matrix, label, row, col, width, height)
assert np.array_equal(matrix, expected_output)

print("All test cases passed!")
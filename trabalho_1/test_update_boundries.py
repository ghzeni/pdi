import numpy as np
from main import update_boundries

""" 
Test update boundries
"""
# Test case 1: Update top and left boundaries
blob = {'label': 1, 'n_pixels': 9, 'T': (1, 1), 'R': (2, 2), 'B': (2, 2), 'L': (1, 1)}
row = 0
col = 0
expected_output = {'label': 1, 'n_pixels': 9, 'T': (0, 0), 'R': (2, 2), 'B': (2, 2), 'L': (0, 0)}
assert update_boundries(blob, row, col) == expected_output

# Test case 2: Update bottom and right boundaries
blob = {'label': 1, 'n_pixels': 9, 'T': (0, 0), 'R': (2, 2), 'B': (2, 2), 'L': (0, 0)}
row = 3
col = 3
expected_output = {'label': 1, 'n_pixels': 9, 'T': (0, 0), 'R': (3, 3), 'B': (3, 3), 'L': (0, 0)}
assert update_boundries(blob, row, col) == expected_output

# Test case 3: No update to boundaries
blob = {'label': 1, 'n_pixels': 9, 'T': (0, 0), 'R': (2, 2), 'B': (2, 2), 'L': (0, 0)}
row = 1
col = 1
expected_output = {'label': 1, 'n_pixels': 9, 'T': (0, 0), 'R': (2, 2), 'B': (2, 2), 'L': (0, 0)}
assert update_boundries(blob, row, col) == expected_output

print("All test cases passed!")


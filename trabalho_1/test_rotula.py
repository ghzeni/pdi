from main import rotula
import numpy as np

"""
Test rotula
"""

# Test case 1: Empty binary image
binarizada = np.zeros((10, 10))
largura_min = 5
altura_min = 5
n_pixels_min = 10
expected_output = []
assert rotula(binarizada, largura_min, altura_min, n_pixels_min) == expected_output

# Test case 2: Binary image with a single blob
binarizada = np.array([[0, 0, 0, 0, 0],
                       [0, 1, 1, 1, 0],
                       [0, 1, 1, 1, 0],
                       [0, 1, 1, 1, 0],
                       [0, 0, 0, 0, 0]])
largura_min = 3
altura_min = 3
n_pixels_min = 5
expected_output = [{'label': 1, 'n_pixels': 9, 'T': (1, 1), 'R': (3, 3), 'B': (3, 3), 'L': (1, 1)}]
assert rotula(binarizada, largura_min, altura_min, n_pixels_min) == expected_output

# Test case 3: Binary image with multiple blobs
binarizada = np.array([[0, 0, 0, 0, 0],
                       [0, 1, 1, 1, 0],
                       [0, 1, 0, 1, 0],
                       [0, 1, 1, 1, 0],
                       [0, 0, 0, 0, 0]])
largura_min = 2
altura_min = 2
n_pixels_min = 4
expected_output = [{'label': 1, 'n_pixels': 8, 'T': (1, 1), 'R': (3, 3), 'B': (3, 3), 'L': (1, 1)}]
assert rotula(binarizada, largura_min, altura_min, n_pixels_min) == expected_output

print("All tests passed!")
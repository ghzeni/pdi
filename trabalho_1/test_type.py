import unittest
import cv2
import numpy as np
from main import count_rice

NEGATIVO = False
THRESHOLD = 0.81
ALTURA_MIN = 5
LARGURA_MIN = 5
N_PIXELS_MIN = 20

class TestCountRice(unittest.TestCase):
    def test_count_rice(self):
        input_image = 'arroz_input/arroz_5.png'
        invert_image = NEGATIVO
        threshold = THRESHOLD
        min_height = ALTURA_MIN
        min_width = LARGURA_MIN
        min_pixel_amount = N_PIXELS_MIN

        result = count_rice(input_image, invert_image, threshold, min_height, min_width, min_pixel_amount)

        self.assertIsInstance(result[0], int)
        self.assertIsInstance(result[1], float)

    def test_img_type(self):
        input_image = 'arroz_input/arroz_5.png'
        invert_image = NEGATIVO
        threshold = THRESHOLD
        min_height = ALTURA_MIN
        min_width = LARGURA_MIN
        min_pixel_amount = N_PIXELS_MIN

        img = cv2.imread(input_image)
        self.assertEqual(type(img), cv2.typing.MatLike)

        img = cv2.UMat(img)
        self.assertEqual(type(img), cv2.UMat)

if __name__ == '__main__':
    unittest.main()
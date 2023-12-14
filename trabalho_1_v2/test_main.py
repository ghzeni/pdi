import unittest
import cv2
from main import main

"""
def count_rice(input_image, invert_image, threshold, min_height, min_width, min_pixel_amount):
    global img, imgb
    img = cv2.imread (input_image, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

    img = img.reshape ((img.shape [0], img.shape [1], 1))
    img = img.astype (np.float32) / 255

    img_out = cv2.cvtColor (img, cv2.COLOR_GRAY2BGR)

    if invert_image:
        img = 1 - img
    imgb = binariza (img, threshold)
    cv2.imwrite ('01 - binarizada.png', imgb.astype(np.int8) * 255)
    imgshow = cv2.imread('01 - binarizada.png', 0)
    cv2.imshow ('01 - binarizada', imgshow)

    start_time = timeit.default_timer ()
    componentes = rotula (imgb, min_width, min_height, min_pixel_amount)
    n_componentes = len (componentes)
    
    return (n_componentes, timeit.default_timer () - start_time)
"""

# generate tests for count_rice() against arroz_5.png, arroz_8.png, arroz_11.png, arroz_16.bmp, arroz_42.png and arroz.bmp
# expected outputs are 5, 8, 11, 16, 42 and 0, respectively

NEGATIVO = False
THRESHOLD = 0.81
ALTURA_MIN = 5
LARGURA_MIN = 5
N_PIXELS_MIN = 20
  
import unittest
from main import count_rice
class TestCountRice(unittest.TestCase):
  def test_arroz_3(self):
    expected_output = 3
    result = count_rice('arroz_input/arroz_3.png', NEGATIVO, THRESHOLD, ALTURA_MIN, LARGURA_MIN, N_PIXELS_MIN)
    self.assertEqual(result[0], expected_output)

  def test_arroz_5(self):
    expected_output = 5
    result = count_rice('arroz_input/arroz_5.png', NEGATIVO, THRESHOLD, ALTURA_MIN, LARGURA_MIN, N_PIXELS_MIN)
    self.assertEqual(result[0], expected_output)

  def test_arroz_8(self):
    expected_output = 8
    result = count_rice('arroz_input/arroz_8.png', NEGATIVO, THRESHOLD, ALTURA_MIN, LARGURA_MIN, N_PIXELS_MIN)
    self.assertEqual(result[0], expected_output)

  def test_arroz_11(self):
    expected_output = 12
    result = count_rice('arroz_input/arroz_12.png', NEGATIVO, THRESHOLD, ALTURA_MIN, LARGURA_MIN, N_PIXELS_MIN)
    self.assertEqual(result[0], expected_output)

  def test_arroz_16(self):
    expected_output = 16
    result = count_rice('arroz_input/arroz_16.bmp', NEGATIVO, THRESHOLD, ALTURA_MIN, LARGURA_MIN, N_PIXELS_MIN)
    self.assertEqual(result[0], expected_output)

  def test_arroz_42(self):
    expected_output = 42
    result = count_rice('arroz_input/arroz_42.png', NEGATIVO, THRESHOLD, ALTURA_MIN, LARGURA_MIN, N_PIXELS_MIN)
    self.assertEqual(result[0], expected_output)

if __name__ == '__main__':
  unittest.main()

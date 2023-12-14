import sys
import timeit
import numpy as np
import cv2
import math as m
import json

INPUT_IMAGE =  'arroz_input/arroz.bmp'

img = cv2.imread (INPUT_IMAGE)
if img is None:
    print ('Erro abrindo a imagem.\n')
    sys.exit ()

print(type(img))
print(type((10, 10)[0]))
cv2.rectangle (img, (10, 10), (100, 100), (0, 0, 255), 2)
cv2.imshow ('test rectangle', img)
cv2.waitKey ()
cv2.destroyAllWindows ()

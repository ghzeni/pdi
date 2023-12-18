#===============================================================================
# Trabalho 5: Chroma Key
#-------------------------------------------------------------------------------
# Autor: Gustavo Henrique Zeni
# Universidade Tecnológica Federal do Paraná
#===============================================================================

import tkinter as tk
from tkinter import filedialog
import sys
import timeit
import numpy as np
import cv2
import math as m
import os

#===============================================================================

INPUT_IMAGE = 'img/7.bmp'
ENABLE_GUI = False
LEAVE_OPEN = True
OPEN_TIME = 1500

# TODO: tratar contornos usando gradientes
# TODO: implementar alpha blending com máscara de verdice

#===============================================================================

def main ():

  if ENABLE_GUI:
      root = tk.Tk()
      root.withdraw()
      file_path = filedialog.askopenfilename(initialdir="./trabalho_5/img", title="Select file", filetypes=(("bmp files", "*.bmp"), ("all files", "*.*")))
  else:
      file_path = INPUT_IMAGE
  
  img = cv2.imread (file_path)
  if img is None:
      print ('Erro abrindo a imagem 1.\n')
      sys.exit ()

  img_rgb = cv2.cvtColor (np.copy(img), cv2.COLOR_BGR2RGB)

  lower_green =  np.array([0, 100, 0])
  upper_green = np.array([100, 255, 100])

  mask = cv2.inRange (img_rgb, lower_green, upper_green)

  cv2.imwrite ('mask.png', mask)
  cv2.imshow ('mask', cv2.imread ('mask.png'))
  cv2.waitKey (0)
  cv2.destroyAllWindows ()

  masked_img = np.copy(img_rgb)
  masked_img[mask != 0] = [0, 0, 0]

  cv2.imwrite ('masked_img.png', masked_img)
  cv2.imshow ('masked_img', cv2.imread ('masked_img.png'))
  cv2.waitKey (0)
  cv2.destroyAllWindows ()

  bg = cv2.imread ('background/bg_test.jpg')
  if bg is None:
      print ('Erro abrindo a imagem de fundo.\n')
      sys.exit ()

  bg = cv2.cvtColor (np.copy(bg), cv2.COLOR_BGR2RGB)

  bg = bg[0:img_rgb.shape[0], 0:img_rgb.shape[1]]
  bg[mask == 0] = [0, 0, 0]

  cv2.imwrite ('bg.png', bg)
  cv2.imshow ('bg', cv2.imread ('bg.png'))
  cv2.waitKey (0)
  cv2.destroyAllWindows ()

  combined = masked_img + bg
  combined = cv2.cvtColor (np.copy(combined), cv2.COLOR_RGB2BGR)

  cv2.imwrite ('combined.png', combined)
  cv2.imshow ('combined', cv2.imread ('combined.png'))
  cv2.waitKey (0)
  cv2.destroyAllWindows ()

if __name__ == '__main__':
  main ()
    
#===============================================================================

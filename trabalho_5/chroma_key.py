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

#===============================================================================

# returns a mask of the greeness of the image, in a single channel, in a scale of 0 to 1
def greeness_mask (img):
  mask = np.zeros ((img.shape[0], img.shape[1]), dtype=np.float32)
  imgf = img.astype (np.float32)/255

  for i in range (img.shape[0]):
    for j in range (img.shape[1]):
      mask[i][j] = 1 + (imgf[i][j][0] + imgf[i][j][2])/2 - imgf[i][j][1]
      if mask[i][j] < 0:
        mask[i][j] = 0
      elif mask[i][j] > 1:
        mask[i][j] = 1

  mask = mask / np.max (mask)
  return mask

def alpha_blend(fg, bg, mask):
  blended = np.copy(bg)

  for i in range (bg.shape[0]):
    for j in range (bg.shape[1]):
        blended[i][j] = (mask[i][j] * fg[i][j]) + ((1 - mask[i][j]) * bg[i][j])

  # back to bgr
  blended = cv2.cvtColor (blended, cv2.COLOR_RGB2BGR)

  
  return blended

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

  mask = greeness_mask (img_rgb)
  
  bg = cv2.imread ('background/bg_test.jpg')
  if bg is None:
      print ('Erro abrindo a imagem de fundo.\n')
      sys.exit ()

  if img_rgb.shape[0] > bg.shape[0] or img_rgb.shape[1] > bg.shape[1]:
    bg = cv2.resize (bg, (img_rgb.shape[1], img_rgb.shape[0]))

  bg = cv2.cvtColor (np.copy(bg), cv2.COLOR_BGR2RGB)

  bg = bg[0:img_rgb.shape[0], 0:img_rgb.shape[1]]

  # alphablending equation for blended = img_rgb, bg and using mask
  blended = alpha_blend(img_rgb, bg, mask)
  
  cv2.imwrite ('blended.png', blended)
  cv2.imshow ('blended', cv2.imread ('blended.png'))
  cv2.waitKey (0)
  cv2.destroyAllWindows ()

if __name__ == '__main__':
  main ()
    
#===============================================================================

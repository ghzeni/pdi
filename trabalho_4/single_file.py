#===============================================================================
# Trabalho 4: Blur
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
import helpers as hp
import pdi as pdi

#===============================================================================
# ORDEM E PARAMETROS
ORDER_REMOVE_NOISE = 0
ORDER_THRESHOLD = 1
GAUSS_KSIZE = 7
THRESHOLD_TYPE = 'ADAPTIVE' # 'ADAPTIVE', 'OTSU' or 'SIMPLE'
ADAPT_BLOCK = 11
ADAPT_C = 3
SIMPLE_THRESH = 0.6


#===============================================================================

INPUT_IMAGE = 'img/60.bmp'
ENABLE_GUI = False
LEAVE_OPEN = True
OPEN_TIME = 1500

#===============================================================================

def show_progress (img, line):
  cv2.imshow ('main.py:' + line, img)
  cv2.waitKey ()
  cv2.destroyWindow ('main.py:' + line)

#-------------------------------------------------------------------------------

def gaussian_blur (img):
  img_out = cv2.blur(img, (GAUSS_KSIZE, GAUSS_KSIZE))
  return img_out

#-------------------------------------------------------------------------------

def all_thresholds (img):
  # from float to uint8
  img_thresh = (img * 255).astype (np.uint8)
  # grayscale
  img_thresh = cv2.cvtColor (img_thresh, cv2.COLOR_BGR2GRAY)
  if THRESHOLD_TYPE == 'ADAPTIVE':
    # threshold
    img_thresh = cv2.adaptiveThreshold(1 - img_thresh, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, ADAPT_BLOCK, ADAPT_C)
  elif THRESHOLD_TYPE == 'OTSU':
    # threshold
    _, img_thresh = cv2.threshold (img_thresh, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
  elif THRESHOLD_TYPE == 'SIMPLE':
    # threshold
    _, img_thresh = cv2.threshold (img_thresh, SIMPLE_THRESH, 255, cv2.THRESH_BINARY)

  # back to BGR
  img_thresh = cv2.cvtColor (img_thresh, cv2.COLOR_GRAY2BGR)
  # from uint8 to float
  img_thresh = img_thresh.astype (np.float32) / 255

  return img_thresh

#-------------------------------------------------------------------------------

def normalize (img):
  img_out = np.zeros (img.shape, dtype=np.float32)
  # normalize
  img_out = cv2.normalize (img, img_out, 0, 1, cv2.NORM_MINMAX)
  return img_out

#===============================================================================
## SOLUÇÃO DESVIO PADRÃO


def count_rice (img):
  desvio_padrao = 999
  blob_list = []


#   pra cada pixel da imagem
#   se é arroz
#     blob = flood_fill (i, j)
#     blob_list.add(blob)
#  # blob_list cheia
#  # calcula_media()
#  #  return int
#  # calcula_dp (blob_list, media)
#  #  for blob in blob_list
#  #    blob.dp = np.dp(tam, media)
#  #  return blob_list

#===============================================================================

def main ():

  if ENABLE_GUI:
      root = tk.Tk()
      root.withdraw()
      file_path = filedialog.askopenfilename(initialdir="./img/", title="Select file", filetypes=(("bmp files", "*.bmp"), ("all files", "*.*")))
  else:
      file_path = INPUT_IMAGE
  
  img = cv2.imread (file_path)
  if img is None:
      print ('Erro abrindo a imagem 1.\n')
      sys.exit ()

  img = img.astype (np.float32) / 255
  img_out = np.copy(img)

  img_step_one = normalize(img_out)
  img_step_two = gaussian_blur(img_step_one)
  img_step_three = all_thresholds(img_step_two)
  blob_list = pdi.label_blobs(img_step_three)

  column_one = np.concatenate((img, img_step_three), axis=0)
  
  cv2.namedWindow('original - blurred - thresholded', cv2.WINDOW_NORMAL)
  cv2.resizeWindow('original - blurred - thresholded', 1440, 900)
  
  cv2.imshow ('original - blurred - thresholded', column_one)
  cv2.waitKey () if LEAVE_OPEN else cv2.waitKey (OPEN_TIME)
  cv2.destroyAllWindows ()

if __name__ == '__main__':
  main ()
    
#===============================================================================

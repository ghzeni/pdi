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

#===============================================================================
# ORDEM E PARAMETROS
ORDER_REMOVE_NOISE = 0
ORDER_THRESHOLD = 1
GAUSS_KSIZE = 5
THRESHOLD_TYPE = 'ADAPTIVE' # 'ADAPTIVE', 'OTSU' or 'SIMPLE'
ADAPT_BLOCK = 11
ADAPT_C = 4
SIMPLE_THRESH = 0.8


#===============================================================================

INPUT_IMAGE_ONE = 'img/60.bmp'
INPUT_IMAGE_TWO = 'img/82.bmp'
INPUT_IMAGE_THREE = 'img/114.bmp'
INPUT_IMAGE_FOUR = 'img/205.bmp'
ENABLE_GUI = False
LEAVE_OPEN = False
OPEN_TIME = 3500

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

#-------------------------------------------------------------------------------

def all_thresholds (img):
  # from float to uint8
  img_thresh = (img * 255).astype (np.uint8)
  # grayscale
  img_thresh = cv2.cvtColor (img_thresh, cv2.COLOR_BGR2GRAY)
  if THRESHOLD_TYPE == 'ADAPTIVE':
    # threshold
    img_thresh = cv2.adaptiveThreshold(img_thresh, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, ADAPT_BLOCK, ADAPT_C)
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

#===============================================================================

def main ():

  if ENABLE_GUI:
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(initialdir="./img/", title="Select file", filetypes=(("bmp files", "*.bmp"), ("all files", "*.*")))

  img_one, img_two, img_three, img_four = hp.open_images(INPUT_IMAGE_ONE, INPUT_IMAGE_TWO, INPUT_IMAGE_THREE, INPUT_IMAGE_FOUR)
  img_one, img_two, img_three, img_four = hp.images_to_float(img_one, img_two, img_three, img_four)
  img_one_out, img_two_out, img_three_out, img_four_out = hp.create_copy(img_one, img_two, img_three, img_four)
  img_one_out, img_two_out, img_three_out, img_four_out = hp.remove_noise(img_one_out, img_two_out, img_three_out, img_four_out)
  img_one_out, img_two_out, img_three_out, img_four_out = hp.threshold(img_one_out, img_two_out, img_three_out, img_four_out)

  
  line_one = np.concatenate((img_one, img_one_out), axis=1)
  line_two = np.concatenate((img_two, img_two_out), axis=1)
  line_three = np.concatenate((img_three, img_three_out), axis=1)
  line_four = np.concatenate((img_four, img_four_out), axis=1)
  join_lines = np.concatenate((line_one, line_two, line_three, line_four), axis=0) #Vertical
  
  """
  join_inputs = np.concatenate((img_one, img_two, img_three, img_four), axis=1) #Horizontal
  join_outputs = np.concatenate((img_one_out, img_two_out, img_three_out, img_four_out), axis=1) #Horizontal
  join_both = np.concatenate((join_inputs, join_outputs), axis=0) #Vertical
  """

  cv2.namedWindow('original - blurred - thresholded', cv2.WINDOW_NORMAL)
  cv2.resizeWindow('original - blurred - thresholded', 1440, 900)
  
  cv2.imshow ('original - blurred - thresholded', join_lines)
  cv2.waitKey () if LEAVE_OPEN else cv2.waitKey (OPEN_TIME)
  cv2.destroyAllWindows ()

if __name__ == '__main__':
  main ()
    
#===============================================================================

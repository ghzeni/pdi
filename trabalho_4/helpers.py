import tkinter as tk
from tkinter import filedialog
import sys
import timeit
import numpy as np
import cv2
import math as m
import rice_counting as rc

#===============================================================================

def show_progress (img, line):
  cv2.imshow ('main.py:' + line, img)
  cv2.waitKey ()
  cv2.destroyWindow ('main.py:' + line)



#-------------------------------------------------------------------------------

def open_images (img_one_path, img_two_path, img_three_path, img_four_path):
  img_one = cv2.imread (img_one_path)
  img_two = cv2.imread (img_two_path)
  img_three = cv2.imread (img_three_path)
  img_four = cv2.imread (img_four_path)

  if img_one is None:
      print ('Erro abrindo a imagem 1.\n')
      sys.exit ()
  if img_two is None:
      print ('Erro abrindo a imagem 2.\n')
      sys.exit ()
  if img_three is None:
      print ('Erro abrindo a imagem 3.\n')
      sys.exit ()
  if img_four is None:
      print ('Erro abrindo a imagem 4.\n')
      sys.exit ()
  
  return img_one, img_two, img_three, img_four

#-------------------------------------------------------------------------------

def images_to_float (img_one, img_two, img_three, img_four):
  img_one = img_one.astype (np.float32) / 255
  img_two = img_two.astype (np.float32) / 255
  img_three = img_three.astype (np.float32) / 255
  img_four = img_four.astype (np.float32) / 255
  
  return img_one, img_two, img_three, img_four

#-------------------------------------------------------------------------------

def create_copy (img_one, img_two, img_three, img_four):
  img_one_out = np.copy(img_one)
  img_two_out = np.copy(img_two)
  img_three_out = np.copy(img_three) 
  img_four_out = np.copy(img_four)

  return img_one_out, img_two_out, img_three_out, img_four_out

#-------------------------------------------------------------------------------

def remove_noise (img_one, img_two, img_three, img_four):
    img_one_out = rc.gaussian_blur(img_one)
    img_two_out = rc.gaussian_blur(img_two) 
    img_three_out = rc.gaussian_blur(img_three)
    img_four_out = rc.gaussian_blur(img_four)

    return img_one_out, img_two_out, img_three_out, img_four_out

#-------------------------------------------------------------------------------

def threshold (img_one, img_two, img_three, img_four):
    img_one_out = rc.all_thresholds(img_one)
    img_two_out = rc.all_thresholds(img_two)
    img_three_out = rc.all_thresholds(img_three)
    img_four_out = rc.all_thresholds(img_four)

    return img_one_out, img_two_out, img_three_out, img_four_out
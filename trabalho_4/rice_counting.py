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
GAUSS_KSIZE = 11
THRESHOLD_TYPE = 'ADAPTIVE' # 'ADAPTIVE', 'OTSU' or 'SIMPLE'
ADAPT_BLOCK = 17 # best 17
ADAPT_C = 7 # best 7
SIMPLE_THRESH = 0.6
NOT_VISITED = 1.0
VISITED = 0.8
IS_RICE = 0.2
MEAN_THRESHOLD = 0.10
# not a rice, just DUST
MIN_RICE_SIZE = 10 # best 10

#===============================================================================

INPUT_IMAGE_ONE = 'img/60.bmp'
INPUT_IMAGE_TWO = 'img/82.bmp'
INPUT_IMAGE_THREE = 'img/114.bmp'
INPUT_IMAGE_FOUR = 'img/150.bmp'
INPUT_IMAGE_FIVE = 'img/205.bmp'
ENABLE_GUI = False
LEAVE_OPEN = True
OPEN_TIME = 3500

#===============================================================================

def show_progress (img, line):
  if img is None:
      print("Error: invalid image")
      return
  
  cv2.imshow('show progress', img)
  cv2.waitKey()
  cv2.destroyWindow('show progress')

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

def label_blobs(img):

  # grayscale
  img_gray = cv2.cvtColor (img, cv2.COLOR_BGR2GRAY)
  img_out = img_gray.copy()
  blob_list = []
  h_img = img.shape[0] 
  w_img = img.shape[1]
  label = 1

  for j in range (0, w_img):
    for i in range (0, h_img):
      if img_out[i][j] == 0 and img_out[i][j] != VISITED and img_out[i][j] != IS_RICE:

        retval, img_out, mask, rect = cv2.floodFill(img_out, None, (j, i), VISITED)
        
        if retval > MIN_RICE_SIZE:
          retval, img_out, mask, rect = cv2.floodFill(img_out, None, (j, i), IS_RICE)
          blob_list.append({"size": retval, "label": label})
          label+=1 

        # show_progress(img_out)

  # back to BGR
  img_out = cv2.cvtColor (img_out, cv2.COLOR_GRAY2BGR)
  return blob_list, img_out

def calculate_mean(blob_list):
  mean = 0
  for blob in blob_list:
    mean += blob["size"]
  mean = mean / len(blob_list)
  return mean

def calculate_dp(blob_list, mean):
  """ Calcula o desvio padrão """
  dp = 0
  for blob in blob_list:
    dp += (blob["size"] - mean)**2
  dp = dp / len(blob_list)
  dp = m.sqrt(dp)
  return dp

def find_outliers(blob_list):
  """ Encontra o maior e o menor blob """
  smaller = {"size": 999}
  bigger = {"size": 0}
  for blob in blob_list:
    if blob["size"] < smaller["size"]:
      smaller = blob
    if blob["size"] > bigger["size"]:
      bigger = blob
  return [smaller, bigger]

# remove bigger and smaller
def remove_outliers(blob_list, outliers):
  blob_list_out = []
  for blob in blob_list:
    if blob["label"] != outliers[0]["label"] and blob["label"] != outliers[1]["label"]:
      blob_list_out.append(blob)
  return blob_list_out

def repeat_process(all_blobs):
  current_blobs = np.copy(all_blobs)
  mean = calculate_mean(current_blobs)
  dp = calculate_dp(current_blobs, mean)
  outliers = find_outliers(current_blobs)
  i = 1
  # print("Geração 1: X = ", mean, "dp = ", dp)
  # print("Outliers: ", outliers)

  while dp > mean * MEAN_THRESHOLD:
    outliers = find_outliers(current_blobs)
    current_blobs = remove_outliers(current_blobs, outliers)
    mean = calculate_mean(current_blobs)
    dp = calculate_dp(current_blobs, mean)
    i += 1
    # print("Geração ", i, ": X = ", mean, "dp = ", dp)
    # print("Outliers: ", outliers)
  return m.floor(mean)

def separate_unsure_blobs(blob_list, rice_size):
  blob_list_out = []
  unsure_blobs = []
  for blob in blob_list:
    if blob["size"] > rice_size * 0.5 and blob["size"] < rice_size * 1.5:
      blob_list_out.append(blob)
    elif blob["size"] > rice_size * 1.5 or blob["size"] < rice_size * 0.5:
      unsure_blobs.append(blob)
  return blob_list_out, unsure_blobs

def separate_couple_blobs(blob_list, unsure_blob_list, rice_size):
  blob_list_out = []
  # append the sure blobs first, blob_list, without checking for size
  # check unsure_blob_list for size and decouple when necessary
  for blob in blob_list:
    blob_list_out.append(blob)
  for blob in unsure_blob_list:
    if blob["size"] >= rice_size * 1.5 and blob["size"] < rice_size * 2.5:
      blob_list_out.append(blob)
      blob_list_out.append(blob)
    elif blob["size"] >= rice_size * 2.5 and blob["size"] < rice_size * 3.5:
      blob_list_out.append(blob)
      blob_list_out.append(blob)
      blob_list_out.append(blob)
    elif blob["size"] >= rice_size * 3.5 and blob["size"] < rice_size * 4.5:
      blob_list_out.append(blob)
      blob_list_out.append(blob)
      blob_list_out.append(blob)
      blob_list_out.append(blob)
    elif blob["size"] >= rice_size * 4.5 and blob["size"] < rice_size * 5.5:
      blob_list_out.append(blob)
      blob_list_out.append(blob)
      blob_list_out.append(blob)
      blob_list_out.append(blob)
      blob_list_out.append(blob)
    elif blob["size"] >= MIN_RICE_SIZE:
      blob_list_out.append(blob)
  return blob_list_out

#===============================================================================

def main ():

  if ENABLE_GUI:
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(initialdir="./img/", title="Select file", filetypes=(("bmp files", "*.bmp"), ("all files", "*.*")))

  img_one, img_two, img_three, img_four, img_five = hp.open_images(INPUT_IMAGE_ONE, INPUT_IMAGE_TWO, INPUT_IMAGE_THREE, INPUT_IMAGE_FOUR, INPUT_IMAGE_FIVE)
  img_one, img_two, img_three, img_four, img_five = hp.images_to_float(img_one, img_two, img_three, img_four, img_five)
  img_one_out, img_two_out, img_three_out, img_four_out, img_five_out = hp.create_copy(img_one, img_two, img_three, img_four, img_five)
  img_one_out, img_two_out, img_three_out, img_four_out, img_five_out = hp.remove_noise(img_one_out, img_two_out, img_three_out, img_four_out, img_five_out)
  img_one_out, img_two_out, img_three_out, img_four_out, img_five_out = hp.threshold(img_one_out, img_two_out, img_three_out, img_four_out, img_five_out)
  
  blob_list_one, img_one_out = label_blobs(img_one_out)
  blob_list_two, img_two_out = label_blobs(img_two_out)
  blob_list_three, img_three_out = label_blobs(img_three_out)
  blob_list_four, img_four_out = label_blobs(img_four_out)
  blob_list_five, img_five_out = label_blobs(img_five_out)

  rice_size_one = repeat_process(blob_list_one)
  rice_size_two = repeat_process(blob_list_two)
  rice_size_three = repeat_process(blob_list_three)
  rice_size_four = repeat_process(blob_list_four)
  rice_size_five = repeat_process(blob_list_five)

  blob_list_one, unsure_blobs_one = separate_unsure_blobs(blob_list_one, rice_size_one)
  blob_list_two, unsure_blobs_two = separate_unsure_blobs(blob_list_two, rice_size_two)
  blob_list_three, unsure_blobs_three = separate_unsure_blobs(blob_list_three, rice_size_three)
  blob_list_four, unsure_blobs_four = separate_unsure_blobs(blob_list_four, rice_size_four)
  blob_list_five, unsure_blobs_five = separate_unsure_blobs(blob_list_five, rice_size_five)
  
  blob_list_one_uncoupled = separate_couple_blobs(blob_list_one, unsure_blobs_one, rice_size_one)
  blob_list_two_uncoupled = separate_couple_blobs(blob_list_two, unsure_blobs_two, rice_size_two)
  blob_list_three_uncoupled = separate_couple_blobs(blob_list_three, unsure_blobs_three, rice_size_three)
  blob_list_four_uncoupled = separate_couple_blobs(blob_list_four, unsure_blobs_four, rice_size_four)
  blob_list_five_uncoupled = separate_couple_blobs(blob_list_five, unsure_blobs_five, rice_size_five)

  

  print("------------------------------------------")
  print("Tamanho / Grãos / Incertos / Desacoplados (ou recontados)")
  print("IMG 1: " + str(rice_size_one) + "/ GR:" + str(len(blob_list_one)) + "/ UNS: " + str(len(unsure_blobs_one)) + "/ UNC: " + str(len(blob_list_one_uncoupled)))
  print("IMG 2: " + str(rice_size_two) + "/ GR:" + str(len(blob_list_two)) + "/ UNS: " + str(len(unsure_blobs_two)) + "/ UNC: " + str(len(blob_list_two_uncoupled)))
  print("IMG 3: " + str(rice_size_three) + "/ GR:" + str(len(blob_list_three)) + "/ UNS: " + str(len(unsure_blobs_three)) + "/ UNC: " + str(len(blob_list_three_uncoupled)))
  print("IMG 4: " + str(rice_size_four) + "/ GR:" + str(len(blob_list_four)) + "/ UNS: " + str(len(unsure_blobs_four)) + "/ UNC: " + str(len(blob_list_four_uncoupled)))
  print("IMG 5: " + str(rice_size_five) + "/ GR:" + str(len(blob_list_five)) + "/ UNS: " + str(len(unsure_blobs_five)) + "/ UNC: " + str(len(blob_list_five_uncoupled)))
  print("------------------------------------------")
  
  line_one = np.concatenate((img_one, img_one_out), axis=1)
  line_two = np.concatenate((img_two, img_two_out), axis=1)
  line_three = np.concatenate((img_three, img_three_out), axis=1)
  line_four = np.concatenate((img_four, img_four_out), axis=1)
  line_five = np.concatenate((img_five, img_five_out), axis=1)
  join_lines = np.concatenate((line_one, line_two, line_three, line_four, line_five), axis=0) #Vertical
  
  """
  join_inputs = np.concatenate((img_one, img_two, img_three, img_four), axis=1) #Horizontal
  join_outputs = np.concatenate((img_one_out, img_two_out, img_three_out, img_four_out), axis=1) #Horizontal
  join_both = np.concatenate((join_inputs, join_outputs), axis=0) #Vertical
  """

  cv2.namedWindow('original - thresholded and filled', cv2.WINDOW_NORMAL)
  cv2.resizeWindow('original - thresholded and filled', 1440, 900)
  
  cv2.imshow ('original - thresholded and filled', join_lines)
  cv2.waitKey () if LEAVE_OPEN else cv2.waitKey (OPEN_TIME)
  cv2.destroyAllWindows ()

if __name__ == '__main__':
  main ()
    
#===============================================================================

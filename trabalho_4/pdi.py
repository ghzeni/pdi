import sys
import timeit
import numpy as np
import cv2
import math as m
import single_file as sf
NOT_VISITED = 1
VISITED = 0.5

def label_blobs(img):

  img_out = img.copy()
  blob_list = []
  h_img = img.shape[0] 
  w_img = img.shape[1]
  label = 1

  for i in range (0, h_img):
    for j in range (0, w_img):
      if img[i][j][0] == NOT_VISITED:  
        no_pixels = 1
        img_out = cv2.floodFill(img, None, (i, j), VISITED)
        blob_list.append({"size": no_pixels, "label": label, "dp": 0})
        label+=1
        sf.show_progress(img_out, '26')
    
  return blob_list

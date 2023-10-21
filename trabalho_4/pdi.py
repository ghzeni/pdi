import sys
import timeit
import numpy as np
import cv2
import math as m
NOT_VISITED = 1
VISITED = 0.5
global label

def label_blobs(img):

  img_gray = cv2.cvtColor (img, cv2.COLOR_BGR2GRAY)
  blob_list = []
  w_img = img.shape[0] 
  h_img = img.shape[1]
  label = 1

  ### Retorna um blob_list com cada blob encontrada
  def flood_fill(x, y, no_pixels):
    if (x<0 or x>=h_img or y<0 or y>=w_img):
      return
    if img_gray[x][y] != NOT_VISITED:
      return
    if img_gray[x][y] == VISITED:
      return
    if img_gray[x][y] == NOT_VISITED:
      img_gray[x][y] = VISITED
      no_pixels+=1
      

    flood_fill(x-1,y)
    flood_fill(x+1,y)
    flood_fill(x,y-1)
    flood_fill(x,y+1)
    flood_fill(x-1,y-1)
    flood_fill(x-1,y+1)
    flood_fill(x+1,y-1)
    flood_fill(x+1,y+1)

  for y in range (0, h_img):
    for x in (0, w_img):
      if img[x][y] == 1
        no_pixels = 1
        flood_fill(x, y, no_pixels)
        blob_list.add({size: no_pixels, label: label, dp: 0})
        label+=1
      
    
  return label_matrix

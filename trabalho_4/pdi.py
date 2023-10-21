import sys
import timeit
import numpy as np
import cv2
import math as m
NOT_VISITED = 1
VISITED = 0.5
global label

def label_blobs(img):

  """   
  # grayscale
  img_gray = cv2.cvtColor (img, cv2.COLOR_BGR2GRAY)
  blob_list = []
  """
  h_img = len(img)
  w_img = len(img[0])
  label = 1

  label_matrix = [ 
      [0,0,0,0,0,0,0,0,0,0],
      [0,0,1,0,0,0,0,0,0,0],
      [0,0,1,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0],
      [0,0,0,1,0,0,1,1,0,0],
      [0,0,0,1,0,0,1,0,0,0],
      [0,0,0,0,0,0,0,0,0,0],
      [0,0,1,0,0,0,1,0,0,0],
      [0,0,1,0,0,1,1,0,0,0],
      [0,0,1,0,0,0,0,0,0,0]
      ]
  
  for i in range(h_img):
      for j in range(w_img):
        if img[i][j] == 1:
          label_matrix[i][j] = -1
        else:
          label_matrix[i][j] = 0

  print("Label matrix: \n")
  for i in range(h_img):
      for j in range(w_img):
          print(label_matrix[i][j], end=" ")
      print()


  ### Retorna um blob_list com cada blob encontrada
  def flood_fill(x, y):
    if (x<0 or x>=h_img or y<0 or y>=w_img):
      return False
    if img[x][y] != NOT_VISITED:
      return
    if img[x][y] == VISITED:
      return
    if img[x][y] == NOT_VISITED:
      label_matrix[x][y] = label

    flood_fill(x-1,y)
    flood_fill(x+1,y)
    flood_fill(x,y-1)
    flood_fill(x,y+1)
    # flood_fill(x-1,y-1)
    # flood_fill(x-1,y+1)
    # flood_fill(x+1,y-1)
    # flood_fill(x+1,y+1)

  for y in range (0, h_img):
    for x in (0, w_img):
      flood_fill(x, y)

      
    
  return label_matrix
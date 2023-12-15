#===============================================================================
# Exemplo: segmentação de uma imagem em escala de cinza.
#-------------------------------------------------------------------------------
# Autor: Bogdan T. Nassu
# Universidade Tecnológica Federal do Paraná
#===============================================================================

import sys
import timeit
import numpy as np
import cv2
import math as m
import json
import unittest

#===============================================================================

INPUT_IMAGE =  'arroz_input/arroz.bmp'
NEGATIVO = False
THRESHOLD = 0.81
ALTURA_MIN = 5
LARGURA_MIN = 5
N_PIXELS_MIN = 20

#===============================================================================

def binariza (img, threshold):
    img_matrix = img
    white = 1
    black = 0

    img_bin = np.where((img_matrix >= threshold), white, black)
    return img_bin

#-------------------------------------------------------------------------------

def update_boundries(blob, row, col):
    # não importa onde a coordenada tá em y, 
    # só importa que ela é mais pra cima (menor valor) do que a y atual
    if row < blob['T'][0]: # row < row
        blob['T'] = (row, col)
    if row >= blob['B'][0]:
        blob['B'] = (row, col)
    if col < blob['L'][1]:
        blob['L'] = (row, col)
    if col >= blob['R'][1]:
        blob['R'] = (row, col)
    return blob

#-------------------------------------------------------------------------------

def flood_fill(matrix, label, row, col, width, height):
    # recursão = começar de trás
    if row < 0 or row >= height or col < 0 or col >= width:
      return

    if matrix[row][col][0] != -1:
      return 
  
    matrix[row][col][0] = label

    flood_fill(matrix, label, row-1, col, width, height)
    flood_fill(matrix, label, row, col+1, width, height)
    flood_fill(matrix, label, row+1, col, width, height)
    flood_fill(matrix, label, row, col-1, width, height)
    return

#-------------------------------------------------------------------------------

def remover_mini_blobs(blob_list, largura_min, altura_min, n_pixels_min):

  blist = []

  for b in blob_list:
    if (b['n_pixels'] > n_pixels_min and b['R'][1] - b['L'][1] >= largura_min and b['B'][0] - b['T'][0] >= altura_min):
       blist.append(b)

  return blist

#-------------------------------------------------------------------------------

def group_blobs(blob_list):
  for b in blob_list:
    for b2 in blob_list:
      if b['label'] != b2['label']:
        if b['T'][0] <= b2['T'][0] <= b['B'][0] or b['T'][0] <= b2['B'][0] <= b['B'][0]:
          if b['L'][1] <= b2['L'][1] <= b['R'][1] or b['L'][1] <= b2['R'][1] <= b['R'][1]:
            b['n_pixels'] += b2['n_pixels']
            b['T'] = (min(b['T'][0], b2['T'][0]), min(b['T'][1], b2['T'][1]))
            b['R'] = (max(b['R'][0], b2['R'][0]), max(b['R'][1], b2['R'][1]))
            b['B'] = (max(b['B'][0], b2['B'][0]), max(b['B'][1], b2['B'][1]))
            b['L'] = (min(b['L'][0], b2['L'][0]), min(b['L'][1], b2['L'][1]))
            blob_list.remove(b2)
            return group_blobs(blob_list)
  return blob_list

#-------------------------------------------------------------------------------

def rotula (binarizada, largura_min, altura_min, n_pixels_min): 

  height = binarizada.shape[0]
  width = binarizada.shape[1]

  matrix = np.where((binarizada == 1), -1, 0) # -1 = não visitado, 0 = background

  label = 1
  for row in range (0, height):
    for col in range (0, width):
      if matrix[row][col][0] == -1:
        flood_fill(matrix, label, row, col, width, height)
        label += 1
        
  blob_list = []

  for row in range (0, height):
    for col in range (0, width):  
      label_atual = matrix[row][col][0]
      if label_atual != 0:
        if len(blob_list) != 0:
          label_existe = False
          for b in blob_list:
            if b['label'] == label_atual:
              label_existe = True
              b['n_pixels'] += 1
              b = update_boundries(b, row, col)
                
          # se não houver uma blob inicializada com aquele label até o momento
          if not label_existe:
            blob = {
              'label': label_atual,
              'n_pixels': 1,
              'T': (row, col), 
              'R': (row, col), 
              'B': (row, col), 
              'L': (row, col), 
            }
            blob_list.append(blob)
        else:
          # se a blob_list for vazia
          blob = {
            'label': matrix[row][col][0],
            'n_pixels': 1,
            'T': (row, col), 
            'R': (row, col), 
            'B': (row, col), 
            'L': (row, col), 
          }
          blob_list.append(blob)

  # excluimos blobs pequenas demais
  blob_list = remover_mini_blobs(blob_list, largura_min, altura_min, n_pixels_min)

  # agrupar blobs que se tocam
  blob_list = group_blobs(blob_list)

  return blob_list

#-------------------------------------------------------------------------------

def count_rice(input_image, invert_image, threshold, min_height, min_width, min_pixel_amount):

  img = cv2.imread (input_image)

  if img is None:
      print ('Erro abrindo a imagem.\n')
      sys.exit ()

  img = img.astype (np.float32) / 255

  if invert_image:
      img = 1 - img

  imgb = binariza (img, threshold)

  cv2.imwrite ('01 - binarizada.png', imgb.astype(np.int8) * 255)

  start_time = timeit.default_timer ()
  componentes = rotula (imgb, min_width, min_height, min_pixel_amount)
  n_componentes = len (componentes)
      
  # Mostra os objetos encontrados.
  for c in componentes:
    cv2.rectangle (img, (c ['L'][1], c ['T'][0]), (c ['R'][1], c ['B'][0]), (0,0,255), 2)

  return (n_componentes, timeit.default_timer () - start_time, img)


#===============================================================================

def main ():
  output = count_rice(INPUT_IMAGE, NEGATIVO, THRESHOLD, ALTURA_MIN, LARGURA_MIN, N_PIXELS_MIN)
  print ('Tempo: %f' % output[1])
  print ('%d componentes detectados.' % output[0])
    
  cv2.namedWindow('02 - out', cv2.WINDOW_NORMAL)
  cv2.resizeWindow('02 - out', 1440, 900)
  cv2.imwrite ('02 - out.png', output[2]*255)
  imgshow = cv2.imread('02 - out.png')
  cv2.imshow ('02 - out', imgshow)
  cv2.waitKey ()
  cv2.destroyAllWindows ()


if __name__ == '__main__':
    main ()
    
#===============================================================================

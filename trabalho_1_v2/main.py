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

#===============================================================================

INPUT_IMAGE =  'arroz.bmp'

NEGATIVO = False
THRESHOLD = 0.8
ALTURA_MIN = 15
LARGURA_MIN = 15
N_PIXELS_MIN = 30

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

    if matrix[row][col] != -1:
      return 
  
    matrix[row][col] = label

    flood_fill(matrix, label, row-1, col, width, height)
    flood_fill(matrix, label, row, col+1, width, height)
    flood_fill(matrix, label, row+1, col, width, height)
    flood_fill(matrix, label, row, col-1, width, height)
    return

#-------------------------------------------------------------------------------

def rotula (binarizada, largura_min, altura_min, n_pixels_min): 

  height = binarizada.shape[0]
  width = binarizada.shape[1]

  matrix = np.where((binarizada == 1), -1, 0) # -1 = não visitado, 0 = background

  label = 1
  for row in range (0, height):
    for col in range (0, width):
      if matrix[row][col] == -1:
        flood_fill(matrix, label, row, col, width, height)
        label += 1
        
  blob_list = []

  # após toda a matriz estar com os devidos labels, agrupamos as blobs
  # excluindo blobs pequenas demais
  for row in range (0, height):
    for col in range (0, width):  
      label_atual = matrix[row][col]
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
            'label': matrix[row][col],
            'n_pixels': 1,
            'T': (row, col), 
            'R': (row, col), 
            'B': (row, col), 
            'L': (row, col), 
          }
          blob_list.append(blob)
  
  # print('122: ' + str(blob_list))
  
  # limpa as que forem mini-blobs demais pra ser uma blob
  for b in blob_list:
    if (b['n_pixels'] < n_pixels_min):
      blob_list.remove(b)
    elif (b['R'][1] - b['L'][1] > largura_min):
      blob_list.remove(b)
    elif (b['B'][0] - b['T'][0] > altura_min):
      blob_list.remove(b)
  
  return blob_list

#===============================================================================

def main ():

    # Abre a imagem em escala de cinza.
    global img, imgb
    img = cv2.imread (INPUT_IMAGE, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

    img = img.reshape ((img.shape [0], img.shape [1], 1))
    img = img.astype (np.float32) / 255

    img_out = cv2.cvtColor (img, cv2.COLOR_GRAY2BGR)

    if NEGATIVO:
        img = 1 - img
    imgb = binariza (img, THRESHOLD)
    cv2.imwrite ('01 - binarizada.png', imgb.astype(np.int8) * 255)
    imgshow = cv2.imread('01 - binarizada.png', 0)
    cv2.imshow ('01 - binarizada', imgshow)

    start_time = timeit.default_timer ()
    componentes = rotula (imgb, LARGURA_MIN, ALTURA_MIN, N_PIXELS_MIN)
    n_componentes = len (componentes)
    print ('Tempo: %f' % (timeit.default_timer () - start_time))
    print ('%d componentes detectados.' % n_componentes)

    # Mostra os objetos encontrados.
    for c in componentes:
        cv2.rectangle (img_out, (c ['L'], c ['T']), (c ['R'], c ['B']), (0,0,255))

    cv2.imshow ('02 - out', img_out)
    cv2.imwrite ('02 - out.png', img_out*255)
    cv2.waitKey ()
    cv2.destroyAllWindows ()

if __name__ == '__main__':
    main ()
    
#===============================================================================

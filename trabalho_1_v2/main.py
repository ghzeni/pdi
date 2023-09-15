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

# TODO: ajuste estes parâmetros!
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

def rotula (binarizada, largura_min, altura_min, n_pixels_min):
    global width_img, height_img, nova_matriz, blob_list
    height_img = binarizada[0].size
    width_img = int(binarizada.size/height_img)

    nova_matriz = np.where((binarizada == 1), -1, 0)

    label = 1
    for y in range (0, height_img-1):
      for x in range (0, width_img-1):
        # só olha se for -1, se não nem olha
        if nova_matriz[x][y][0] == -1:
          flood_fill(label, x, y) 
          label += 1
          
    
    # aqui já temos toda a nova_matriz labelada

    blob_list = []

    # após toda a matriz estar com os devidos labels, agrupamos as blobs
    # excluindo blobs pequenas demais
    for y in range (0, height_img-1):
      for x in range (0, width_img-1):
        # se a coord checada não é 0 (background)
        label_atual = nova_matriz[x][y][0]
        if label_atual != 0:
          if len(blob_list) != 0:
            label_existe = False
            for b in blob_list:
               if b['label'] == label_atual:
                  label_existe = True
                  b['n_pixels'] += 1
                  b = update_boundries(b, x, y)
            # se não houver uma blob inicializada com aquele label até o momento
            if not label_existe:
              blob = {
                'label': label_atual,
                'n_pixels': 1,
                'T': (x, y), 
                'R': (x, y), 
                'B': (x, y), 
                'L': (x, y), 
              }
              blob_list.append(blob)
          else:
            # se a blob_list for vazia
            blob = {
              'label': nova_matriz[x][y][0],
              'n_pixels': 1,
              'T': (x, y), 
              'R': (x, y), 
              'B': (x, y), 
              'L': (x, y), 
            }
            blob_list.append(blob)
      
    # limpa as que forem mini-blobs demais pra ser uma blob
    for b in blob_list:
      if (b['n_pixels'] < n_pixels_min) or (b['R'][0] - b['L'][0] < largura_min) or (b['B'][1] - b['T'][1] < altura_min):
        blob_list.remove(b)
    
    return blob_list

def flood_fill(label, x0, y0):

  nova_matriz[x0][y0] = label

  """ T """
  if dentro_img(x0,y0-1) and not_bkg(x0,y0-1) and nova_matriz[x0][y0-1][0] == -1:
    flood_fill(label, x0, y0-1)

  """ R """        
  if dentro_img(x0+1,y0) and not_bkg(x0+1,y0) and nova_matriz[x0+1][y0][0] == -1:         
    flood_fill(label, x0+1, y0)

  """ B """
  if dentro_img(x0,y0+1) and not_bkg(x0,y0+1) and nova_matriz[x0][y0+1][0] == -1:
    flood_fill(label, x0, y0+1)
  
  """ L """
  if dentro_img(x0-1,y0) and not_bkg(x0-1,y0) and nova_matriz[x0-1][y0][0] == -1:
    flood_fill(label, x0-1, y0)

  return

def update_boundries(blob, x, y):
  # não importa onde a coordenada tá em y, 
  # só importa que ela é mais pra cima (menor valor) do que a y atual
  if y < blob['T'][1]:
      blob['T'] = (x, y)
  if x > blob['R'][0]:
      blob['R'] = (x, y)
  if y > blob['B'][1]:
      blob['B'] = (x, y)
  if x < blob['L'][0]:
      blob['L'] = (x, y)
  return blob
    
def dentro_img (x, y):
  if (x >= 0) and (x < width_img-1) and (y >= 0) and (y < height_img-1):
    return True
  return False

def not_bkg (x, y):
  if imgb[x][y] != 0:
    return True
  return False

#===============================================================================

def main ():

    # Abre a imagem em escala de cinza.
    global img, imgb
    img = cv2.imread (INPUT_IMAGE, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

    # É uma boa prática manter o shape com 3 valores, independente da imagem ser
    # colorida ou não. Também já convertemos para float32.
    img = img.reshape ((img.shape [0], img.shape [1], 1))
    img = img.astype (np.float32) / 255

    # Mantém uma cópia colorida para desenhar a saída.
    img_out = cv2.cvtColor (img, cv2.COLOR_GRAY2BGR)

    # Segmenta a imagem.
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

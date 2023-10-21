#===============================================================================
# Trabalho 3: Blur
#-------------------------------------------------------------------------------
# Autor: Gustavo Henrique Zeni
# Universidade Tecnológica Federal do Paraná
#===============================================================================

# import tkinter as tk
# from tkinter import filedialog
import sys
import timeit
import numpy as np
import cv2
import math as m

#===============================================================================
#TODO: ajustar
INPUT_IMAGE =  'Wind Waker GC.bmp'
ENABLE_GUI = False
JANELA_W = 9
JANELA_H = 9
KSIZE = 5
KSIZE_RATIO = 3

#===============================================================================

def show_progress (img, line):
  cv2.imshow ('main.py:' + line, img)
  cv2.waitKey ()
  cv2.destroyWindow ('main.py:' + line)

#-------------------------------------------------------------------------------
def box_bloom(img_entrada, width, height):

  show_progress (img_entrada, '35')
  img_output = np.copy(img_entrada)
  img_color = np.copy(img_entrada)

  
  # convert to HLS
  # img_converted = cv2.cvtColor(img_output, cv2.COLOR_BGR2HLS)
  # _, img_limiar = cv2.threshold(img_converted, 0.5, 1, cv2.THRESH_BINARY, img_output)
  
  # convert to gray_scale
  img_converted = cv2.cvtColor(img_output, cv2.COLOR_BGR2GRAY)
  _, img_limiar = cv2.threshold(img_converted, 0.7, 1, cv2.THRESH_BINARY, img_output)

  # borrar a imagem limiarizada
  img_blur = cv2.blur(img_limiar, (width, height))
  img_blur = cv2.blur(img_blur, (width, height))
  img_blur = cv2.blur(img_blur, (width, height))

  img_blur2 = cv2.blur(img_limiar, (width*KSIZE_RATIO, height*KSIZE_RATIO))
  img_blur2 = cv2.blur(img_blur2, (width*KSIZE_RATIO, height*KSIZE_RATIO))
  img_blur2 = cv2.blur(img_blur2, (width*KSIZE_RATIO, height*KSIZE_RATIO))

  img_blur3 = cv2.blur(img_limiar, (width*KSIZE_RATIO^2, height*KSIZE_RATIO^2))
  img_blur3 = cv2.blur(img_blur3, (width*KSIZE_RATIO^2, height*KSIZE_RATIO^2))
  img_blur3 = cv2.blur(img_blur3, (width*KSIZE_RATIO^2, height*KSIZE_RATIO^2))
  # repetir N vezes:
  # imagem_borrada = imagem pelo filtro da média com janela widthxheight

  img_output = img_color + cv2.cvtColor(img_blur,cv2.COLOR_GRAY2RGB) + cv2.cvtColor(img_blur2,cv2.COLOR_GRAY2RGB) + cv2.cvtColor(img_blur2,cv2.COLOR_GRAY2RGB)

  show_progress (img_output, '63')

  return img_output
  # somar imagem_borrada com img_entrada
  # encontrar uma forma de 
  # evitar que o resultado fique muito “estourado”.
#-------------------------------------------------------------------------------

def gaussian_bloom(img_entrada, width, height):

  img_output = np.copy(img_entrada)
  img_color = np.copy(img_entrada)

  # convert to gray_scale
  img_converted = cv2.cvtColor(img_output, cv2.COLOR_BGR2GRAY)

  # limiarização global
  _, img_limiar = cv2.threshold(img_converted, 0.7, 1, cv2.THRESH_BINARY, img_converted)

  # borrar a imagem limiarizada
  img_blur = cv2.GaussianBlur(img_limiar, (width, height), KSIZE)
  img_blur_2 = cv2.GaussianBlur(img_limiar, (width, height), KSIZE^2)
  img_blur_3 = cv2.GaussianBlur(img_limiar, (width, height), KSIZE^3)
  img_output = img_color + cv2.cvtColor(img_blur,cv2.COLOR_GRAY2RGB) + cv2.cvtColor(img_blur_2,cv2.COLOR_GRAY2RGB) + cv2.cvtColor(img_blur_3,cv2.COLOR_GRAY2RGB)

  return img_output


#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------


#===============================================================================

def main ():

    if ENABLE_GUI:
      root = tk.Tk()
      root.withdraw()
      file_path = filedialog.askopenfilename()

    # Abre a imagem em escala de cinza.
    img = cv2.imread (file_path if ENABLE_GUI else INPUT_IMAGE)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

    # É uma boa prática manter o shape com 3 valores, independente da imagem ser
    # colorida ou não. Também já convertemos para float32.
    # img = img.reshape ((img.shape [0], img.shape [1], 1))
    img = img.astype (np.float32) / 255

    # Mantém uma cópia colorida para desenhar a saída.
    img_out = np.copy(img)

    # Inicia o timer
    start_time = timeit.default_timer ()

    
    # Ingênuo
    img_box = box_bloom(img, JANELA_W, JANELA_H)
    print ('Box bloom finalizado.')
    print ('Tempo: %f' % (timeit.default_timer () - start_time))
    cv2.imshow ('01 - Box bloom', img_box)
    
    # Separável
    img_gaussian = gaussian_bloom(img, JANELA_W, JANELA_H)
    print ('Gaussian bloom finalizado.')
    print ('Tempo: %f' % (timeit.default_timer () - start_time))

    cv2.imshow ('02 - Gaussian bloom', img_gaussian)
    cv2.imshow ('00 - img original', img_out)
    cv2.waitKey ()
    cv2.destroyAllWindows ()

if __name__ == '__main__':
    main ()
    
#===============================================================================

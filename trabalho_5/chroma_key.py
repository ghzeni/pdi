#===============================================================================
# Trabalho 5: Chroma Key
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
import os

# TODO: gerar explicitamente uma máscara de "verdíce" - uma espécie de grau do quão verde é aquele pixel
  # copiar imagem com todos os pixels sendo 0
    # np copy as
  # o que é verde aceitável e o que é verde demais?
    # definir threshold
  # vou varrer a imagem duas vezes, vou encontrar o pixel mais verde
    # max = 0
    # dois for
    # pro próximo pixel, se nivel_verde(pixel) > max
  # max = pixel
  # que existe nela, vou chamar isso de MÁXIMO
  # vou repassar a imagem, normalizando de forma que todos os pixels
  # verde sejam algum valor entre 0 e 1, sendo 1 o máximo
  # vou delimitar o threshold de pixel verde como sendo 40%
  # o output vai ser uma imagem com pixels brancos, cinzas e pretos
  # pra cada pixel cujo valor não seja 0, vou excluir esse 
  # pixel da outra imagem (que não é a máscara)
    # aqui é o momento que excluir significa usar o que tá no fundo
    # não sei como funciona pra exportar um PNG com um valor
    # literalmente vazio, então vou fazer dessa forma
# TODO: alphablending FG*m + BG*(1-m)
# o que é alphablending? o que é essa fórmula?
# FG é foreground, BG é background, o que é m?
# preciso fazer assim pra juntar as duas imagens?

#===============================================================================

INPUT_IMAGE = 'img/114.bmp'
ENABLE_GUI = True
LEAVE_OPEN = True
OPEN_TIME = 1500

#-----------

  # funcao nivel_verde(pixel)
    # bgr to hsv = cv.cvtColor(input_image, cv.COLOR_BGR2HSV
    # define range of green color in HSV
    # lower_green = np.array([50 100 100])
    # upper_green = np.array([70 255 255])
    # threshold the HSV image to get only green colors
    # mask = cv.inRange(hsv, lower_green, upper_green)
    # mascara de verdice de 0 a 1 pra criar o alphablending
    # rgb é mais fácil

# pra HSV, matiz tem o intervalo [0, 179] -> 180 graus
# saturação tem [0, 255] e a range do valor é [0, 255]


#===============================================================================

def main ():

  if ENABLE_GUI:
      root = tk.Tk()
      root.withdraw()
      file_path = filedialog.askopenfilename(initialdir="./trabalho_4/img/", title="Select file", filetypes=(("bmp files", "*.bmp"), ("all files", "*.*")))
  else:
      file_path = INPUT_IMAGE
  
  img = cv2.imread (file_path)
  if img is None:
      print ('Erro abrindo a imagem 1.\n')
      sys.exit ()

  # Converter pra float e fazer de [0, 255] pra [0, 1]
  img = img.astype (np.float32) / 255
  img_out = np.copy(img)
  img_step_two = rc.gaussian_blur(img_out)
  img_step_three = rc.all_thresholds(img_step_two)
  blob_list, img_step_four = rc.label_blobs(img_step_three)
  rice_size = rc.repeat_process(blob_list)
  blob_list, unsure_blobs = rc.separate_unsure_blobs(blob_list, rice_size)
  blob_list_uncoupled = rc.separate_couple_blobs(blob_list, unsure_blobs, rice_size)

  print("------------------------------------------")
  print("Tamanho / Grãos / Incertos / Desacoplados (ou recontados)")
  print("IMG 1: " + str(rice_size) + "/ GR:" + str(len(blob_list)) + "/ UNS: " + str(len(unsure_blobs)) + "/ UNC: " + str(len(blob_list_uncoupled)))
  print("------------------------------------------")

  column_one = np.concatenate((img, img_step_three, img_step_four), axis=1)
  
  cv2.namedWindow('original - threshold - flood_filled', cv2.WINDOW_NORMAL)
  cv2.resizeWindow('original - threshold - flood_filled', 1440, 900)
  
  cv2.imshow ('original - threshold - flood_filled', column_one)
  cv2.waitKey () if LEAVE_OPEN else cv2.waitKey (OPEN_TIME)
  cv2.destroyAllWindows ()

if __name__ == '__main__':
  main ()
    
#===============================================================================

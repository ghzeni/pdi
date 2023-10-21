#===============================================================================
# Trabalho 2: Blur
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
INPUT_IMAGE =  'screenshot.png'
ENABLE_GUI = False
JANELA_W = 9
JANELA_H = 9

#===============================================================================

def naive_blur(img_entrada, width, height):

  img_blur = np.empty_like (img_entrada)


  """ 
  for (cada linha y)
    for (cada coluna x)
    {
      soma = 0;
      for (cada linha y' no intervalo [y-h/2,y+h/2])
      for (cada coluna x' no intervalo [x-w/2,x+w/2])
      soma += f(x',y')
      g(x,y) = soma / (h*w)
    } 

  """
  w_img = img_entrada.shape [0] 
  h_img = img_entrada.shape [1]

  # TODO: arrumar cores
  for c in range (0, 3):
    for y in range(width//2, (w_img-width//2)):
        for x in range(height//2, (h_img-height//2)):
            soma = 0
            for yw in range(y-height//2, y+height//2+1): # divisão de inteiro // yw = ywindow
                for xw in range(x-width//2, x+width//2+1):
                    soma += img_entrada[yw, xw, c]
            img_blur[y, x, c] = soma/(width*height)
  
  return img_blur
                

#-------------------------------------------------------------------------------

def separable_blur(img_entrada, width, height):
  img_blur = np.empty_like (img_entrada)

  w_img = img_entrada.shape [0] 
  h_img = img_entrada.shape [1]

  # TODO: arrumar cores
  for c in range (0, 3): # 0, 1, 2
    for y in range(width//2, (w_img-width//2)): # pra cada linha
      for x in range(height//2, (h_img-height//2)): # pra cada coluna
        soma = 0
        for xw in range(x-width//2, x+width//2+1):
          soma += img_entrada[y, xw, c]
        img_blur[y, x, c] = soma/(width)

    for x in range(height//2, (h_img-height//2)): 
      for y in range(width//2, (w_img-width//2)): 
        soma = 0
        for yw in range(y-height//2, y+height//2+1):
          soma += img_blur[yw, x, c]
        img_blur[y, x, c] = soma/(height)
  
  return img_blur

#-------------------------------------------------------------------------------

def integral_blur(img_entrada, width, height):
  img_integral = np.empty_like(img_entrada)
  img_blur = np.empty_like(img_entrada)

  h_img = img_entrada.shape[0]
  w_img = img_entrada.shape[1]

  def cap(numero, limite):
      if numero < 0:
          return 0
      elif numero >= limite:
          return limite - 1
      else:
          return numero

  for c in range(0, 3):  # 0, 1, 2
      for y in range(0, h_img):
          img_integral[y, 0, c] = img_entrada[y, 0, c]
          for x in range(1, w_img):
              img_integral[y, x, c] = img_entrada[y, x, c] + img_integral[y, x - 1, c]

      for x in range(0, w_img):
          for y in range(0, h_img):
              soma = 0
              upper_left, upper_right, lower_left, lower_right = False, False, False, False

              window = width*height

              if (y == 0 and x == 0): 
                lower_right = True         
                window = width//2 * height//2
              elif (y == 0 and x == w_img - 1): 
                lower_right, lower_left = True, True
                window = width//2 * height//2
              elif (y == h_img - 1 and x == 0):
                lower_right, upper_right = True, True
                window = width//2 * height//2
              elif (y == 0):
                lower_right, lower_left = True, True
                window = width * height//2
              elif (x == 0):
                lower_right, upper_right = True, True
                window = width//2 * height
              else: 
                upper_left, upper_right, lower_left, lower_right = True, True, True, True

              

              if lower_right:
                  soma += img_integral[cap(y + height // 2, h_img), cap(x + width // 2, w_img), c]

              if upper_right:
                  soma -= img_integral[cap(y - height // 2 - 1, h_img), cap(x + width // 2, w_img), c]

              if lower_left:
                  soma -= img_integral[cap(y + height // 2, h_img), cap(x - width // 2 - 1, w_img), c]

              if upper_left:
                  soma += img_integral[cap(y - height // 2 - 1, h_img), cap(x - width // 2 - 1, w_img), c]

              

              img_blur[y, x, c] = soma / window

  return img_blur


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
    # img_naive = naive_blur(img, JANELA_W, JANELA_H)
    print ('naive-blur finalizado.')
    print ('Tempo: %f' % (timeit.default_timer () - start_time))

    # Separável
    # img_separable = separable_blur(img, JANELA_W, JANELA_H)
    print ('separable-blur finalizado.')
    print ('Tempo: %f' % (timeit.default_timer () - start_time))

    # Integral
    img_int = integral_blur(img, JANELA_W, JANELA_H)
    print ('integral-blur finalizado.')
    print ('Tempo: %f' % (timeit.default_timer () - start_time))

    # cv2.imshow ('01 - naive-blur', img_naive)
    # cv2.imshow ('02 - separable-blur', img_separable)
    cv2.imshow ('03 - integral-blur', img_int)
    cv2.imshow ('00 - img original', img_out)
    cv2.waitKey ()
    cv2.destroyAllWindows ()

if __name__ == '__main__':
    main ()
    
#===============================================================================

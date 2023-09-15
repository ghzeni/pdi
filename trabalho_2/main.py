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
INPUT_IMAGE =  '01 - naive-blur.bmp'
ENABLE_GUI = False
JANELA_W = 3
JANELA_H = 3

#===============================================================================

def naive_blur(img_entrada, width, height):

  print (img_entrada.shape)

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
                    soma += img_entrada[yw, xw][c]
            img_blur[y, x][c] = soma/(width*height)
  
  print (img_blur.shape)
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
          soma += img_entrada[y, xw][c]
        img_blur[y, x][c] = soma/(width)

    for x in range(height//2, (h_img-height//2)): 
      for y in range(width//2, (w_img-width//2)): 
        soma = 0
        for yw in range(y-height//2, y+height//2+1):
          soma += img_blur[yw, x][c]
        img_blur[y, x][c] = soma/(height)
  
  return img_blur

#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------



def integral_blur(img_entrada, width, height):
  img_integral = np.empty_like (img_entrada)
  img_blur = np.empty_like (img_entrada)

  w_img = img_entrada.shape [0] 
  h_img = img_entrada.shape [1]

  def cap(numero):
    if numero >= w_img:
       return w_img-1
    if numero >= h_img:
       return h_img-1
    if numero < 0:
       return 0
    
  for c in range(0, 3): # 0, 1, 2

    # passa somando os valores apenas nas linhas
    for y in range(0, w_img): # pra cada linha
      img_integral [y, 0, c] = img_entrada[y, 0][c]
      for x in range(1, h_img): # pra cada coluna menos a primeira
        # img integral é o pixel atual + a soma dos que estão acima e à esquerda dele
        img_integral[y, x][c] = img_entrada[y, x][c] + img_integral[y, x-1][c]

    # passa somando os valores já somados, agora verticalmente
    for y in range(1, w_img):
      #TODO: testar
      img_integral [0, x][c] = img_entrada[0, x][c]
      for x in range (0, h_img):
        img_integral[y, x][c] = img_integral[y, x][c] + img_integral[y-1, x][c]


    for y in range(width//2, (w_img-width//2)):
      for x in range(height//2, (h_img-height//2)):
        soma = 0
        upper_left = False
        upper_right = False
        lower_left = False
        lower_right = False

        # 9 casos:
        # 1) canto superior esquerdo
        if (y == 0 and x == 0):
          # - apenas somo o pixel dentro do canto inferior direito de uma janela
          lower_right = True
        # 2) canto superior direito
        elif (y == 0 and x == w_img-1):
          # - somo o pixel dentro do canto inferior direito de uma janela
          lower_right = True
          # - subtraio o pixel que tá à esquerda do canto inferior esquerdo de uma janela
          lower_left = True
        # 3) canto inferior esquerdo
        elif (y == h_img-1, x == 0):
          # - somo o pixel dentro do canto inferior direito de uma janela
          lower_right = True
          # - subtraio o pixel que tá acima do canto superior direito de uma janela
          upper_right = True

        # 4) canto inferior direito
        elif (y == h_img-1, x == w_img-1):
          # - todas as operações
          upper_left, upper_right, lower_left, lower_right = True
        # 5) borda superior
        elif (y == 0):
          # - somo pixel dentro do canto inferior direito de uma janela
          lower_right = True
          # - subtraio o pixel que tá à esquerda do canto inferior esquerdo de uma janela
          lower_left = True
        # 6) borda inferior
        elif (y == h_img-1):
          # - todas
          upper_left, upper_right, lower_left, lower_right = True

        # 7) borda esquerda
        elif (x == 0):
          # - somo pixel dentro do canto inferior direito de uma janela
          lower_right = True
          # - subtraio o pixel que tá acima do canto superior direito de uma janela
          upper_right = True
        # 8) borda direita
        elif (x == w_img-1):
          # - todas
          upper_left, upper_right, lower_left, lower_right = True
        # 9) não é borda
        else:
          # cap() cuida disso
          upper_left, upper_right, lower_left, lower_right = True

        if lower_right:
          # somo pixel dentro do canto inferior direito de uma janela
          print (img_integral[cap(y+width//2), cap(x+width//2)][c])

          soma = soma + img_integral[cap(y+width//2), cap(x+width//2)][c]

        if upper_right:
          # subtraio o pixel que tá acima do canto superior direito de uma janela
          soma = soma - img_integral[cap(y-width//2-1), cap(x+width//2)][c]
        
        if lower_left:
          # subtraio o pixel que tá à esquerda do canto inferior esquerdo de uma janela
          soma = soma - img_integral[cap(y+width//2), cap(x-width//2-1)][c]
        
        if upper_left:
          # somo de novo o pixel à esquerda e acima da parte esquerda superior de uma janela
          soma = soma + img_integral[cap(y-width//2+1), cap(x-width//2)][c]

        img_blur[y, x, c] = soma/(width*height)


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
    """ 
    # Ingênuo
    img_naive = naive_blur(img, JANELA_W, JANELA_H)
    # cv2.imwrite ('01 - naive-blur.bmp', img_naive*255)
    # imgshow = cv2.imread('01 - naive-blur.bmp')
    # cv2.imshow ('01 - naive-blur', imgshow)
    cv2.imshow ('01 - naive-blur', img_naive)

    print ('naive-blur finalizado.')
    print ('Tempo: %f' % (timeit.default_timer () - start_time))

    # Separável
    img_separable = separable_blur(img, JANELA_W, JANELA_H)
    # cv2.imwrite ('01 - naive-blur.bmp', img_naive*255)
    # imgshow = cv2.imread('01 - naive-blur.bmp')
    # cv2.imshow ('01 - naive-blur', imgshow)
    cv2.imshow ('02 - separable-blur', img_separable)
 """
    print ('separable-blur finalizado.')
    print ('Tempo: %f' % (timeit.default_timer () - start_time))

    # Integral
    img_int = integral_blur(img, JANELA_W, JANELA_H)
    # cv2.imwrite ('01 - naive-blur.bmp', img_naive*255)
    # imgshow = cv2.imread('01 - naive-blur.bmp')
    # cv2.imshow ('01 - naive-blur', imgshow)
    cv2.imshow ('03 - integral-blur', img_int)

    print ('naive-blur finalizado.')
    print ('Tempo: %f' % (timeit.default_timer () - start_time))

    cv2.imshow ('00 - img original', img_out)
    cv2.waitKey ()
    cv2.destroyAllWindows ()

if __name__ == '__main__':
    main ()
    
#===============================================================================

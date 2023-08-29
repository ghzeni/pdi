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

#===============================================================================

INPUT_IMAGE =  'trabalho_1/arroz.bmp'

# TODO: ajuste estes parâmetros!
NEGATIVO = False
THRESHOLD = 0.2
ALTURA_MIN = 1
LARGURA_MIN = 1
N_PIXELS_MIN = 1

#===============================================================================

def binariza (img, threshold):
    # res_img = np.where (img >= threshold, 1, 0)
    # return res_img
    return np.where (img >= threshold, 1, 0)
    # res_img = img

    # for i in img:
    #     for j in img[i]:
    #         if img[i][j] >= threshold:
    #             res_img[i][j] = 1
    #         else:
    #             res_img[i][j] = 0
    
    # return res_img
        

#-------------------------------------------------------------------------------

def rotula (img, largura_min, altura_min, n_pixels_min):
    '''Rotulagem usando flood fill. Marca os objetos da imagem com os valores
[0.1,0.2,etc].

Parâmetros: img: imagem de entrada E saída.
            largura_min: descarta componentes com largura menor que esta.
            altura_min: descarta componentes com altura menor que esta.
            n_pixels_min: descarta componentes com menos pixels que isso.

Valor de retorno: uma lista, onde cada item é um vetor associativo (dictionary)
com os seguintes campos:

'label': rótulo do componente.
'n_pixels': número de pixels do componente.
'T', 'L', 'B', 'R': coordenadas do retângulo envolvente de um componente conexo,
respectivamente: topo, esquerda, baixo e direita.'''

    # TODO: escreva esta função.
    # Use a abordagem com flood fill recursivo.
    # TODO: criar função fill recursiva
    #   ENTRADA: um índice
    #   MARCA QUE ENTROU
    #   COMPARAÇÃO: 

#===============================================================================

def main ():

    # arr = [[0, 0.5, 1][9, 20, 10]]
    # print (binariza(arr, THRESHOLD))

    # Abre a imagem em escala de cinza.
    img = cv2.imread (INPUT_IMAGE)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

    
    # É uma boa prática manter o shape com 3 valores, independente da imagem ser
    # colorida ou não. Também já convertemos para float32.
    img = img.reshape ((img.shape [0], img.shape [1], -1))
    # Converte os valores da imagem de [0, 255] pra [0, 1] sendo 1 = 255
    # (porcentagem)
    img = img.astype (np.float32) / 255

    # Mantém uma cópia colorida para desenhar a saída.
    # img_out = cv2.cvtColor (img, cv2.COLOR_GRAY2BGR)

    # Segmenta a imagem.
    if NEGATIVO:
        img = 1 - img
    img_binarizada = binariza (img, THRESHOLD)
    img_binarizada = img.astype(np.float32)
    img_binarizada /= 255
    cv2.imshow ('01 - binarizada', img_binarizada)
    cv2.imwrite ('01 - binarizada.png', img_binarizada*255)
    cv2.waitKey ()


    start_time = timeit.default_timer ()
    componentes = rotula (img, LARGURA_MIN, ALTURA_MIN, N_PIXELS_MIN)
    n_componentes = len (componentes)
    print ('Tempo: %f' % (timeit.default_timer () - start_time))
    print ('%d componentes detectados.' % n_componentes)

    # Mostra os objetos encontrados.
    for c in componentes:
        cv2.rectangle (img_out, (c ['L'], c ['T']), (c ['R'], c ['B']), (0,0,1))

    cv2.imshow ('02 - out', img_out)
    cv2.imwrite ('02 - out.png', img_out*255)
    cv2.waitKey ()
    cv2.destroyAllWindows ()

if __name__ == '__main__':
    main ()

#===============================================================================

"""
Gera uma imagem sintética 4x4 (BGR) com valores conhecidos,
para permitir conferência manual dos cálculos.

Layout da imagem (linha, coluna) -> (B, G, R):

(0,0) preto puro      (0,1) branco puro     (0,2) azul puro      (0,3) verde puro
(1,0) vermelho puro   (1,1) cinza médio     (1,2) cinza escuro   (1,3) cinza claro
(2,0) valor ímpar p/  (2,1) próximo do 0    (2,2) próximo do 255 (2,3) mistura RGB
      testar arred.
(3,0) mistura RGB 2   (3,1) mistura RGB 3   (3,2) preto quase    (3,3) branco quase
"""
import numpy as np
import cv2

# Matriz 4x4, 3 canais, em ordem BGR (padrão OpenCV)
img = np.array([
    [[0, 0, 0],       [255, 255, 255], [255, 0, 0],     [0, 255, 0]],
    [[0, 0, 255],     [128, 128, 128], [50, 50, 50],    [200, 200, 200]],
    [[10, 20, 31],    [1, 2, 3],       [253, 254, 255], [60, 120, 180]],
    [[90, 30, 200],   [15, 200, 90],   [2, 1, 0],       [254, 255, 253]],
], dtype=np.uint8)

cv2.imwrite("images/input/synthetic.png", img)
print("Imagem sintética criada em images/input/synthetic.png")
print("Shape:", img.shape, "| dtype:", img.dtype)

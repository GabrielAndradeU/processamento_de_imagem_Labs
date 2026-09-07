"""
result_io.py

Responsável apenas por SAÍDA: salvar as imagens processadas em
disco, garantindo que a pasta de destino exista.
"""

import os
import cv2


def garantir_pasta_saida(pasta_saida):
    os.makedirs(pasta_saida, exist_ok=True)


def salvar(pasta_saida, nome_arquivo, img):
    caminho = os.path.join(pasta_saida, nome_arquivo)
    cv2.imwrite(caminho, img)
    print(f"  -> salvo em {caminho}")
    return caminho

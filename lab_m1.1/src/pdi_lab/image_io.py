"""
image_io.py

Responsável apenas por ENTRADA: ler uma imagem do disco e validar
que ela está em condições de ser processada (leitura bem-sucedida,
tipo de dado compatível). A saída (salvar resultados) fica em
result_io.py — separar entrada de saída deixa claro qual módulo
mexe com o quê.
"""

import numpy as np
import cv2

from contract import ImagemInvalidaError, TipoDeImagemIncompativelError


def carregar_imagem(caminho):
    """
    Lê uma imagem do disco com cv2.imread e valida se a leitura
    foi bem-sucedida.

    cv2.imread não lança exceção quando falha: ele retorna None.
    Por isso a verificação explícita é necessária.
    """
    img = cv2.imread(caminho, cv2.IMREAD_UNCHANGED)

    if img is None:
        raise ImagemInvalidaError(
            f"Falha na leitura da imagem: '{caminho}' não existe "
            f"ou não é um arquivo de imagem válido."
        )

    if img.dtype != np.uint8:
        raise TipoDeImagemIncompativelError(
            f"Tipo de imagem incompatível: esperado uint8, "
            f"recebido {img.dtype}."
        )

    return img

"""
test_manual.py

Testes mínimos sobre a imagem sintética 4x4, conforme pedido no
enunciado: conferem cópia exata, ordem dos canais, as duas versões
de escala de cinza, quantidade de níveis após quantização e
comportamento em valores próximos aos limites (0 e 255).

Execução:
    python3 tests/test_manual.py
(a partir da raiz do projeto lab_m1_1/)
"""

import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "pdi_lab"))

from operations import (
    copia_manual,
    separar_canais,
    escala_cinza_media_simples,
    escala_cinza_media_ponderada,
    quantizar,
)

# Mesma matriz usada em create_synthetic.py, em BGR
IMG = np.array([
    [[0, 0, 0],       [255, 255, 255], [255, 0, 0],     [0, 255, 0]],
    [[0, 0, 255],     [128, 128, 128], [50, 50, 50],    [200, 200, 200]],
    [[10, 20, 31],    [1, 2, 3],       [253, 254, 255], [60, 120, 180]],
    [[90, 30, 200],   [15, 200, 90],   [2, 1, 0],       [254, 255, 253]],
], dtype=np.uint8)


def teste_copia_exata():
    copia = copia_manual(IMG)
    assert np.array_equal(copia, IMG), "Cópia difere do original"
    assert copia is not IMG, "Cópia não pode ser a mesma referência de memória"
    print("OK: copia_manual é numericamente idêntica e é um objeto novo")


def teste_ordem_dos_canais():
    canais = separar_canais(IMG)

    # pixel (0,2) é azul puro em BGR: (255, 0, 0)
    assert tuple(canais["b"][0, 2]) == (255, 0, 0)
    assert tuple(canais["g"][0, 2]) == (0, 0, 0)
    assert tuple(canais["r"][0, 2]) == (0, 0, 0)

    # pixel (1,0) é vermelho puro em BGR: (0, 0, 255)
    assert tuple(canais["r"][1, 0]) == (0, 0, 255)
    assert tuple(canais["b"][1, 0]) == (0, 0, 0)
    assert tuple(canais["g"][1, 0]) == (0, 0, 0)

    print("OK: ordem dos canais (BGR) confere com o esperado")


def teste_escala_cinza_valor_conhecido():
    # pixel (1,1) = (B,G,R) = (128,128,128) -> cinza deve ser 128
    # em ambas as versões (média simples e ponderada), pois R=G=B
    simples = escala_cinza_media_simples(IMG)
    ponderada = escala_cinza_media_ponderada(IMG)

    assert simples[1, 1] == 128
    assert ponderada[1, 1] == 128

    # pixel (0,0) = (0,0,0) -> cinza 0 em ambas
    assert simples[0, 0] == 0
    assert ponderada[0, 0] == 0

    # pixel (0,1) = (255,255,255) -> cinza 255 em ambas
    assert simples[0, 1] == 255
    assert ponderada[0, 1] == 255

    # pixel (1,3) = (200,200,200) -> cinza 200 em ambas
    assert simples[1, 3] == 200
    assert ponderada[1, 3] == 200

    # pixel (0,2) = B=255,G=0,R=0 (azul puro)
    # media simples: (0+0+255)/3 = 85
    # media ponderada: 0.299*0 + 0.587*0 + 0.114*255 = 29.07 -> round = 29
    assert simples[0, 2] == 85, f"esperado 85, obtido {simples[0,2]}"
    assert ponderada[0, 2] == 29, f"esperado 29, obtido {ponderada[0,2]}"

    print("OK: valores de escala de cinza conferem com o cálculo manual")


def teste_diferenca_entre_versoes_de_cinza():
    simples = escala_cinza_media_simples(IMG)
    ponderada = escala_cinza_media_ponderada(IMG)

    # nos pixels em que R=G=B, as duas versões devem ser IGUAIS
    assert simples[1, 1] == ponderada[1, 1]

    # no pixel azul puro (0,2), as versões devem DIFERIR
    # (a ponderada dá menos peso ao azul)
    assert simples[0, 2] != ponderada[0, 2]

    print("OK: diferença entre médias simples e ponderada confere com o esperado")


def teste_quantidade_de_niveis():
    cinza = escala_cinza_media_ponderada(IMG)

    for niveis in (16, 8, 4, 2):
        quantizada = quantizar(cinza, niveis)
        valores_unicos = np.unique(quantizada)
        assert len(valores_unicos) <= niveis, (
            f"quantizar com niveis={niveis} gerou "
            f"{len(valores_unicos)} valores únicos"
        )

    print("OK: quantidade de níveis após quantização respeita o limite pedido")


def teste_limites_quantizacao():
    cinza = escala_cinza_media_ponderada(IMG)
    quant2 = quantizar(cinza, 2)

    # com 2 níveis, os únicos valores possíveis devem ser 0 e 255
    valores_unicos = set(np.unique(quant2).tolist())
    assert valores_unicos.issubset({0, 255}), (
        f"quantizar com niveis=2 gerou valores fora de {{0, 255}}: {valores_unicos}"
    )

    print("OK: quantização com 2 níveis usa apenas 0 e 255")


def teste_niveis_invalido():
    cinza = escala_cinza_media_ponderada(IMG)
    try:
        quantizar(cinza, 1)
        assert False, "deveria ter levantado erro para niveis=1"
    except Exception:
        print("OK: quantidade de níveis inválida levanta erro corretamente")


if __name__ == "__main__":
    teste_copia_exata()
    teste_ordem_dos_canais()
    teste_escala_cinza_valor_conhecido()
    teste_diferenca_entre_versoes_de_cinza()
    teste_quantidade_de_niveis()
    teste_limites_quantizacao()
    teste_niveis_invalido()
    print("\nTodos os testes passaram.")

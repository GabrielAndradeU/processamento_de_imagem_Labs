"""
operations.py

Implementação manual das operações de processamento de imagem
pedidas no Laboratório M1.1.

Regra do laboratório: nenhuma função pronta de cópia, separação de
canais, conversão para cinza ou quantização pode ser usada. Todo o
processamento pixel a pixel é feito manualmente com loops explícitos.

Bibliotecas usadas apenas para: criação de matrizes (np.zeros) e
acesso a pixels (indexação numpy). Leitura/escrita ficam em
image_io.py / result_io.py.
"""

import numpy as np

from contract import NumeroDeCanaisInesperadoError, QuantidadeDeNiveisInvalidaError
from parameters import PESO_R, PESO_G, PESO_B, VALOR_MINIMO_VALIDO, VALOR_MAXIMO_VALIDO


def _clamp(valor):
    """Limita um valor ao intervalo válido [0, 255]."""
    return max(VALOR_MINIMO_VALIDO, min(VALOR_MAXIMO_VALIDO, valor))


def validar_canais(img, esperado=(1, 3)):
    """
    Verifica se a imagem tem um número de canais suportado pelas
    operações deste laboratório.

    esperado: tupla com as quantidades de canais aceitas.
      - 1 canal  -> imagem em níveis de cinza
      - 3 canais -> imagem colorida (BGR)
    """
    if img.ndim == 2:
        canais = 1
    elif img.ndim == 3:
        canais = img.shape[2]
    else:
        raise NumeroDeCanaisInesperadoError(
            f"Número inesperado de dimensões: {img.ndim}."
        )

    if canais not in esperado:
        raise NumeroDeCanaisInesperadoError(
            f"Número inesperado de canais: {canais}. "
            f"Esperado um de {esperado}."
        )

    return canais


# ---------------------------------------------------------------------
# 1. Inspeção da imagem
# ---------------------------------------------------------------------

def inspecionar_imagem(img):
    """
    Retorna um dicionário com largura, altura, canais, tipo,
    quantidade de pixels, mínimo, máximo e média (por canal, se
    colorida). Percurso manual, pixel a pixel.
    """
    canais = validar_canais(img)
    altura, largura = img.shape[0], img.shape[1]
    total_pixels = altura * largura

    info = {
        "largura": largura,
        "altura": altura,
        "canais": canais,
        "tipo": str(img.dtype),
        "quantidade_pixels": total_pixels,
    }

    if canais == 1:
        minimo = 255
        maximo = 0
        soma = 0
        for y in range(altura):
            for x in range(largura):
                valor = int(img[y, x])
                if valor < minimo:
                    minimo = valor
                if valor > maximo:
                    maximo = valor
                soma += valor
        info["minimo"] = minimo
        info["maximo"] = maximo
        info["media"] = soma / total_pixels

    else:
        minimos = [255] * canais
        maximos = [0] * canais
        somas = [0] * canais

        for y in range(altura):
            for x in range(largura):
                for c in range(canais):
                    valor = int(img[y, x, c])
                    if valor < minimos[c]:
                        minimos[c] = valor
                    if valor > maximos[c]:
                        maximos[c] = valor
                    somas[c] += valor

        nomes_canais = ["B", "G", "R"] if canais == 3 else [f"C{c}" for c in range(canais)]
        info["minimo_por_canal"] = dict(zip(nomes_canais, minimos))
        info["maximo_por_canal"] = dict(zip(nomes_canais, maximos))
        info["media_por_canal"] = {
            nomes_canais[c]: somas[c] / total_pixels for c in range(canais)
        }

    return info


def imprimir_inspecao(info):
    """Imprime o dicionário de inspecionar_imagem de forma legível."""
    print(f"Largura: {info['largura']}")
    print(f"Altura: {info['altura']}")
    print(f"Canais: {info['canais']}")
    print(f"Tipo: {info['tipo']}")
    print(f"Quantidade de pixels: {info['quantidade_pixels']}")

    if "minimo" in info:
        print(f"Mínimo: {info['minimo']}")
        print(f"Máximo: {info['maximo']}")
        print(f"Média: {info['media']:.4f}")
    else:
        print(f"Mínimo por canal: {info['minimo_por_canal']}")
        print(f"Máximo por canal: {info['maximo_por_canal']}")
        print("Média por canal:", {
            k: round(v, 4) for k, v in info["media_por_canal"].items()
        })


# ---------------------------------------------------------------------
# 2. Cópia manual
# ---------------------------------------------------------------------

def copia_manual(img):
    """Cria uma nova imagem e copia pixel a pixel (sem img.copy())."""
    canais = validar_canais(img)
    altura, largura = img.shape[0], img.shape[1]

    if canais == 1:
        saida = np.zeros((altura, largura), dtype=img.dtype)
        for y in range(altura):
            for x in range(largura):
                saida[y, x] = img[y, x]
    else:
        saida = np.zeros((altura, largura, canais), dtype=img.dtype)
        for y in range(altura):
            for x in range(largura):
                for c in range(canais):
                    saida[y, x, c] = img[y, x, c]

    return saida


# ---------------------------------------------------------------------
# 3. Separação manual dos canais
# ---------------------------------------------------------------------

def separar_canais(img):
    """
    Retorna {"b": img_b, "g": img_g, "r": img_r}, cada uma
    preservando apenas o canal correspondente e zerando os demais.
    """
    canais = validar_canais(img, esperado=(3,))
    altura, largura = img.shape[0], img.shape[1]

    img_b = np.zeros((altura, largura, canais), dtype=img.dtype)
    img_g = np.zeros((altura, largura, canais), dtype=img.dtype)
    img_r = np.zeros((altura, largura, canais), dtype=img.dtype)

    # índices no OpenCV: 0 = B, 1 = G, 2 = R
    for y in range(altura):
        for x in range(largura):
            b = img[y, x, 0]
            g = img[y, x, 1]
            r = img[y, x, 2]

            img_b[y, x, 0] = b
            img_g[y, x, 1] = g
            img_r[y, x, 2] = r

    return {"b": img_b, "g": img_g, "r": img_r}


# ---------------------------------------------------------------------
# 4. Conversão manual para níveis de cinza
# ---------------------------------------------------------------------

def escala_cinza_media_simples(img):
    """g = (R + G + B) / 3, com arredondamento e clamp para [0, 255]."""
    validar_canais(img, esperado=(3,))
    altura, largura = img.shape[0], img.shape[1]
    saida = np.zeros((altura, largura), dtype=np.uint8)

    for y in range(altura):
        for x in range(largura):
            b = int(img[y, x, 0])
            g = int(img[y, x, 1])
            r = int(img[y, x, 2])

            valor = round((r + g + b) / 3.0)
            saida[y, x] = _clamp(valor)

    return saida


def escala_cinza_media_ponderada(img):
    """g = 0.299*R + 0.587*G + 0.114*B, com arredondamento e clamp."""
    validar_canais(img, esperado=(3,))
    altura, largura = img.shape[0], img.shape[1]
    saida = np.zeros((altura, largura), dtype=np.uint8)

    for y in range(altura):
        for x in range(largura):
            b = int(img[y, x, 0])
            g = int(img[y, x, 1])
            r = int(img[y, x, 2])

            valor = round(PESO_R * r + PESO_G * g + PESO_B * b)
            saida[y, x] = _clamp(valor)

    return saida


# ---------------------------------------------------------------------
# 5. Quantização
# ---------------------------------------------------------------------

def quantizar(img_cinza, niveis):
    """
    Reduz uma imagem em níveis de cinza (0-255) para `niveis` faixas
    iguais, mapeando cada faixa para um representante reescalado de
    volta a [0, 255].
    """
    if niveis < 2 or niveis > 256:
        raise QuantidadeDeNiveisInvalidaError(
            f"Quantidade de níveis inválida: {niveis}. "
            f"Deve ser um inteiro entre 2 e 256."
        )

    validar_canais(img_cinza, esperado=(1,))
    altura, largura = img_cinza.shape[0], img_cinza.shape[1]
    saida = np.zeros((altura, largura), dtype=np.uint8)

    tamanho_faixa = 256 / niveis

    for y in range(altura):
        for x in range(largura):
            valor = int(img_cinza[y, x])

            indice_faixa = int(valor / tamanho_faixa)
            if indice_faixa >= niveis:  # guarda para valor == 255
                indice_faixa = niveis - 1

            representante = round(indice_faixa * 255 / (niveis - 1)) if niveis > 1 else 0
            saida[y, x] = _clamp(representante)

    return saida

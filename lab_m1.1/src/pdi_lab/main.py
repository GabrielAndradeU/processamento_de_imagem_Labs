"""
main.py

Executa todas as atividades do Laboratório M1.1 sobre uma imagem
de entrada e salva os resultados em images/output/.

Uso:
    python src/pdi_lab/main.py images/input/sua_foto.png

Se nenhum caminho for passado, usa a imagem sintética de teste
em images/input/synthetic.png.
"""

import sys
import os
import cv2

from operations import (
    carregar_imagem,
    inspecionar_imagem,
    imprimir_inspecao,
    copia_manual,
    separar_canais,
    escala_cinza_media_simples,
    escala_cinza_media_ponderada,
    quantizar,
    ImagemInvalidaError,
    QuantidadeDeNiveisInvalidaError,
)

PASTA_SAIDA = "images/output"


def garantir_pasta_saida():
    os.makedirs(PASTA_SAIDA, exist_ok=True)


def salvar(nome_arquivo, img):
    caminho = os.path.join(PASTA_SAIDA, nome_arquivo)
    cv2.imwrite(caminho, img)
    print(f"  -> salvo em {caminho}")


def main():
    caminho_entrada = (
        sys.argv[1] if len(sys.argv) > 1 else "images/input/synthetic.png"
    )

    garantir_pasta_saida()

    print(f"Carregando imagem: {caminho_entrada}")
    try:
        img = carregar_imagem(caminho_entrada)
    except ImagemInvalidaError as e:
        print(f"ERRO: {e}")
        sys.exit(1)

    # ---------------- 1. Inspeção ----------------
    print("\n=== 1. Inspeção da imagem ===")
    info = inspecionar_imagem(img)
    imprimir_inspecao(info)

    # ---------------- 2. Cópia manual ----------------
    print("\n=== 2. Cópia manual ===")
    copia = copia_manual(img)
    diferenca_maxima = int((img.astype(int) - copia.astype(int)).__abs__().max())
    print(f"Diferença máxima entre original e cópia: {diferenca_maxima}")
    salvar("copy.png", copia)

    # ---------------- 3. Separação de canais ----------------
    # Só faz sentido para imagem colorida (3 canais)
    if info["canais"] == 3:
        print("\n=== 3. Separação manual dos canais ===")
        canais = separar_canais(img)
        salvar("channel_b.png", canais["b"])
        salvar("channel_g.png", canais["g"])
        salvar("channel_r.png", canais["r"])

        # ---------------- 4. Escala de cinza ----------------
        print("\n=== 4. Conversão manual para níveis de cinza ===")
        cinza_simples = escala_cinza_media_simples(img)
        cinza_ponderada = escala_cinza_media_ponderada(img)
        salvar("gray_average.png", cinza_simples)
        salvar("gray_weighted.png", cinza_ponderada)

        diff_medio = abs(
            cinza_simples.astype(int) - cinza_ponderada.astype(int)
        ).mean()
        print(f"Diferença média entre as duas versões de cinza: {diff_medio:.4f}")

    else:
        print("\nImagem já está em níveis de cinza — pulando itens 3 e 4.")
        cinza_ponderada = img if img.ndim == 2 else img[:, :, 0]

    # ---------------- 5. Quantização ----------------
    print("\n=== 5. Quantização ===")
    for niveis in (16, 8, 4, 2):
        try:
            quantizada = quantizar(cinza_ponderada, niveis)
            salvar(f"quant_{niveis}.png", quantizada)
        except QuantidadeDeNiveisInvalidaError as e:
            print(f"ERRO: {e}")

    print("\nProcessamento concluído.")


if __name__ == "__main__":
    main()

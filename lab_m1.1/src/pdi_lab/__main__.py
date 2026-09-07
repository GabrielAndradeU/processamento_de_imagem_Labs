"""
__main__.py

Orquestra a execução das 5 atividades sobre uma imagem de entrada
e salva os resultados. Permite rodar com:

    python -m pdi_lab
    python -m pdi_lab images/input/foto.png
    python src/pdi_lab/__main__.py
"""

import sys

from cli import parse_args
from contract import ImagemInvalidaError, QuantidadeDeNiveisInvalidaError
from image_io import carregar_imagem
from result_io import garantir_pasta_saida, salvar
from parameters import NIVEIS_QUANTIZACAO_PADRAO
from operations import (
    inspecionar_imagem,
    imprimir_inspecao,
    copia_manual,
    separar_canais,
    escala_cinza_media_simples,
    escala_cinza_media_ponderada,
    quantizar,
)


def main(argv=None):
    args = parse_args(argv)
    garantir_pasta_saida(args.saida)

    print(f"Carregando imagem: {args.caminho_entrada}")
    try:
        img = carregar_imagem(args.caminho_entrada)
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
    diferenca_maxima = int(abs(img.astype(int) - copia.astype(int)).max())
    print(f"Diferença máxima entre original e cópia: {diferenca_maxima}")
    salvar(args.saida, "copy.png", copia)

    # ---------------- 3 e 4. Canais e escala de cinza ----------------
    if info["canais"] == 3:
        print("\n=== 3. Separação manual dos canais ===")
        canais = separar_canais(img)
        salvar(args.saida, "channel_b.png", canais["b"])
        salvar(args.saida, "channel_g.png", canais["g"])
        salvar(args.saida, "channel_r.png", canais["r"])

        print("\n=== 4. Conversão manual para níveis de cinza ===")
        cinza_simples = escala_cinza_media_simples(img)
        cinza_ponderada = escala_cinza_media_ponderada(img)
        salvar(args.saida, "gray_average.png", cinza_simples)
        salvar(args.saida, "gray_weighted.png", cinza_ponderada)

        diff_medio = abs(cinza_simples.astype(int) - cinza_ponderada.astype(int)).mean()
        print(f"Diferença média entre as duas versões de cinza: {diff_medio:.4f}")
    else:
        print("\nImagem já está em níveis de cinza — pulando itens 3 e 4.")
        cinza_ponderada = img if img.ndim == 2 else img[:, :, 0]

    # ---------------- 5. Quantização ----------------
    print("\n=== 5. Quantização ===")
    for niveis in NIVEIS_QUANTIZACAO_PADRAO:
        try:
            quantizada = quantizar(cinza_ponderada, niveis)
            salvar(args.saida, f"quant_{niveis}.png", quantizada)
        except QuantidadeDeNiveisInvalidaError as e:
            print(f"ERRO: {e}")

    print("\nProcessamento concluído.")


if __name__ == "__main__":
    main()

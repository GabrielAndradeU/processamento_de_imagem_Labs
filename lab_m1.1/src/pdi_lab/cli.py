"""
cli.py

Responsável apenas por interpretar os argumentos de linha de
comando. Mantém __main__.py livre de lógica de parsing.
"""

import argparse


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Laboratório M1.1 — Processamento de Imagens"
    )
    parser.add_argument(
        "caminho_entrada",
        nargs="?",
        default="images/input/synthetic.png",
        help="Caminho da imagem de entrada (padrão: imagem sintética de teste)",
    )
    parser.add_argument(
        "--saida",
        default="images/output",
        help="Pasta onde salvar as imagens de saída (padrão: images/output)",
    )
    parser.add_argument(
        "--resultados",
        default="results",
        help="Pasta onde salvar os dados numéricos em CSV (padrão: results)",
    )
    return parser.parse_args(argv)
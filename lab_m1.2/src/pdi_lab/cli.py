import argparse

from .contract import validate_operation
from .image_io import read_image
from .operations import (
    brightness,
    contrast,
    negative,
    threshold,
    histogram,
)
from .parameters import (
    validate_brightness,
    validate_alpha,
    validate_threshold,
)
from .result_io import (
    save_result_image,
    save_histogram,
)


def create_parser():
    parser = argparse.ArgumentParser(
        description=(
            "Laboratorio M1.2 - Transformacoes "
            "de intensidade em imagens em niveis de cinza."
        )
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Caminho da imagem de entrada."
    )

    parser.add_argument(
        "--output",
        required=True,
        help=(
            "Caminho do arquivo de imagem ou "
            "CSV de saida."
        )
    )

    parser.add_argument(
        "--operation",
        required=True,
        choices=[
            "brightness",
            "contrast",
            "negative",
            "threshold",
            "histogram",
        ],
        help="Operacao a ser executada."
    )

    parser.add_argument(
        "--value",
        type=int,
        help="Valor usado na operacao de brilho."
    )

    parser.add_argument(
        "--alpha",
        type=float,
        help="Fator usado na operacao de contraste."
    )

    parser.add_argument(
        "--threshold",
        type=int,
        help="Limiar usado na limiarizacao."
    )

    return parser


def execute(args):
    operation = validate_operation(args.operation)

    image = read_image(args.input)

    if operation == "brightness":
        if args.value is None:
            raise ValueError(
                "A operacao brightness exige --value."
            )

        value = validate_brightness(args.value)

        result = brightness(image, value)

        save_result_image(args.output, result)

    elif operation == "contrast":
        if args.alpha is None:
            raise ValueError(
                "A operacao contrast exige --alpha."
            )

        alpha = validate_alpha(args.alpha)

        result = contrast(image, alpha)

        save_result_image(args.output, result)

    elif operation == "negative":
        result = negative(image)

        save_result_image(args.output, result)

    elif operation == "threshold":
        if args.threshold is None:
            raise ValueError(
                "A operacao threshold exige --threshold."
            )

        threshold_value = validate_threshold(
            args.threshold
        )

        result = threshold(
            image,
            threshold_value
        )

        save_result_image(args.output, result)

    elif operation == "histogram":
        result = histogram(image)

        save_histogram(args.output, result)


def main():
    parser = create_parser()

    args = parser.parse_args()

    try:
        execute(args)

    except Exception as error:
        parser.error(str(error))
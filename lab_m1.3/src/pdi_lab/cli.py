import argparse

import numpy as np

from .image_io import read_image
from .operations import (
    convolution_image,
    mean_filter,
    weighted_mean,
    laplacian,
    laplacian_enhance,
    sobel_gx,
    sobel_gy,
    sobel_magnitude_approx,
    sobel_magnitude_euclidean,
)
from .parameters import (
    validate_kernel,
    validate_border,
)
from .result_io import save_result_image


def create_parser():
    parser = argparse.ArgumentParser(
        description=(
            "Laboratorio M1.3 - "
            "Convolucao e filtragem espacial."
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
        help="Caminho da imagem de saída."
    )

    parser.add_argument(
        "--operation",
        required=True,
        choices=[
            "convolution",
            "mean_filter",
            "weighted_mean",
            "laplacian",
            "laplacian_enhance",
            "sobel_gx",
            "sobel_gy",
            "sobel_approx",
            "sobel_euclidean",
        ],
        help="Operacao a ser executada."
    )

    parser.add_argument(
        "--kernel",
        help="Arquivo contendo o kernel."
    )

    parser.add_argument(
        "--size",
        type=int,
        choices=[3, 5],
        help="Tamanho do filtro de média."
    )

    parser.add_argument(
        "--border",
        default="copy",
        choices=[
            "copy",
            "replicate",
        ],
        help="Estrategia de tratamento das bordas."
    )

    return parser


def load_kernel(path):
    try:
        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            lines = [
                line.strip()
                for line in file
                if line.strip()
            ]

    except OSError:
        raise ValueError(
            f"Não foi possível abrir o kernel: {path}"
        )

    if not lines:
        raise ValueError(
            "O arquivo do kernel está vazio."
        )

    first = lines[0].split()

    if len(first) != 2:
        raise ValueError(
            "A primeira linha deve informar linhas e colunas."
        )

    try:
        rows = int(first[0])
        cols = int(first[1])
    except ValueError:
        raise ValueError(
            "As dimensões do kernel devem ser inteiras."
        )

    if rows <= 0 or cols <= 0:
        raise ValueError(
            "As dimensões do kernel devem ser positivas."
        )

    values = []

    for line in lines[1:]:
        parts = line.split()

        if len(parts) != cols:
            raise ValueError(
                "Quantidade inválida de valores no kernel."
            )

        try:
            values.append(
                [float(value) for value in parts]
            )
        except ValueError:
            raise ValueError(
                "O kernel contém valor inválido."
            )

    if len(values) != rows:
        raise ValueError(
            "Quantidade inválida de linhas no kernel."
        )

    kernel = np.array(
        values,
        dtype=float
    )

    return validate_kernel(kernel)


def execute(args):
    image = read_image(
        args.input
    )

    border = validate_border(
        args.border
    )

    if args.operation == "convolution":

        if args.kernel is None:
            raise ValueError(
                "convolution exige --kernel."
            )

        kernel = load_kernel(
            args.kernel
        )

        result = convolution_image(
            image,
            kernel,
            border
        )

    elif args.operation == "mean_filter":

        if args.size is None:
            raise ValueError(
                "mean_filter exige --size."
            )

        result = mean_filter(
            image,
            args.size,
            border
        )

    elif args.operation == "weighted_mean":

        result = weighted_mean(
            image,
            border
        )

    elif args.operation == "laplacian":

        response = laplacian(
            image,
            border
        )

        result = np.zeros_like(
            image,
            dtype=np.uint8
        )

        height, width = image.shape

        for y in range(height):
            for x in range(width):
                value = abs(
                    response[y, x]
                )

                if value > 255:
                    value = 255

                result[y, x] = int(
                    round(value)
                )

    elif args.operation == "laplacian_enhance":

        result = laplacian_enhance(
            image,
            border
        )

    elif args.operation == "sobel_gx":

        response = sobel_gx(
            image,
            border
        )

        result = np.zeros_like(
            image,
            dtype=np.uint8
        )

        height, width = image.shape

        for y in range(height):
            for x in range(width):
                value = abs(
                    response[y, x]
                )

                if value > 255:
                    value = 255

                result[y, x] = int(
                    round(value)
                )

    elif args.operation == "sobel_gy":

        response = sobel_gy(
            image,
            border
        )

        result = np.zeros_like(
            image,
            dtype=np.uint8
        )

        height, width = image.shape

        for y in range(height):
            for x in range(width):
                value = abs(
                    response[y, x]
                )

                if value > 255:
                    value = 255

                result[y, x] = int(
                    round(value)
                )

    elif args.operation == "sobel_approx":

        result = sobel_magnitude_approx(
            image,
            border
        )

    elif args.operation == "sobel_euclidean":

        result = sobel_magnitude_euclidean(
            image,
            border
        )

    else:
        raise ValueError(
            f"Operação inválida: {args.operation}"
        )

    save_result_image(
        args.output,
        result
    )


def main():
    parser = create_parser()

    args = parser.parse_args()

    try:
        execute(args)

    except Exception as error:
        parser.error(
            str(error)
        )
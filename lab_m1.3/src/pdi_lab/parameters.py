import numpy as np


def validate_kernel(kernel):
    if kernel is None:
        raise ValueError("O kernel não pode ser vazio.")

    kernel = np.asarray(kernel, dtype=float)

    if kernel.size == 0:
        raise ValueError("O kernel não pode ser vazio.")

    if kernel.ndim != 2:
        raise ValueError(
            "O kernel deve ser uma matriz."
        )

    rows, cols = kernel.shape

    if rows != cols:
        raise ValueError(
            "O kernel deve ser quadrado."
        )

    if rows % 2 == 0:
        raise ValueError(
            "O kernel deve possuir dimensão ímpar."
        )

    return kernel


def validate_border(border):
    valid = ["copy", "replicate"]

    if border not in valid:
        raise ValueError(
            "A estratégia de borda deve ser "
            "'copy' ou 'replicate'."
        )

    return border
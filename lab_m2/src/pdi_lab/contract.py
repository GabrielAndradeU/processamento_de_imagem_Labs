
import numpy as np


def validate_binary_mask(mask: np.ndarray) -> None:
    if not isinstance(mask, np.ndarray):
        raise TypeError("A máscara deve ser um array NumPy.")

    if mask.ndim != 2:
        raise ValueError("A máscara deve possuir apenas um canal.")

    if mask.size == 0:
        raise ValueError("A máscara não pode estar vazia.")

    values = np.unique(mask)

    if not np.all(np.isin(values, [0, 255])):
        raise ValueError("A máscara deve conter apenas valores 0 e 255.")


def validate_mask_dimensions(
    mask: np.ndarray,
    image: np.ndarray
) -> None:
    if mask.shape != image.shape[:2]:
        raise ValueError(
            "As dimensões da máscara devem corresponder às da imagem."
        )
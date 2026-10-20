from pathlib import Path

import cv2
import numpy as np


def load_image(path: str | Path) -> np.ndarray:
    image_path = Path(path)

    if not image_path.is_file():
        raise FileNotFoundError(
            f"Arquivo de imagem não encontrado: {image_path}"
        )

    image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError(
            f"Não foi possível abrir a imagem: {image_path}"
        )

    return image


def to_grayscale(image: np.ndarray) -> np.ndarray:
    if not isinstance(image, np.ndarray) or image.size == 0:
        raise ValueError("A imagem fornecida é inválida.")

    if image.ndim == 2:
        return image.copy()

    if image.ndim == 3 and image.shape[2] == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    raise ValueError(
        "A imagem deve estar em escala de cinza ou possuir três canais BGR."
    )

def invert_binary_mask(mask: np.ndarray) -> np.ndarray:
    from pdi_lab.contract import validate_binary_mask

    validate_binary_mask(mask)
    return cv2.bitwise_not(mask)

def load_mask(path: str | Path) -> np.ndarray:
    image_path = Path(path)

    if not image_path.is_file():
        raise FileNotFoundError(
            f"Arquivo de máscara não encontrado: {image_path}"
        )

    mask = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)

    if mask is None:
        raise ValueError(
            f"Não foi possível abrir a máscara: {image_path}"
        )

    from pdi_lab.contract import validate_binary_mask
    validate_binary_mask(mask)

    return mask
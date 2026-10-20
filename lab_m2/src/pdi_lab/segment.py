import cv2
import numpy as np

from pdi_lab.contract import (
    validate_binary_mask,
    validate_mask_dimensions,
)
from pdi_lab.image_io import to_grayscale
from pdi_lab.parameters import (
    validate_adaptive_parameters,
    validate_fixed_threshold,
    validate_method,
)


def segment_image(
    image: np.ndarray,
    method: str = "fixed",
    threshold: int = 120,
    block_size: int = 21,
    constant: float = 5
) -> np.ndarray:
    validate_method(method)

    gray = to_grayscale(image)

    if method == "fixed":
        validate_fixed_threshold(threshold)

        _, mask = cv2.threshold(
            gray,
            threshold,
            255,
            cv2.THRESH_BINARY
        )

    elif method == "adaptive":
        validate_adaptive_parameters(block_size, constant)

        if min(gray.shape) < block_size:
            raise ValueError(
                "O tamanho do bloco adaptativo não pode ser maior "
                "que a menor dimensão da imagem."
            )

        mask = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            block_size,
            constant
        )

    else:
        raise ValueError(f"Método não suportado: {method}")

    validate_binary_mask(mask)
    validate_mask_dimensions(mask, image)

    return mask
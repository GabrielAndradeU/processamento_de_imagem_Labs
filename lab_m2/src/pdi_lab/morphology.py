
from pathlib import Path

import cv2
import numpy as np

from pdi_lab.contract import validate_binary_mask
from pdi_lab.result_io import save_mask


def apply_morphology(
    mask: np.ndarray,
    output_dir: str | Path,
    kernel_size: int = 3,
    min_area: int = 20,
) -> dict[str, np.ndarray]:
    validate_binary_mask(mask)

    if kernel_size < 1 or kernel_size % 2 == 0:
        raise ValueError("O tamanho do kernel deve ser ímpar e maior que zero.")

    if min_area < 0:
        raise ValueError("A área mínima não pode ser negativa.")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (kernel_size, kernel_size),
    )

    # Etapa 1: fechamento para preencher pequenos buracos e unir pequenas lacunas.
    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Etapa 2: abertura para remover pequenos ruídos brancos.
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)

    save_mask(closing, output_path / "stage_closing.png")
    save_mask(opening, output_path / "stage_opening.png")

    return {
        "initial": mask.copy(),
        "closing": closing,
        "opening": opening,
    }

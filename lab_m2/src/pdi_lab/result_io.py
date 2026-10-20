from pathlib import Path

import cv2
import numpy as np

from pdi_lab.contract import validate_binary_mask


def save_mask(mask: np.ndarray, path: str | Path) -> None:
    validate_binary_mask(mask)

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.suffix.lower() != ".png":
        raise ValueError("A máscara deve ser salva em formato PNG.")

    success = cv2.imwrite(str(output_path), mask)

    if not success:
        raise OSError(f"Não foi possível salvar a máscara: {output_path}")


def calculate_mask_statistics(mask: np.ndarray) -> dict[str, float | int]:
    validate_binary_mask(mask)

    total_pixels = int(mask.size)
    foreground_pixels = int(np.count_nonzero(mask == 255))
    background_pixels = total_pixels - foreground_pixels
    foreground_percentage = foreground_pixels / total_pixels * 100

    return {
        "total_pixels": total_pixels,
        "foreground_pixels": foreground_pixels,
        "background_pixels": background_pixels,
        "foreground_percentage": foreground_percentage,
    }
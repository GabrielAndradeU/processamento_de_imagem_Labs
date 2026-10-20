
import csv
from pathlib import Path

import cv2
import numpy as np

from pdi_lab.contract import validate_binary_mask


def label_components(
    mask: np.ndarray,
    connectivity: int = 8,
) -> tuple[int, np.ndarray, list[dict[str, int | float]]]:
    validate_binary_mask(mask)

    if connectivity not in (4, 8):
        raise ValueError("A conectividade deve ser 4 ou 8.")

    count, labels, stats, centroids = cv2.connectedComponentsWithStats(
        mask,
        connectivity=connectivity,
        ltype=cv2.CV_32S,
    )

    components = []

    # O rótulo 0 representa o fundo, por isso começamos em 1.
    for label in range(1, count):
        x = int(stats[label, cv2.CC_STAT_LEFT])
        y = int(stats[label, cv2.CC_STAT_TOP])
        width = int(stats[label, cv2.CC_STAT_WIDTH])
        height = int(stats[label, cv2.CC_STAT_HEIGHT])
        area = int(stats[label, cv2.CC_STAT_AREA])
        cx = float(centroids[label, 0])
        cy = float(centroids[label, 1])

        components.append({
            "label": label,
            "area": area,
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "cx": cx,
            "cy": cy,
        })

    return len(components), labels, components


def save_components_csv(
    components: list[dict[str, int | float]],
    path: str | Path,
    min_area: int = 0,
) -> None:
    if min_area < 0:
        raise ValueError("A área mínima não pode ser negativa.")

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    columns = [
        "label",
        "area",
        "x",
        "y",
        "width",
        "height",
        "cx",
        "cy",
        "kept",
    ]

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()

        for component in components:
            row = dict(component)
            row["kept"] = int(component["area"] >= min_area)
            writer.writerow(row)


def draw_component_boxes(
    mask: np.ndarray,
    components: list[dict[str, int | float]],
    min_area: int = 0,
) -> np.ndarray:
    validate_binary_mask(mask)

    if min_area < 0:
        raise ValueError("A área mínima não pode ser negativa.")

    image = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    for component in components:
        if component["area"] < min_area:
            continue

        x = int(component["x"])
        y = int(component["y"])
        width = int(component["width"])
        height = int(component["height"])

        cv2.rectangle(
            image,
            (x, y),
            (x + width - 1, y + height - 1),
            (0, 0, 255),
            1,
        )

        cv2.putText(
            image,
            str(component["label"]),
            (x, max(y - 4, 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.35,
            (0, 0, 255),
            1,
            cv2.LINE_AA,
        )

    return image

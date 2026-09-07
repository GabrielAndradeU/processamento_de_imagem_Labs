import csv
from pathlib import Path

import cv2
import numpy as np


def save_result_image(path, image):
    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if not isinstance(image, np.ndarray):
        raise ValueError(
            "O resultado deve ser um numpy.ndarray."
        )

    image = np.asarray(
        image,
        dtype=np.uint8
    )

    success = cv2.imwrite(
        str(path),
        image
    )

    if not success:
        raise ValueError(
            f"Não foi possível salvar a imagem: {path}"
        )


def save_histogram(path, histogram):
    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if len(histogram) != 256:
        raise ValueError(
            "O histograma deve possuir 256 posições."
        )

    with open(
        path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            ["intensity", "count"]
        )

        for intensity in range(256):
            writer.writerow(
                [
                    intensity,
                    int(histogram[intensity])
                ]
            )
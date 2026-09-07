import csv
from pathlib import Path

from .image_io import save_image


def save_result_image(path, image):
    save_image(path, image)


def save_histogram(path, histogram_data):
    path = Path(path)

    path.parent.mkdir(parents=True, exist_ok=True)

    if len(histogram_data) != 256:
        raise ValueError(
            "O histograma deve possuir exatamente 256 posicoes."
        )

    with path.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow(["intensity", "count"])

        for intensity in range(256):
            writer.writerow([
                intensity,
                histogram_data[intensity]
            ])
from pathlib import Path

import cv2


def read_image(path):
    path = Path(path)

    if not path.is_file():
        raise FileNotFoundError(
            f"Arquivo de entrada nao encontrado: {path}"
        )

    image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)

    if image is None:
        raise ValueError(
            f"Nao foi possivel abrir a imagem: {path}"
        )

    if image.ndim != 2:
        raise ValueError(
            "A imagem deve estar em niveis de cinza."
        )

    return image


def save_image(path, image):
    path = Path(path)

    path.parent.mkdir(parents=True, exist_ok=True)

    if not cv2.imwrite(str(path), image):
        raise IOError(
            f"Nao foi possivel salvar a imagem: {path}"
        )
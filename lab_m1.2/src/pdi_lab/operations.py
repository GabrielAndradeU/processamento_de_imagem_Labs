import numpy as np


def _validate_image(image):
    if image is None:
        raise ValueError("Imagem invalida.")

    if not isinstance(image, np.ndarray):
        raise TypeError(
            "A imagem deve ser uma matriz NumPy."
        )

    if image.ndim != 2:
        raise ValueError(
            "A imagem deve estar em niveis de cinza."
        )

    if image.size == 0:
        raise ValueError("A imagem esta vazia.")


def _clip(value):
    if value < 0:
        return 0

    if value > 255:
        return 255

    return value


def brightness(image, value):
    _validate_image(image)

    height, width = image.shape

    result = np.zeros_like(image)

    for y in range(height):
        for x in range(width):
            pixel = int(image[y, x])

            new_value = pixel + value

            new_value = _clip(new_value)

            result[y, x] = new_value

    return result


def contrast(image, alpha):
    _validate_image(image)

    height, width = image.shape

    result = np.zeros_like(image)

    for y in range(height):
        for x in range(width):
            pixel = int(image[y, x])

            new_value = alpha * (pixel - 128) + 128

            new_value = _clip(new_value)

            result[y, x] = int(round(new_value))

    return result


def negative(image):
    _validate_image(image)

    height, width = image.shape

    result = np.zeros_like(image)

    for y in range(height):
        for x in range(width):
            pixel = int(image[y, x])

            result[y, x] = 255 - pixel

    return result


def threshold(image, threshold_value):
    _validate_image(image)

    if isinstance(threshold_value, bool):
        raise ValueError("O threshold deve ser inteiro.")

    if not isinstance(threshold_value, int):
        raise ValueError("O threshold deve ser inteiro.")

    if threshold_value < 0 or threshold_value > 255:
        raise ValueError(
            "O threshold deve estar entre 0 e 255."
        )

    height, width = image.shape

    result = np.zeros_like(image)

    for y in range(height):
        for x in range(width):
            pixel = int(image[y, x])

            if pixel < threshold_value:
                result[y, x] = 0
            else:
                result[y, x] = 255

    return result


def histogram(image):
    _validate_image(image)

    counts = [0] * 256

    height, width = image.shape

    for y in range(height):
        for x in range(width):
            pixel = int(image[y, x])

            if pixel < 0 or pixel > 255:
                raise ValueError(
                    "Pixel fora do intervalo [0, 255]."
                )

            counts[pixel] += 1

    return counts
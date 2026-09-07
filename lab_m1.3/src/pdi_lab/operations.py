import math

import numpy as np

from .parameters import (
    validate_kernel,
    validate_border,
)


def _validate_image(image):
    if not isinstance(image, np.ndarray):
        raise ValueError(
            "A imagem deve ser um numpy.ndarray."
        )

    if image.ndim != 2:
        raise ValueError(
            "A imagem deve estar em níveis de cinza."
        )

    if image.size == 0:
        raise ValueError(
            "A imagem não pode ser vazia."
        )


def _saturate(value):
    if value < 0:
        return 0

    if value > 255:
        return 255

    return int(round(value))


def _get_pixel(image, y, x, border):
    height, width = image.shape

    if 0 <= y < height and 0 <= x < width:
        return int(image[y, x])

    if border == "copy":
        return None

    if border == "replicate":
        y = max(0, min(y, height - 1))
        x = max(0, min(x, width - 1))

        return int(image[y, x])

    raise ValueError(
        f"Estratégia de borda inválida: {border}"
    )


def convolution(image, kernel, border="copy"):
    _validate_image(image)

    kernel = validate_kernel(kernel)
    border = validate_border(border)

    height, width = image.shape
    kernel_size = kernel.shape[0]
    radius = kernel_size // 2

    result = np.zeros(
        (height, width),
        dtype=np.float64
    )

    for y in range(height):
        for x in range(width):

            if border == "copy":
                if (
                    y - radius < 0
                    or y + radius >= height
                    or x - radius < 0
                    or x + radius >= width
                ):
                    result[y, x] = image[y, x]
                    continue

            accumulator = 0.0

            for ky in range(kernel_size):
                for kx in range(kernel_size):

                    image_y = y + ky - radius
                    image_x = x + kx - radius

                    pixel = _get_pixel(
                        image,
                        image_y,
                        image_x,
                        border
                    )

                    if pixel is None:
                        continue

                    accumulator += (
                        pixel * kernel[ky, kx]
                    )

            result[y, x] = accumulator

    return result


def convolution_image(image, kernel, border="copy"):
    result = convolution(
        image,
        kernel,
        border
    )

    output = np.zeros_like(
        image,
        dtype=np.uint8
    )

    height, width = image.shape

    for y in range(height):
        for x in range(width):
            output[y, x] = _saturate(
                result[y, x]
            )

    return output


def mean_filter(image, size=3, border="copy"):
    if size not in (3, 5):
        raise ValueError(
            "O filtro de média deve possuir tamanho 3 ou 5."
        )

    value = 1.0 / (size * size)

    kernel = np.full(
        (size, size),
        value,
        dtype=float
    )

    return convolution_image(
        image,
        kernel,
        border
    )


def weighted_mean(image, border="copy"):
    kernel = np.array(
        [
            [1, 2, 1],
            [2, 4, 2],
            [1, 2, 1],
        ],
        dtype=float
    )

    kernel /= kernel.sum()

    return convolution_image(
        image,
        kernel,
        border
    )


def laplacian(image, border="copy"):
    kernel = np.array(
        [
            [0, 1, 0],
            [1, -4, 1],
            [0, 1, 0],
        ],
        dtype=float
    )

    return convolution(
        image,
        kernel,
        border
    )


def laplacian_enhance(image, border="copy"):
    response = laplacian(
        image,
        border
    )

    height, width = image.shape

    result = np.zeros_like(
        image,
        dtype=np.uint8
    )

    for y in range(height):
        for x in range(width):
            value = (
                int(image[y, x])
                - response[y, x]
            )

            result[y, x] = _saturate(value)

    return result


def sobel_gx(image, border="copy"):
    kernel = np.array(
        [
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1],
        ],
        dtype=float
    )

    return convolution(
        image,
        kernel,
        border
    )


def sobel_gy(image, border="copy"):
    kernel = np.array(
        [
            [-1, -2, -1],
            [0, 0, 0],
            [1, 2, 1],
        ],
        dtype=float
    )

    return convolution(
        image,
        kernel,
        border
    )


def sobel_magnitude_approx(image, border="copy"):
    gx = sobel_gx(
        image,
        border
    )

    gy = sobel_gy(
        image,
        border
    )

    height, width = image.shape

    result = np.zeros_like(
        image,
        dtype=np.uint8
    )

    for y in range(height):
        for x in range(width):
            value = (
                abs(gx[y, x])
                + abs(gy[y, x])
            )

            result[y, x] = _saturate(value)

    return result


def sobel_magnitude_euclidean(image, border="copy"):
    gx = sobel_gx(
        image,
        border
    )

    gy = sobel_gy(
        image,
        border
    )

    height, width = image.shape

    result = np.zeros_like(
        image,
        dtype=np.uint8
    )

    for y in range(height):
        for x in range(width):
            value = math.sqrt(
                gx[y, x] ** 2
                + gy[y, x] ** 2
            )

            result[y, x] = _saturate(value)

    return result
import numpy as np
import pytest

from pdi_lab.operations import (
    convolution,
    mean_filter,
    weighted_mean,
    laplacian,
    sobel_gx,
    sobel_gy,
)


def test_identity_kernel():
    image = np.array(
        [
            [10, 20, 30],
            [40, 50, 60],
            [70, 80, 90],
        ],
        dtype=np.uint8
    )

    kernel = np.array(
        [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0],
        ],
        dtype=float
    )

    result = convolution(
        image,
        kernel,
        "copy"
    )

    np.testing.assert_array_equal(
        result,
        image
    )


def test_constant_image_mean():
    image = np.full(
        (5, 5),
        100,
        dtype=np.uint8
    )

    result = mean_filter(
        image,
        3,
        "replicate"
    )

    expected = np.full(
        (5, 5),
        100,
        dtype=np.uint8
    )

    np.testing.assert_array_equal(
        result,
        expected
    )


def test_impulse_identity():
    image = np.zeros(
        (5, 5),
        dtype=np.uint8
    )

    image[2, 2] = 255

    kernel = np.array(
        [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0],
        ],
        dtype=float
    )

    result = convolution(
        image,
        kernel,
        "copy"
    )

    np.testing.assert_array_equal(
        result,
        image
    )


def test_mean_filter_reduces_impulse():
    image = np.zeros(
        (5, 5),
        dtype=np.uint8
    )

    image[2, 2] = 255

    result = mean_filter(
        image,
        3,
        "copy"
    )

    assert result[2, 2] == 28


def test_weighted_mean_constant():
    image = np.full(
        (5, 5),
        80,
        dtype=np.uint8
    )

    result = weighted_mean(
        image,
        "replicate"
    )

    expected = np.full(
        (5, 5),
        80,
        dtype=np.uint8
    )

    np.testing.assert_array_equal(
        result,
        expected
    )


def test_mean_5x5_constant():
    image = np.full(
        (7, 7),
        120,
        dtype=np.uint8
    )

    result = mean_filter(
        image,
        5,
        "replicate"
    )

    expected = np.full(
        (7, 7),
        120,
        dtype=np.uint8
    )

    np.testing.assert_array_equal(
        result,
        expected
    )


def test_laplacian_constant():
    image = np.full(
        (5, 5),
        100,
        dtype=np.uint8
    )

    result = laplacian(
        image,
        "replicate"
    )

    expected = np.zeros(
        (5, 5),
        dtype=float
    )

    np.testing.assert_array_equal(
        result,
        expected
    )


def test_laplacian_can_be_negative():
    image = np.zeros(
        (5, 5),
        dtype=np.uint8
    )

    image[2, 2] = 255

    result = laplacian(
        image,
        "copy"
    )

    assert result[2, 2] < 0


def test_sobel_gx_constant():
    image = np.full(
        (5, 5),
        100,
        dtype=np.uint8
    )

    result = sobel_gx(
        image,
        "replicate"
    )

    np.testing.assert_array_equal(
        result,
        np.zeros(
            (5, 5),
            dtype=float
        )
    )


def test_sobel_gy_constant():
    image = np.full(
        (5, 5),
        100,
        dtype=np.uint8
    )

    result = sobel_gy(
        image,
        "replicate"
    )

    np.testing.assert_array_equal(
        result,
        np.zeros(
            (5, 5),
            dtype=float
        )
    )


def test_invalid_even_kernel():
    image = np.zeros(
        (5, 5),
        dtype=np.uint8
    )

    kernel = np.ones(
        (2, 2),
        dtype=float
    )

    with pytest.raises(ValueError):
        convolution(
            image,
            kernel
        )


def test_invalid_non_square_kernel():
    image = np.zeros(
        (5, 5),
        dtype=np.uint8
    )

    kernel = np.ones(
        (3, 5),
        dtype=float
    )

    with pytest.raises(ValueError):
        convolution(
            image,
            kernel
        )


def test_invalid_border():
    image = np.zeros(
        (5, 5),
        dtype=np.uint8
    )

    kernel = np.ones(
        (3, 3),
        dtype=float
    )

    with pytest.raises(ValueError):
        convolution(
            image,
            kernel,
            "invalid"
        )
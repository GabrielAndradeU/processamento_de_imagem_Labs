import numpy as np
import pytest

from pdi_lab.operations import (
    brightness,
    contrast,
    negative,
    threshold,
    histogram,
)


def test_brightness_positive():
    image = np.array(
        [[0, 50], [100, 200]],
        dtype=np.uint8
    )

    result = brightness(image, 30)

    expected = np.array(
        [[30, 80], [130, 230]],
        dtype=np.uint8
    )

    np.testing.assert_array_equal(result, expected)


def test_brightness_negative():
    image = np.array(
        [[0, 50], [100, 200]],
        dtype=np.uint8
    )

    result = brightness(image, -30)

    expected = np.array(
        [[0, 20], [70, 170]],
        dtype=np.uint8
    )

    np.testing.assert_array_equal(result, expected)


def test_brightness_saturation_upper():
    image = np.array(
        [[230, 250], [255, 100]],
        dtype=np.uint8
    )

    result = brightness(image, 30)

    expected = np.array(
        [[255, 255], [255, 130]],
        dtype=np.uint8
    )

    np.testing.assert_array_equal(result, expected)


def test_brightness_saturation_lower():
    image = np.array(
        [[0, 10], [30, 100]],
        dtype=np.uint8
    )

    result = brightness(image, -30)

    expected = np.array(
        [[0, 0], [0, 70]],
        dtype=np.uint8
    )

    np.testing.assert_array_equal(result, expected)


def test_contrast_half():
    image = np.array(
        [[0, 128], [200, 255]],
        dtype=np.uint8
    )

    result = contrast(image, 0.5)

    expected = np.array(
        [[64, 128], [164, 192]],
        dtype=np.uint8
    )

    np.testing.assert_array_equal(result, expected)


def test_contrast_identity():
    image = np.array(
        [[0, 50], [128, 255]],
        dtype=np.uint8
    )

    result = contrast(image, 1.0)

    expected = image

    np.testing.assert_array_equal(result, expected)


def test_contrast_increased():
    image = np.array(
        [[0, 100], [128, 200]],
        dtype=np.uint8
    )

    result = contrast(image, 1.5)

    expected = np.array(
        [[0, 86], [128, 236]],
        dtype=np.uint8
    )

    np.testing.assert_array_equal(result, expected)


def test_negative():
    image = np.array(
        [[0, 50], [128, 255]],
        dtype=np.uint8
    )

    result = negative(image)

    expected = np.array(
        [[255, 205], [127, 0]],
        dtype=np.uint8
    )

    np.testing.assert_array_equal(result, expected)


def test_threshold():
    image = np.array(
        [[0, 127], [128, 255]],
        dtype=np.uint8
    )

    result = threshold(image, 128)

    expected = np.array(
        [[0, 0], [255, 255]],
        dtype=np.uint8
    )

    np.testing.assert_array_equal(result, expected)


def test_histogram():
    image = np.array(
        [[0, 0], [128, 255]],
        dtype=np.uint8
    )

    result = histogram(image)

    assert len(result) == 256
    assert result[0] == 2
    assert result[128] == 1
    assert result[255] == 1

    total = sum(result)

    assert total == 4


def test_histogram_all_values():
    image = np.arange(
        256,
        dtype=np.uint8
    ).reshape(16, 16)

    result = histogram(image)

    assert len(result) == 256

    for value in result:
        assert value == 1


def test_threshold_invalid():
    image = np.array(
        [[100]],
        dtype=np.uint8
    )

    with pytest.raises(ValueError):
        threshold(image, -1)

    with pytest.raises(ValueError):
        threshold(image, 256)
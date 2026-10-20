import cv2
import numpy as np
import pytest

from pdi_lab.contract import (
    validate_binary_mask,
    validate_mask_dimensions,
)
from pdi_lab.image_io import load_image
from pdi_lab.result_io import calculate_mask_statistics, save_mask
from pdi_lab.segment import segment_image
from pdi_lab.cli import main


def test_fixed_threshold_below_equal_above():
    image = np.array(
        [[99, 100, 101]],
        dtype=np.uint8
    )

    mask = segment_image(
        image,
        method="fixed",
        threshold=100
    )

    expected = np.array(
        [[0, 0, 255]],
        dtype=np.uint8
    )

    np.testing.assert_array_equal(mask, expected)


def test_fixed_threshold_produces_binary_mask():
    image = np.array(
        [[0, 50, 100], [150, 200, 255]],
        dtype=np.uint8
    )

    mask = segment_image(image, method="fixed", threshold=120)

    validate_binary_mask(mask)
    validate_mask_dimensions(mask, image)


def test_adaptive_produces_binary_mask():
    image = np.tile(
        np.array([0, 50, 100, 150, 200, 255], dtype=np.uint8),
        (21, 1)
    )

    mask = segment_image(
        image,
        method="adaptive",
        block_size=3,
        constant=5
    )

    validate_binary_mask(mask)
    validate_mask_dimensions(mask, image)


def test_invalid_method():
    image = np.zeros((10, 10), dtype=np.uint8)

    with pytest.raises(ValueError):
        segment_image(image, method="unknown")


@pytest.mark.parametrize("threshold", [-1, 256])
def test_invalid_fixed_threshold(threshold):
    image = np.zeros((10, 10), dtype=np.uint8)

    with pytest.raises(ValueError):
        segment_image(image, method="fixed", threshold=threshold)


@pytest.mark.parametrize("block_size", [0, 2, 4])
def test_invalid_adaptive_block_size(block_size):
    image = np.zeros((10, 10), dtype=np.uint8)

    with pytest.raises(ValueError):
        segment_image(
            image,
            method="adaptive",
            block_size=block_size
        )


def test_load_missing_image():
    with pytest.raises(FileNotFoundError):
        load_image("images/input/arquivo_inexistente.png")


def test_mask_statistics():
    mask = np.array(
        [[0, 255], [0, 255]],
        dtype=np.uint8
    )

    statistics = calculate_mask_statistics(mask)

    assert statistics["total_pixels"] == 4
    assert statistics["foreground_pixels"] == 2
    assert statistics["background_pixels"] == 2
    assert statistics["foreground_percentage"] == 50.0


def test_save_mask(tmp_path):
    mask = np.array(
        [[0, 255], [255, 0]],
        dtype=np.uint8
    )

    output_path = tmp_path / "mask.png"
    save_mask(mask, output_path)

    loaded = cv2.imread(str(output_path), cv2.IMREAD_UNCHANGED)

    assert loaded is not None
    assert loaded.ndim == 2
    np.testing.assert_array_equal(loaded, mask)


def test_save_mask_rejects_non_png(tmp_path):
    mask = np.zeros((2, 2), dtype=np.uint8)

    with pytest.raises(ValueError):
        save_mask(mask, tmp_path / "mask.jpg")


def test_cli_success(tmp_path, monkeypatch):
    input_path = tmp_path / "input.png"
    output_path = tmp_path / "output.png"

    image = np.array(
        [[0, 100, 200], [50, 150, 255]],
        dtype=np.uint8
    )

    assert cv2.imwrite(str(input_path), image)

    monkeypatch.setattr(
        "sys.argv",
        [
            "pdi_lab",
            "--input", str(input_path),
            "--output", str(output_path),
            "--operation", "segment",
            "--method", "fixed",
            "--threshold", "120"
        ]
    )

    assert main() == 0
    assert output_path.is_file()


def test_cli_failure_returns_nonzero(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        [
            "pdi_lab",
            "--input", str(tmp_path / "missing.png"),
            "--output", str(tmp_path / "mask.png"),
            "--operation", "segment"
        ]
    )

    assert main() == 1
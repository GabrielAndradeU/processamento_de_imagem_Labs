
import cv2
import numpy as np
import pytest

from pdi_lab.components import label_components, save_components_csv
from pdi_lab.morphology import apply_morphology


def test_diagonal_pixels_connectivity_4_and_8():
    mask = np.zeros((5, 5), dtype=np.uint8)
    mask[1, 1] = 255
    mask[2, 2] = 255

    count_4, _, _ = label_components(mask, connectivity=4)
    count_8, _, _ = label_components(mask, connectivity=8)

    assert count_4 == 2
    assert count_8 == 1


def test_empty_mask_has_zero_components():
    mask = np.zeros((10, 10), dtype=np.uint8)

    count, labels, components = label_components(mask, connectivity=8)

    assert count == 0
    assert len(components) == 0
    assert labels.shape == mask.shape


def test_component_touching_border():
    mask = np.zeros((10, 10), dtype=np.uint8)
    mask[0:3, 0:4] = 255

    count, _, components = label_components(mask, connectivity=8)

    assert count == 1
    assert components[0]["area"] == 12
    assert components[0]["x"] == 0
    assert components[0]["y"] == 0
    assert components[0]["width"] == 4
    assert components[0]["height"] == 3


def test_invalid_connectivity():
    mask = np.zeros((5, 5), dtype=np.uint8)

    with pytest.raises(ValueError):
        label_components(mask, connectivity=6)


def test_opening_removes_small_noise(tmp_path):
    mask = np.zeros((30, 30), dtype=np.uint8)
    mask[10:20, 10:20] = 255
    mask[2, 2] = 255

    stages = apply_morphology(mask, tmp_path, kernel_size=3)

    assert stages["opening"][2, 2] == 0
    assert np.count_nonzero(stages["opening"]) < np.count_nonzero(mask)
    assert (tmp_path / "stage_closing.png").is_file()
    assert (tmp_path / "stage_opening.png").is_file()


def test_closing_fills_small_hole(tmp_path):
    mask = np.zeros((30, 30), dtype=np.uint8)
    mask[5:25, 5:25] = 255
    mask[14, 14] = 0

    stages = apply_morphology(mask, tmp_path, kernel_size=3)

    assert stages["closing"][14, 14] == 255


def test_csv_contains_required_columns_and_kept(tmp_path):
    mask = np.zeros((10, 10), dtype=np.uint8)
    mask[1:4, 1:4] = 255
    mask[7, 7] = 255

    _, _, components = label_components(mask, connectivity=8)
    csv_path = tmp_path / "components.csv"

    save_components_csv(components, csv_path, min_area=2)

    content = csv_path.read_text(encoding="utf-8")
    header = content.splitlines()[0]

    assert header == "label,area,x,y,width,height,cx,cy,kept"
    assert "1" in content


def test_invalid_kernel_size(tmp_path):
    mask = np.zeros((10, 10), dtype=np.uint8)

    with pytest.raises(ValueError):
        apply_morphology(mask, tmp_path, kernel_size=2)

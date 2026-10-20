
from pathlib import Path

from pdi_lab.image_io import load_mask, invert_binary_mask
from pdi_lab.result_io import save_mask


experiments = [
    (
        Path("images/output/imagem_a_fixed.png"),
        Path("results/imagem_a/imagem_a_initial.png"),
    ),
    (
        Path("images/output/imagem_b_fixed.png"),
        Path("results/imagem_b/imagem_b_initial.png"),
    ),
]

for input_path, output_path in experiments:
    mask = load_mask(input_path)

    inverted_mask = invert_binary_mask(mask)
    save_mask(inverted_mask, output_path)

    print(f"Máscara inicial salva: {output_path}")

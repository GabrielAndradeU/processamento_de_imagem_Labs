
import csv
import cv2

pares = [
    (
        "Imagem A inicial",
        "results/imagem_a_initial.png",
        "results/imagem_a_initial.csv",
    ),
    (
        "Imagem A final",
        "results/imagem_a_final.png",
        "results/imagem_a_final.csv",
    ),
    (
        "Imagem B inicial",
        "results/imagem_b_initial.png",
        "results/imagem_b_initial.csv",
    ),
    (
        "Imagem B final",
        "results/imagem_b_final.png",
        "results/imagem_b_final.csv",
    ),
]

for nome, caminho_mascara, caminho_csv in pares:
    mascara = cv2.imread(caminho_mascara, cv2.IMREAD_GRAYSCALE)

    if mascara is None:
        print(f"{nome}: ERRO — máscara não encontrada.")
        continue

    with open(caminho_csv, encoding="utf-8", newline="") as arquivo:
        componentes = list(csv.DictReader(arquivo))

    soma_areas = sum(int(item["area"]) for item in componentes)
    pixels_brancos = cv2.countNonZero(mascara)

    correto = soma_areas == pixels_brancos

    print(f"\n{nome}")
    print(f"Pixels brancos na máscara: {pixels_brancos}")
    print(f"Soma das áreas no CSV:    {soma_areas}")
    print(f"Resultado correto:        {correto}")

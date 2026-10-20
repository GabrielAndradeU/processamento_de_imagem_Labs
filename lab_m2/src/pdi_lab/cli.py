
import argparse
import json
import sys
from pathlib import Path

import cv2

from pdi_lab.contract import validate_binary_mask, validate_mask_dimensions
from pdi_lab.image_io import load_image, load_mask
from pdi_lab.result_io import calculate_mask_statistics, save_mask
from pdi_lab.segment import segment_image
from pdi_lab.components import (
    label_components,
    save_components_csv,
    draw_component_boxes,
)
from pdi_lab.morphology import apply_morphology


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pdi_lab",
        description="Ferramenta de segmentação e análise de imagens.",
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Caminho da imagem original ou máscara binária.",
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Caminho da máscara PNG ou prefixo dos resultados.",
    )

    parser.add_argument(
        "--operation",
        choices=["segment", "analyze"],
        required=True,
        help="Operação a executar.",
    )

    parser.add_argument(
        "--method",
        choices=["fixed", "adaptive"],
        default="fixed",
        help="Método de segmentação.",
    )

    parser.add_argument(
        "--threshold",
        type=int,
        default=120,
        help="Limiar fixo entre 0 e 255.",
    )

    parser.add_argument(
        "--block-size",
        type=int,
        default=21,
        help="Tamanho ímpar da vizinhança adaptativa.",
    )

    parser.add_argument(
        "--constant",
        type=float,
        default=5,
        help="Constante subtraída do limiar adaptativo.",
    )

    parser.add_argument(
        "--connectivity",
        type=int,
        choices=[4, 8],
        default=8,
        help="Conectividade utilizada na análise final.",
    )

    parser.add_argument(
        "--min-area",
        type=int,
        default=0,
        help="Área mínima para marcar um componente como mantido.",
    )

    parser.add_argument(
        "--kernel-size",
        type=int,
        default=3,
        help="Tamanho ímpar do kernel morfológico.",
    )

    return parser


def run_segment(args: argparse.Namespace) -> None:
    image = load_image(args.input)

    mask = segment_image(
        image=image,
        method=args.method,
        threshold=args.threshold,
        block_size=args.block_size,
        constant=args.constant,
    )

    validate_binary_mask(mask)
    validate_mask_dimensions(mask, image)
    save_mask(mask, args.output)

    statistics = calculate_mask_statistics(mask)

    print("Segmentação concluída com sucesso.")
    print(f"Método: {args.method}")
    print(f"Imagem de entrada: {args.input}")
    print(f"Máscara salva em: {args.output}")
    print(f"Dimensões: {mask.shape[1]} x {mask.shape[0]}")
    print(f"Pixels totais: {statistics['total_pixels']}")
    print(f"Pixels de primeiro plano: {statistics['foreground_pixels']}")
    print(f"Pixels de fundo: {statistics['background_pixels']}")
    print(
        "Proporção de primeiro plano: "
        f"{statistics['foreground_percentage']:.2f}%"
    )


def run_analyze(args: argparse.Namespace) -> None:
    if args.min_area < 0:
        raise ValueError("A área mínima não pode ser negativa.")

    if args.kernel_size < 1 or args.kernel_size % 2 == 0:
        raise ValueError("O tamanho do kernel deve ser ímpar e maior que zero.")

    mask = load_mask(args.input)
    output_prefix = Path(args.output)
    output_prefix.parent.mkdir(parents=True, exist_ok=True)

    initial_path = output_prefix.with_name(
        f"{output_prefix.name}_initial.png"
    )
    closing_path = output_prefix.with_name(
        f"{output_prefix.name}_closing.png"
    )
    final_path = output_prefix.with_name(
        f"{output_prefix.name}_final.png"
    )
    initial_csv = output_prefix.with_name(
        f"{output_prefix.name}_initial.csv"
    )
    final_csv = output_prefix.with_name(
        f"{output_prefix.name}_final.csv"
    )
    labels_path = output_prefix.with_name(
        f"{output_prefix.name}_labels.png"
    )
    summary_path = output_prefix.with_name(
        f"{output_prefix.name}_summary.json"
    )

    save_mask(mask, initial_path)

    initial_count_4, _, components_4 = label_components(mask, 4)
    initial_count_8, _, components_8 = label_components(mask, 8)

    initial_count, _, initial_components = label_components(
        mask,
        args.connectivity,
    )
    save_components_csv(initial_components, initial_csv, args.min_area)

    stages = apply_morphology(
        mask,
        output_prefix.parent / f"{output_prefix.name}_stages",
        kernel_size=args.kernel_size,
    )

    closing = stages["closing"]
    final_mask = stages["opening"]

    save_mask(closing, closing_path)
    save_mask(final_mask, final_path)

    final_count, _, final_components = label_components(
        final_mask,
        args.connectivity,
    )
    save_components_csv(final_components, final_csv, args.min_area)

    boxed_image = draw_component_boxes(
        final_mask,
        final_components,
        args.min_area,
    )

    if not cv2.imwrite(str(labels_path), boxed_image):
        raise OSError(f"Não foi possível salvar a imagem: {labels_path}")

    initial_stats = calculate_mask_statistics(mask)
    final_stats = calculate_mask_statistics(final_mask)

    initial_kept = sum(
        component["area"] >= args.min_area
        for component in initial_components
    )
    final_kept = sum(
        component["area"] >= args.min_area
        for component in final_components
    )

    summary = {
        "input": str(args.input),
        "connectivity": args.connectivity,
        "min_area": args.min_area,
        "kernel_size": args.kernel_size,
        "morphology_sequence": ["closing", "opening"],
        "initial": {
            "components_connectivity_4": initial_count_4,
            "components_connectivity_8": initial_count_8,
            "components_selected_connectivity": initial_count,
            "components_kept": int(initial_kept),
            "foreground_pixels": initial_stats["foreground_pixels"],
            "total_pixels": initial_stats["total_pixels"],
        },
        "final": {
            "components_selected_connectivity": final_count,
            "components_kept": int(final_kept),
            "foreground_pixels": final_stats["foreground_pixels"],
            "total_pixels": final_stats["total_pixels"],
        },
        "files": {
            "initial_mask": str(initial_path),
            "closing_mask": str(closing_path),
            "final_mask": str(final_path),
            "initial_csv": str(initial_csv),
            "final_csv": str(final_csv),
            "labeled_image": str(labels_path),
        },
    }

    with summary_path.open("w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4, ensure_ascii=False)

    print("Análise concluída com sucesso.")
    print(f"Conectividade selecionada: {args.connectivity}")
    print(f"Componentes iniciais (4): {initial_count_4}")
    print(f"Componentes iniciais (8): {initial_count_8}")
    print(f"Componentes iniciais: {initial_count}")
    print(f"Componentes finais: {final_count}")
    print(f"Componentes iniciais mantidos: {initial_kept}")
    print(f"Componentes finais mantidos: {final_kept}")
    print(
        "Pixels brancos antes/depois: "
        f"{initial_stats['foreground_pixels']} / "
        f"{final_stats['foreground_pixels']}"
    )
    print(f"CSV inicial: {initial_csv}")
    print(f"CSV final: {final_csv}")
    print(f"Imagem rotulada: {labels_path}")
    print(f"Resumo JSON: {summary_path}")


def main() -> int:
    parser = create_parser()
    args = parser.parse_args()

    try:
        if args.operation == "segment":
            run_segment(args)
        elif args.operation == "analyze":
            run_analyze(args)

        return 0

    except (OSError, ValueError, TypeError, cv2.error) as error:
        print(f"Erro: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

def validate_method(method: str) -> None:
    valid_methods = {"fixed", "adaptive"}

    if method not in valid_methods:
        raise ValueError(
            f"Método inválido: {method}. "
            f"Utilize um destes métodos: {', '.join(sorted(valid_methods))}."
        )


def validate_fixed_threshold(threshold: int) -> None:
    if isinstance(threshold, bool) or not isinstance(threshold, int):
        raise ValueError("O limiar fixo deve ser um número inteiro.")

    if not 0 <= threshold <= 255:
        raise ValueError("O limiar fixo deve estar entre 0 e 255.")


def validate_adaptive_parameters(
    block_size: int,
    constant: float
) -> None:
    if isinstance(block_size, bool) or not isinstance(block_size, int):
        raise ValueError("O tamanho do bloco deve ser um número inteiro.")

    if block_size < 3 or block_size % 2 == 0:
        raise ValueError(
            "O tamanho do bloco deve ser ímpar e maior ou igual a 3."
        )

    if not isinstance(constant, (int, float)) or isinstance(constant, bool):
        raise ValueError("A constante adaptativa deve ser numérica.")

    if not -255 <= constant <= 255:
        raise ValueError(
            "A constante adaptativa deve estar entre -255 e 255."
        )
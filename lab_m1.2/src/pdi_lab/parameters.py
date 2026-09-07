def validate_brightness(value):
    if isinstance(value, bool):
        raise ValueError("O valor de brilho deve ser inteiro.")

    if not isinstance(value, int):
        raise ValueError("O valor de brilho deve ser inteiro.")

    return value


def validate_alpha(alpha):
    if isinstance(alpha, bool):
        raise ValueError("Alpha deve ser um numero.")

    if not isinstance(alpha, (int, float)):
        raise ValueError("Alpha deve ser um numero.")

    if alpha < 0:
        raise ValueError("Alpha nao pode ser negativo.")

    return float(alpha)


def validate_threshold(value):
    if isinstance(value, bool):
        raise ValueError("O threshold deve ser inteiro.")

    if not isinstance(value, int):
        raise ValueError("O threshold deve ser inteiro.")

    if value < 0 or value > 255:
        raise ValueError(
            "O threshold deve estar entre 0 e 255."
        )

    return value
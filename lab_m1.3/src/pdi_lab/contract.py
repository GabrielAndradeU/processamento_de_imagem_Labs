class PdiLabError(Exception):
    """Excecao base do projeto."""


OPERATIONS = {
    "brightness",
    "contrast",
    "negative",
    "threshold",
    "histogram",
}


def validate_operation(operation):
    if operation not in OPERATIONS:
        raise PdiLabError(
            f"Operacao invalida: {operation}. "
            f"Operacoes disponiveis: {', '.join(sorted(OPERATIONS))}"
        )

    return operation
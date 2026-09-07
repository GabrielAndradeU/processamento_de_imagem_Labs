"""
contract.py

Exceções customizadas usadas em todo o pacote. Centralizar os erros
aqui evita ciclos de import entre image_io.py e operations.py, já
que ambos precisam levantar/capturar os mesmos tipos de erro.
"""


class ImagemInvalidaError(Exception):
    """Erro genérico para problemas de leitura ou formato de imagem."""
    pass


class NumeroDeCanaisInesperadoError(ImagemInvalidaError):
    pass


class TipoDeImagemIncompativelError(ImagemInvalidaError):
    pass


class QuantidadeDeNiveisInvalidaError(ValueError):
    pass

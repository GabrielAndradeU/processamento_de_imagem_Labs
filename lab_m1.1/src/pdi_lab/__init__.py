"""
pdi_lab

Pacote do Laboratório M1.1 — Processamento de Imagens.
Expõe as funções principais para quem quiser importar o pacote
diretamente (ex.: nos testes) em vez de rodar via CLI.
"""

from operations import (
    inspecionar_imagem,
    copia_manual,
    separar_canais,
    escala_cinza_media_simples,
    escala_cinza_media_ponderada,
    quantizar,
)

__all__ = [
    "inspecionar_imagem",
    "copia_manual",
    "separar_canais",
    "escala_cinza_media_simples",
    "escala_cinza_media_ponderada",
    "quantizar",
]

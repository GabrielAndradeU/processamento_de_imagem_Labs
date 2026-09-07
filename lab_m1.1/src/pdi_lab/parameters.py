"""
parameters.py

Constantes usadas pelas operações do laboratório: pesos da média
ponderada (ITU-R BT.601) e a lista padrão de níveis de quantização
pedida no enunciado.
"""

# Pesos da conversão para cinza por média ponderada:
# g = PESO_R*R + PESO_G*G + PESO_B*B
PESO_R = 0.299
PESO_G = 0.587
PESO_B = 0.114

# Níveis de quantização pedidos no enunciado (item 5)
NIVEIS_QUANTIZACAO_PADRAO = (16, 8, 4, 2)

# Faixa válida de intensidade para imagens uint8
VALOR_MINIMO_VALIDO = 0
VALOR_MAXIMO_VALIDO = 255

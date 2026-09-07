# Relatório — Laboratório M1.2

## 1. Objetivo

O objetivo do laboratório foi implementar transformações pontuais em imagens em níveis de cinza, nas quais cada pixel de saída depende apenas do pixel correspondente da imagem de entrada.

Foram implementadas as operações de ajuste de brilho, ajuste de contraste, negativo, limiarização binária e cálculo manual do histograma.

## 2. Operações implementadas

### 2.1 Ajuste de brilho

Foi implementada a expressão:

g(x,y) = f(x,y) + b

Foram realizados testes com valores positivos e negativos de `b`.

Os resultados foram limitados ao intervalo válido de 0 a 255 para evitar valores fora do intervalo de uma imagem de 8 bits.

### 2.2 Ajuste de contraste

Foi implementada a expressão:

g(x,y) = α(f(x,y) - 128) + 128

Foram utilizados os valores:

* α = 0,5;
* α = 1,0;
* α = 1,5.

### 2.3 Negativo

Foi implementada a expressão:

g(x,y) = 255 - f(x,y)

A transformação inverte as intensidades da imagem.

### 2.4 Limiarização

Foi implementada a limiarização binária utilizando:

g(x,y) = 0, quando f(x,y) < T

g(x,y) = 255, quando f(x,y) >= T

Foram utilizados dois valores diferentes de limiar.

### 2.5 Histograma

O histograma foi implementado manualmente utilizando uma estrutura com 256 posições.

Cada posição representa uma intensidade entre 0 e 255 e armazena a quantidade de pixels que possuem aquela intensidade.

## 3. Testes

Foram realizados testes com:

* brilho negativo;
* brilho positivo;
* saturação inferior;
* saturação superior;
* contraste reduzido;
* contraste identidade;
* contraste ampliado;
* negativo;
* dois valores de limiar;
* histograma da imagem original;
* histogramas de imagens transformadas;
* imagem pequena para conferência manual.

Os testes automatizados foram executados utilizando:

```bash
python -m pytest
```

## 4. Resultados

### Brilho

O aumento do brilho deslocou as intensidades dos pixels para valores maiores. A redução do brilho deslocou as intensidades para valores menores.

Nos casos em que o resultado ultrapassou 255, o valor foi limitado a 255. Nos casos em que ficou abaixo de 0, foi limitado a 0.

### Contraste

Com α = 0,5, as intensidades foram aproximadas do valor central 128, reduzindo o contraste.

Com α = 1,0, a imagem manteve suas intensidades originais.

Com α = 1,5, os valores foram afastados de 128, aumentando o contraste. Valores que ultrapassaram os limites foram saturados.

### Negativo

O negativo inverteu as intensidades. Pixels claros passaram a ser escuros e pixels escuros passaram a ser claros.

### Limiarização

A limiarização transformou a imagem em apenas dois valores possíveis: 0 e 255.

Alterar o valor de `T` modificou a quantidade de pixels classificados como preto ou branco.

### Histograma

O histograma permitiu observar a distribuição das intensidades da imagem.

Após o aumento do brilho, a distribuição foi deslocada para intensidades maiores, com possibilidade de concentração em 255 devido à saturação.

Após o aumento do contraste, as intensidades se afastaram de 128, podendo ocorrer concentração nos extremos devido à saturação.

## 5. Análise técnica

### 5.1 Diferença entre brilho e contraste

O brilho desloca as intensidades aproximadamente na mesma direção, aumentando ou diminuindo os valores dos pixels.

O contraste modifica a distância dos valores em relação a 128. Dessa forma, valores abaixo de 128 podem ficar ainda menores e valores acima de 128 podem ficar ainda maiores quando α > 1.

### 5.2 Saturação

A saturação ocorreu quando uma transformação produziu valores menores que 0 ou maiores que 255.

Esses valores foram limitados para permanecer no intervalo válido de uma imagem de 8 bits.

### 5.3 Histograma após alteração do brilho

Ao aumentar o brilho, o histograma tende a se deslocar para a direita, em direção às intensidades maiores.

Ao diminuir o brilho, tende a se deslocar para a esquerda.

### 5.4 Histograma após alteração do contraste

Com contraste reduzido, as intensidades tendem a se concentrar em torno de 128.

Com contraste aumentado, as intensidades tendem a se afastar de 128, aumentando a presença de valores próximos aos extremos.

### 5.5 Informação perdida na limiarização

A limiarização substitui diversas intensidades diferentes por apenas dois valores: 0 ou 255.

Consequentemente, informações sobre os níveis intermediários de intensidade são perdidas.

## 6. Limitações

A implementação trabalha com imagens em níveis de cinza de 8 bits, utilizando intensidades entre 0 e 255.

A limitação ao intervalo de 0 a 255 provoca saturação quando uma transformação gera valores fora desse intervalo.

## 7. Conclusão

O laboratório permitiu observar, na prática, como transformações pontuais alteram os valores dos pixels e como essas alterações aparecem na distribuição das intensidades.

As operações foram implementadas manualmente com percurso explícito dos pixels, enquanto as bibliotecas foram utilizadas como infraestrutura para leitura, escrita e manipulação das matrizes.

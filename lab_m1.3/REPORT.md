# Mini Relatório — Laboratório M1.3

## 1. Objetivo

O objetivo deste laboratório foi implementar operações de vizinhança e convolução em imagens em níveis de cinza, utilizando percurso explícito dos pixels e tratamento manual das bordas.

## 2. Operações implementadas

Foram implementadas:

* convolução genérica;
* filtro de média 3 × 3;
* filtro de média ponderada 3 × 3;
* filtro de média 5 × 5;
* Laplaciano;
* realce utilizando a resposta do Laplaciano;
* Sobel Gx;
* Sobel Gy;
* magnitude aproximada `|Gx| + |Gy|`;
* magnitude euclidiana.

## 3. Tratamento das bordas

Foram implementadas as estratégias `copy` e `replicate`.

A estratégia `copy` preserva os pixels que não possuem vizinhança completa. Já `replicate` utiliza o pixel válido mais próximo quando uma coordenada ultrapassa os limites da imagem.

## 4. Testes

Foram utilizados testes sintéticos para verificar:

* kernel identidade;
* imagem constante;
* imagem impulso;
* filtros de média;
* kernel 3 × 3;
* kernel 5 × 5;
* Laplaciano;
* Sobel;
* kernels inválidos;
* estratégia de borda inválida.

## 5. Análise

### 5.1 Operação pontual x operação de vizinhança

Em uma operação pontual, o valor do pixel de saída depende somente do pixel correspondente da imagem de entrada.

Em uma operação de vizinhança, o valor de saída depende também dos pixels ao redor. Por isso, é necessário considerar o tamanho do kernel e o tratamento das bordas.

### 5.2 Dimensões ímpares dos kernels

Kernels normalmente possuem dimensões ímpares para que exista um elemento central bem definido. Dessa forma, é possível posicionar o centro do kernel sobre cada pixel da imagem.

### 5.3 Aumento do tamanho do filtro de média

Ao aumentar o kernel de 3 × 3 para 5 × 5, uma região maior da imagem participa do cálculo. Isso aumenta a suavização e reduz mais variações locais, mas também pode causar maior perda de detalhes.

### 5.4 Tratamento das bordas

O tratamento escolhido altera principalmente os resultados próximos às extremidades da imagem. Na replicação, os pixels próximos às bordas são calculados utilizando os valores dos pixels mais próximos disponíveis.

### 5.5 Valores negativos no Laplaciano

O Laplaciano utiliza coeficientes positivos e negativos. Por isso, a resposta da convolução pode apresentar valores menores que zero em determinadas transições de intensidade.

A resposta bruta deve ser mantida antes da conversão para uma imagem de 8 bits.

### 5.6 Diferença entre Gx e Gy

`Gx` responde principalmente a variações horizontais de intensidade, sendo utilizado para detectar bordas verticais.

`Gy` responde principalmente a variações verticais de intensidade, sendo utilizado para detectar bordas horizontais.

### 5.7 Magnitudes L1 e L2

A magnitude `|Gx| + |Gy|` é uma aproximação mais simples e geralmente possui menor custo computacional.

A magnitude euclidiana utiliza:

`sqrt(Gx² + Gy²)`

e representa geometricamente o comprimento do vetor gradiente, mas possui custo computacional maior.

## 6. Limitações

Os resultados são armazenados como imagens de 8 bits somente após os cálculos necessários. Durante operações como Laplaciano e Sobel são utilizados tipos numéricos capazes de representar valores negativos e valores superiores a 255.

## 7. Conclusão

O laboratório permitiu verificar na prática como operações de vizinhança modificam uma imagem e como o tamanho do kernel, a estratégia de borda e os tipos numéricos interferem nos resultados.

# Processamento de Imagens — 2026-02

## Laboratório M1.3 — Convolução e filtragem espacial

## Objetivo

Implementar operações de vizinhança e convolução no domínio espacial, tratando explicitamente kernels, bordas, tipos numéricos e saturação.

Neste laboratório, o valor de cada pixel de saída depende de uma vizinhança da imagem de entrada.

As operações foram implementadas manualmente, utilizando percurso explícito dos pixels e das vizinhanças.

## Linguagem

Python 3.12 ou superior.

## Dependências

As dependências utilizadas são:

* NumPy;
* OpenCV;
* pytest.

O OpenCV é utilizado para leitura e escrita das imagens. As operações de convolução, filtragem, Laplaciano e Sobel são implementadas manualmente.

## Preparação

Na raiz do projeto:

```bash
python -m venv .venv
```

### Windows PowerShell

```bash
.\.venv\Scripts\Activate.ps1
```

### Instalação das dependências

```bash
python -m pip install -r requirements.txt
```

### Instalação do projeto em modo editável

```bash
python -m pip install -e .
```

## Testes

Execute todos os testes automatizados com:

```bash
python -m pytest -v
```

Os testes verificam, entre outros casos:

* kernel identidade;
* imagem constante;
* imagem impulso;
* filtros de média;
* Laplaciano;
* Sobel;
* kernels inválidos;
* estratégias de borda inválidas.

## Execução

Verifique a interface de linha de comando:

```bash
python -m pdi_lab --help
```

A aplicação utiliza os seguintes parâmetros:

```text
--input
--output
--operation
--kernel
--size
--border
```

As operações disponíveis são:

```text
convolution
mean_filter
weighted_mean
laplacian
laplacian_enhance
sobel_gx
sobel_gy
sobel_approx
sobel_euclidean
```

---

# Operações

## 1. Convolução genérica

A convolução recebe uma imagem, um kernel quadrado de dimensão ímpar e uma estratégia de tratamento de bordas.

Exemplo com kernel identidade 3 × 3:

```bash
python -m pdi_lab --input images/input/carro.jpg --output images/output/convolution.png --operation convolution --kernel kernels/identity_3x3.txt --border replicate
```

O arquivo `kernels/identity_3x3.txt` possui:

```text
3 3
0 0 0
0 1 0
0 0 0
```

O kernel identidade deve reproduzir a imagem de entrada.

---

## 2. Tratamento de bordas

O projeto implementa duas estratégias:

### `copy`

Pixels em que a vizinhança não cabe integralmente mantêm o valor original.

### `replicate`

Coordenadas que ultrapassam os limites da imagem são substituídas pela coordenada válida mais próxima.

Exemplo:

```bash
python -m pdi_lab --input images/input/carro.jpg --output images/output/convolution_replicate.png --operation convolution --kernel kernels/identity_3x3.txt --border replicate
```

A estratégia pode ser alterada para:

```bash
--border copy
```

As duas estratégias podem produzir diferenças principalmente nas regiões periféricas da imagem.

---

## 3. Filtro de média 3 × 3

Aplica um filtro de média utilizando uma vizinhança 3 × 3.

```bash
python -m pdi_lab --input images/input/carro.jpg --output images/output/media_3x3.png --operation mean_filter --size 3 --border replicate
```

O filtro reduz variações locais e suaviza detalhes da imagem.

---

## 4. Filtro de média 5 × 5

Aplica um filtro de média utilizando uma vizinhança 5 × 5.

```bash
python -m pdi_lab --input images/input/carro.jpg --output images/output/media_5x5.png --operation mean_filter --size 5 --border replicate
```

O aumento do tamanho da vizinhança produz maior suavização, podendo causar maior perda de detalhes.

---

## 5. Média ponderada 3 × 3

Aplica um filtro de média ponderada utilizando um kernel 3 × 3.

```bash
python -m pdi_lab --input images/input/carro.jpg --output images/output/media_ponderada.png --operation weighted_mean --border replicate
```

O filtro atribui pesos diferentes aos pixels da vizinhança, dando maior importância aos pixels próximos ao centro.

---

## 6. Laplaciano

O Laplaciano é utilizado para detectar variações de intensidade e destacar transições na imagem.

```bash
python -m pdi_lab --input images/input/carro.jpg --output images/output/laplacian.png --operation laplacian --border replicate
```

A resposta do Laplaciano é calculada utilizando valores numéricos que podem ser negativos antes da conversão para uma imagem de visualização.

---

## 7. Realce de nitidez com Laplaciano

O projeto também produz uma imagem realçada a partir da combinação da imagem original com a resposta do Laplaciano.

Essa operação corresponde ao realce de nitidez, também conhecido como *sharpening*.

```bash
python -m pdi_lab --input images/input/carro.jpg --output images/output/sharpen.png --operation laplacian_enhance --border replicate
```

A operação `laplacian_enhance` é utilizada no lugar de uma operação chamada `sharpen`, pois esse é o nome definido na interface atual do projeto.

---

## 8. Sobel Gx

Calcula a resposta do operador Sobel na direção horizontal, destacando principalmente bordas verticais.

```bash
python -m pdi_lab --input images/input/carro.jpg --output images/output/sobel_gx.png --operation sobel_gx --border replicate
```

---

## 9. Sobel Gy

Calcula a resposta do operador Sobel na direção vertical, destacando principalmente bordas horizontais.

```bash
python -m pdi_lab --input images/input/carro.jpg --output images/output/sobel_gy.png --operation sobel_gy --border replicate
```

---

## 10. Magnitude aproximada do Sobel

Calcula a magnitude utilizando:

```text
|Gx| + |Gy|
```

Execução:

```bash
python -m pdi_lab --input images/input/carro.jpg --output images/output/sobel_approx.png --operation sobel_approx --border replicate
```

Essa abordagem evita o cálculo de raiz quadrada e possui menor custo computacional.

---

## 11. Magnitude euclidiana do Sobel

Calcula a magnitude utilizando:

```text
sqrt(Gx² + Gy²)
```

Execução:

```bash
python -m pdi_lab --input images/input/carro.jpg --output images/output/sobel_euclidean.png --operation sobel_euclidean --border replicate
```

Essa é a magnitude euclidiana tradicional do gradiente.

---

# Kernels

Os kernels utilizados pelas operações ficam na pasta:

```text
kernels/
```

O formato utilizado para um kernel é:

```text
linhas colunas
valores do kernel
```

Exemplo de kernel identidade 3 × 3:

```text
3 3
0 0 0
0 1 0
0 0 0
```

Os kernels devem ser:

* quadrados;
* possuir dimensão ímpar;
* possuir valores numéricos válidos.

O programa realiza validações para kernels inválidos.

---

# Testes sintéticos

Os testes automatizados utilizam casos pequenos que permitem prever os resultados antes da execução.

Entre os casos considerados estão:

* kernel identidade;
* imagem constante;
* imagem impulso;
* degraus de intensidade;
* formas geométricas simples;
* conteúdo próximo às bordas;
* kernels 3 × 3;
* kernels 5 × 5.

Esses casos permitem verificar o comportamento das operações e do tratamento de bordas.

---

# Cuidados numéricos

Durante os cálculos são utilizados tipos numéricos adequados para evitar overflow e permitir valores negativos quando necessário.

A saturação para o intervalo de uma imagem de 8 bits ocorre somente no momento apropriado para gerar a imagem final.

Isso é especialmente importante em:

* convolução;
* Laplaciano;
* Sobel;
* cálculo de magnitudes.

---

# Guardas e validações

O projeto considera situações inválidas, incluindo:

* falha na leitura da imagem;
* kernel inexistente;
* kernel vazio;
* kernel não quadrado;
* kernel de dimensão par;
* estratégia de borda inválida;
* acesso fora dos limites;
* valores negativos durante os cálculos;
* valores superiores a 255;
* conversões entre tipos numéricos;
* saturação para geração da imagem final.

Em caso de erro, o programa apresenta uma mensagem informando o problema.

---

# Estrutura do projeto

```text
lab_m1.3/
├── README.md
├── REPORT.md
├── AI_USAGE.md
├── lab.json
├── requirements.txt
├── pyproject.toml
├── images/
│   ├── input/
│   └── output/
├── results/
├── kernels/
├── src/
│   └── pdi_lab/
└── tests/
```

---

# Operações implementadas

O projeto implementa:

* convolução genérica;
* tratamento de bordas `copy`;
* tratamento de bordas `replicate`;
* média 3 × 3;
* média ponderada 3 × 3;
* média 5 × 5;
* Laplaciano;
* realce de nitidez utilizando Laplaciano;
* Sobel Gx;
* Sobel Gy;
* magnitude aproximada `|Gx| + |Gy|`;
* magnitude euclidiana `sqrt(Gx² + Gy²)`.

Todas as operações avaliadas são implementadas manualmente, sem utilização de funções prontas que realizem diretamente convolução ou filtragem espacial.

---

# Resultado dos testes

Para executar os testes:

```bash
python -m pytest -v
```

O projeto deve executar todos os testes sem falhas.

Exemplo:

```text
13 passed
```

---

# Reprodutibilidade

A mesma operação executada com:

* a mesma imagem de entrada;
* os mesmos parâmetros;
* o mesmo kernel;
* a mesma estratégia de borda;

deve produzir o mesmo resultado.

A execução não depende de entrada interativa, números aleatórios ou configurações específicas do computador.

---

# Observação

O OpenCV é utilizado somente como infraestrutura para leitura e escrita das imagens.

As operações avaliadas neste laboratório foram implementadas manualmente, com percurso explícito dos pixels e das vizinhanças, sem utilização de funções prontas equivalentes de convolução, média, Laplaciano ou Sobel.

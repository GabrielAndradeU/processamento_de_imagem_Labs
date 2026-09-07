# Processamento de Imagens — Laboratório M1.2

## 1. Laboratório

Este projeto corresponde ao Laboratório M1.2 da disciplina de Processamento de Imagens — 2026-02.

O objetivo é implementar manualmente transformações pontuais em imagens em níveis de cinza:

* ajuste de brilho;
* ajuste de contraste;
* negativo;
* limiarização binária;
* histograma.

As transformações são realizadas com percurso explícito dos pixels.

## 2. Linguagem

Python 3.12 ou superior.

## 3. Dependências

As dependências estão em `requirements.txt`:

* `numpy`;
* `opencv-python`;
* `pytest`.

O OpenCV é utilizado para leitura e escrita das imagens. As operações avaliadas são implementadas manualmente.

## 4. Preparação do ambiente

Na raiz do projeto:

```bash
python -m venv .venv
```

Ative o ambiente virtual.

Windows PowerShell:

```bash
.\.venv\Scripts\Activate.ps1
```

Windows CMD:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Depois instale as dependências:

```bash
python -m pip install -r requirements.txt
```

Instale o projeto em modo editável:

```bash
python -m pip install -e .
```

## 5. Execução

Verifique a interface:

```bash
python -m pdi_lab --help
```

### Brilho

```bash
python -m pdi_lab \
  --input images/input/carro.jpg \
  --output images/output/brilho.png \
  --operation brightness \
  --value 30
```

### Contraste

```bash
python -m pdi_lab \
  --input images/input/carro.jpg \
  --output images/output/contraste.png \
  --operation contrast \
  --alpha 1.5
```

### Negativo

```bash
python -m pdi_lab \
  --input images/input/carro.jpg \
  --output images/output/negativo.png \
  --operation negative
```

### Limiarização

```bash
python -m pdi_lab \
  --input images/input/carro.jpg \
  --output images/output/limiar.png \
  --operation threshold \
  --threshold 128
```

### Histograma

```bash
python -m pdi_lab \
  --input images/input/carro.jpg \
  --output results/histograma.csv \
  --operation histogram
```

## 6. Testes

Execute os testes automatizados com:

```bash
python -m pytest
```

Os testes verificam brilho positivo e negativo, saturação, contraste, negativo, limiarização e histograma.

## 7. Estrutura

```text
images/input/     imagens de entrada
images/output/    imagens transformadas
results/          histogramas CSV
src/pdi_lab/      código-fonte
tests/            testes automatizados
kernels/          reservado para operações do M1.3
```

## 8. Observações

As transformações de intensidade e o cálculo do histograma foram implementados manualmente, com percurso explícito dos pixels.

A imagem de entrada é convertida para níveis de cinza durante a leitura.

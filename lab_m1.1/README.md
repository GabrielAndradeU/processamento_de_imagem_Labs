# Laboratório M1.1 — Representação, canais e níveis de cinza

## Qual laboratório está sendo entregue

Laboratório M1.1 da disciplina de Processamento de Imagens (2026-02):
implementação manual de operações fundamentais de representação de
imagens digitais — inspeção, cópia, separação de canais, conversão
para níveis de cinza e quantização — por meio de acesso direto aos
pixels, sem uso de funções prontas para essas operações.

**Autores:** Guilherme de Alcântara Leite, Gabriel Andrade Urbano

## Linguagem utilizada

Python 3.

## Dependências

- `numpy` — criação e manipulação de matrizes
- `opencv-python` (ou `opencv-python-headless`) — leitura e escrita de imagens

Declaradas em `requirements.txt`:

```text
numpy
opencv-python
```

## Como preparar o ambiente

1. Crie um ambiente virtual (obrigatório):

   **Windows (PowerShell):**
```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
```

   Se aparecer um erro de política de execução
   (`... não pode ser carregado porque a execução de scripts foi
   desabilitada neste sistema ...`), rode o comando abaixo uma única
   vez (é necessário apenas na primeira vez, por usuário):
```powershell
   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```
   Confirme com `S` quando perguntado, e rode novamente
   `.\venv\Scripts\Activate.ps1`.

   **Windows (cmd):**
```bash
   python -m venv venv
   venv\Scripts\activate
```

   **Linux/macOS:**
```bash
   python3 -m venv venv
   source venv/bin/activate
```

   Em todos os casos, `(venv)` deve aparecer no início da linha do
   terminal quando o ambiente estiver ativo.

2. Com o ambiente virtual ativo, instale as dependências:
```bash
   pip install -r requirements.txt
```
   (Se estiver fora de um venv e o pip recusar a instalação por ser um
   ambiente gerenciado, use `pip install -r requirements.txt --break-system-packages`
   — mas o recomendado é sempre usar o venv, conforme pedido pelo professor.)

   **Importante:** a pasta `venv/` é local da sua máquina e **não deve
   ser incluída na entrega** (é pesada e específica do seu sistema).
   Se estiver usando Git, adicione `venv/` ao `.gitignore`.

## Como compilar ou instalar

Não há etapa de compilação — Python é interpretado. Basta ter o
ambiente com as dependências instaladas (passo anterior).

## Como executar

Estrutura relevante do projeto:
lab_m1_1_Guilherme_de_Alcantara_Leite_Gabriel_Andrade_Urbano/
├── src/
│ └── pdi_lab/
│ ├── init.py # torna o pacote importável, expõe API pública
│ ├── main.py # orquestra o pipeline completo
│ ├── cli.py # parsing dos argumentos de linha de comando
│ ├── contract.py # exceções customizadas do projeto
│ ├── image_io.py # leitura/validação da imagem de entrada
│ ├── operations.py # as 5 operações manuais do laboratório
│ ├── parameters.py # constantes (pesos, níveis padrão, limites)
│ ├── result_io.py # salvamento das imagens de saída e resultados CSV
│ └── create_synthetic.py # gera a imagem sintética de teste
├── images/
│ ├── input/
│ └── output/
├── results/ # CSV com os dados numéricos (inspeção e métricas)
├── tests/
│ └── test_manual.py
├── README.md
├── REPORT.md
├── AI_USAGE.md
└── requirements.txt


Todos os comandos abaixo devem ser executados a partir da **raiz do
projeto** (a pasta que contém `src/`, `images/`, `tests/`).

1. **(Opcional) Gerar novamente a imagem sintética de teste:**
```bash
   python src/pdi_lab/create_synthetic.py
```

2. **Rodar o processamento completo:**
```bash
   python src/pdi_lab/__main__.py
```
   Isso processa a imagem sintética padrão (`images/input/synthetic.png`),
   salva todas as imagens de saída em `images/output/` e um CSV com os
   dados numéricos (inspeção da imagem e métricas de cada operação)
   em `results/resultados.csv`.

3. **Rodar sobre uma imagem própria:**
```bash
   python src/pdi_lab/__main__.py images/input/sua_foto.png
```

4. **Rodar escolhendo as pastas de saída (opcional):**
```bash
   python src/pdi_lab/__main__.py images/input/sua_foto.png --saida images/output --resultados results
```
   - `--saida` define onde vão as imagens (`copy.png`, `channel_*.png`, `gray_*.png`, `quant_*.png`).
   - `--resultados` define onde vai o CSV com os dados numéricos (`resultados.csv`).

5. **Rodar os testes:**
```bash
   python tests/test_manual.py
```

## Exemplos de comandos

```bash
# preparar ambiente (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# gerar imagem sintética
python src/pdi_lab/create_synthetic.py

# processar a imagem sintética
python src/pdi_lab/__main__.py

# processar uma imagem própria
python src/pdi_lab/__main__.py images/input/predio.jpg

# processar escolhendo as pastas de saída
python src/pdi_lab/__main__.py images/input/predio.jpg --saida images/output --resultados results

# exemplo usado neste projeto: sua_foto.png
python src/pdi_lab/__main__.py images/input/sua_foto.png --saida images/output --resultados results

# rodar os testes
python tests/test_manual.py
```

Saída esperada do processamento (resumida):
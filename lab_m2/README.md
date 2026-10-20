# pdi_lab — Processamento de Imagens

Projeto da disciplina de Processamento de Imagens que reúne as atividades M2.1 e M2.2 em um único pacote Python.

- **M2.1 — Segmentação:** gera máscaras binárias usando limiar fixo ou limiarização adaptativa.
- **M2.2 — Análise de máscaras:** identifica componentes conectados, calcula características das regiões, exporta CSV e aplica operações morfológicas de fechamento e abertura.

## 1. Requisitos

- Python 3.10 ou superior.
- NumPy.
- OpenCV.
- pytest para executar os testes.

As dependências estão declaradas em `requirements.txt` e `pyproject.toml`.

## 2. Preparar o ambiente

No PowerShell do Windows, execute os comandos a partir da pasta raiz do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip install -e .
```

Se o ambiente virtual já estiver ativado e o projeto instalado, não é necessário repetir a instalação.

## 3. Consultar os comandos

Para visualizar as opções disponíveis na versão instalada:

```powershell
python -m pdi_lab --help
```

A interface principal é:

```text
python -m pdi_lab --input ENTRADA --output SAIDA --operation OPERACAO
```

As operações disponíveis são `segment` e `analyze`.

## 4. M2.1 — Segmentação

A operação `segment` recebe uma imagem original e gera uma máscara binária.

### Limiar fixo

Exemplo com a Imagem A:

```powershell
python -m pdi_lab --input images/input/imagem_a.png --output results/imagem_a_fixed.png --operation segment --method fixed --threshold 120
```

O parâmetro `--threshold` define o limiar de intensidade em escala de cinza. Na implementação atual, os pixels com intensidade maior que o limiar recebem valor 255; os pixels menores ou iguais recebem valor 0.

### Limiarização adaptativa

Exemplo com a Imagem A:

```powershell
python -m pdi_lab --input images/input/imagem_a.png --output results/imagem_a_adaptive.png --operation segment --method adaptive --block-size 21 --constant 5
```

A limiarização adaptativa calcula limiares locais. `--block-size` define o tamanho da vizinhança e deve ser ímpar. `--constant` ajusta o limiar local.

### Imagens utilizadas

As imagens de entrada do projeto são:

- `images/input/imagem_a.png`
- `images/input/imagem_b.png`

Como os objetos de interesse são escuros sobre fundo claro, as máscaras geradas diretamente pela limiarização podem representar o fundo como branco. Para a análise de componentes, foi necessário inverter as máscaras selecionadas para representar os objetos em branco (255) e o fundo em preto (0).

As máscaras invertidas utilizadas na análise foram preparadas em `results/invertidas/`.

## 5. M2.2 — Análise de máscaras

A operação `analyze` recebe uma máscara binária, preserva uma cópia inicial, calcula componentes conectados, executa operações morfológicas e gera arquivos de resultado.

Exemplo com a Imagem A:

```powershell
python -m pdi_lab --input results/invertidas/imagem_a_fixed.png --output results/imagem_a --operation analyze --connectivity 8 --min-area 20 --kernel-size 3
```

Exemplo com a Imagem B:

```powershell
python -m pdi_lab --input results/invertidas/imagem_b_fixed.png --output results/imagem_b --operation analyze --connectivity 8 --min-area 20 --kernel-size 3
```

### Parâmetros da análise

| Parâmetro | Descrição |
|---|---|
| `--connectivity` | Define a conectividade dos componentes: 4 ou 8. |
| `--min-area` | Área mínima utilizada para indicar se um componente é mantido (`kept`) nos CSVs. |
| `--kernel-size` | Tamanho ímpar do kernel morfológico. |

A sequência morfológica implementada é fechamento seguido de abertura, usando um kernel retangular. O fechamento pode preencher pequenas lacunas e conectar regiões próximas; a abertura pode remover pequenos fragmentos brancos.

### Arquivos gerados

Para o prefixo `results/imagem_a`, a análise gera arquivos como:

- `results/imagem_a_initial.png`: máscara inicial.
- `results/imagem_a_closing.png`: máscara após fechamento.
- `results/imagem_a_final.png`: máscara após a sequência morfológica.
- `results/imagem_a_initial.csv`: componentes da máscara inicial.
- `results/imagem_a_final.csv`: componentes da máscara final.
- `results/imagem_a_labels.png`: visualização dos componentes.
- `results/imagem_a_summary.json`: resumo quantitativo da análise.
- `results/imagem_a_stages/`: imagens das etapas morfológicas.

Os nomes correspondentes da Imagem B usam o prefixo `results/imagem_b`.

Os CSVs registram o identificador do componente, área, posição, largura, altura, centroide e indicação `kept`. A área mínima classifica os componentes, mas não remove automaticamente pixels da máscara final.

## 6. Testes

Execute os testes a partir da raiz do projeto:

```powershell
python -m pytest -v
```

Os testes existentes cobrem segmentação, validação de máscaras, conectividade 4 e 8, máscaras vazias, componentes junto à borda, operações morfológicas, estrutura dos CSVs e validação de parâmetros.

Durante a validação registrada do projeto, 23 testes foram aprovados. Execute-os novamente antes da entrega para confirmar o estado final.

## 7. Verificação independente das áreas

O projeto também possui um script para comparar a quantidade de pixels brancos de cada máscara com a soma das áreas registradas no CSV:

```powershell
python -m pdi_lab.verificar_areas
```

Na validação realizada para as máscaras inicial e final das Imagens A e B, os quatro pares apresentaram correspondência entre os pixels brancos e a soma das áreas.

Essa verificação confirma a consistência das áreas exportadas, mas não comprova, por si só, que cada componente corresponda a um objeto físico real.

## 8. Estrutura principal

```text
images/
  input/
results/
src/
  pdi_lab/
    cli.py
    components.py
    contract.py
    image_io.py
    morphology.py
    parameters.py
    result_io.py
    segment.py
tests/
README.md
REPORT.md
ai_declaration.md
lab.json
pyproject.toml
requirements.txt
```

## 9. Limitações

A qualidade da análise depende da máscara de entrada. Ruído pode criar componentes adicionais, enquanto regiões próximas podem se unir em um único componente. As operações morfológicas também podem alterar áreas e contornos.

Por isso, os resultados quantitativos devem ser analisados em conjunto com as imagens originais, as máscaras intermediárias e a visualização dos componentes. A contagem de componentes não deve ser interpretada automaticamente como a quantidade real de objetos.
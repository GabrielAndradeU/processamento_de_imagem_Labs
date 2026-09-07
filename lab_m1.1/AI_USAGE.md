# AI_USAGE.md — Declaração de uso de Inteligência Artificial generativa

## Ferramenta utilizada

Claude (Anthropic).

## Como foi utilizada

A IA foi usada como ferramenta de **consulta e apoio na estruturação**
do projeto, e não como substituta do desenvolvimento pelos autores:

- **Consulta sobre organização do projeto**: apoio na definição da
  estrutura de pastas (`src/`, `images/`, `tests/`) e na convenção de
  nomes dos arquivos de saída.
- **Suporte na estruturação do código**: apoio na organização das
  funções de `src/pdi_lab/operations.py` e do fluxo de execução em
  `src/pdi_lab/main.py`, servindo como referência para a lógica de
  percurso manual de pixels exigida pelo enunciado.
- **Apoio na criação da imagem sintética** (`create_synthetic.py`)
  usada para conferência manual dos cálculos, e na estruturação dos
  casos de teste em `tests/test_manual.py`.
- **Consulta na redação da documentação** (`README.md`, `REPORT.md`,
  `AI_USAGE.md`), como apoio na organização das seções pedidas pela
  rubrica.
- **Suporte na depuração** de um erro de importação
  (`ModuleNotFoundError`) após reorganização da estrutura de pastas
  do projeto.

## O que não foi gerado por IA

- A implementação e a lógica das operações manuais (percurso de
  pixels, fórmulas de conversão para escala de cinza, estratégia de
  quantização) foram compreendidas e validadas pelos autores, que
  usaram a IA como apoio de estrutura e consulta, não como fonte única
  do código.
- As decisões de organização do projeto foram revisadas e ajustadas
  pelos autores (ex.: reorganização da pasta `src/` para
  `src/pdi_lab/`).
- Todos os resultados foram executados e conferidos manualmente pelos
  autores antes da entrega, incluindo a validação dos testes e a
  inspeção visual das imagens de saída.
- As respostas do mini relatório (`REPORT.md`) refletem a compreensão
  dos autores sobre os conceitos de resolução espacial, resolução
  radiométrica e representação de imagens, com a IA usada apenas como
  apoio na organização textual.

## Responsabilidade

Os autores declaram ter revisado, executado e compreendido a
totalidade do código entregue, sendo responsáveis pelo conteúdo final
desta entrega, independentemente da ferramenta utilizada como apoio na
sua produção.
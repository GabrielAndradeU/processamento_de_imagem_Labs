# Relatório técnico — M2.1 e M2.2

## 1. Objetivo

O projeto aborda duas etapas do processamento digital de imagens. No M2.1, são utilizados métodos de limiarização para transformar imagens em máscaras binárias. No M2.2, essas máscaras são analisadas por componentes conexos e submetidas a operações morfológicas, permitindo comparar a quantidade de componentes e a área de primeiro plano antes e depois do processamento.

O projeto utiliza Python e OpenCV, com uma interface de linha de comando para executar as operações e gerar máscaras, arquivos CSV e resumos dos resultados.

## 2. M2.1 — Segmentação por máscara binária

### 2.1. Métodos utilizados

A versão atual do projeto implementa dois métodos de segmentação:

- **Limiar fixo:** compara os valores dos pixels em escala de cinza com um único limiar global. É um método simples, mas seu resultado pode ser prejudicado por variações de iluminação.
- **Limiar adaptativo:** calcula o limiar considerando a vizinhança local de cada pixel. Pode lidar melhor com variações de iluminação, dependendo dos parâmetros utilizados.

A interface de linha de comando permite selecionar os métodos `fixed` e `adaptive`.

### 2.2. Imagens e configurações

Foram utilizadas duas imagens de entrada, denominadas `imagem_a.png` e `imagem_b.png`, ambas com resolução de 1200 × 896 pixels, totalizando 1.075.200 pixels por imagem.

As imagens apresentam objetos escuros sobre um fundo claro. Para os experimentos de segmentação, foram utilizados os seguintes parâmetros:

| Parâmetro | Limiar fixo | Limiar adaptativo |
|---|---|---|
| Método | `fixed` | `adaptive` |
| Limiar | 120 | Não se aplica |
| Tamanho do bloco | Não se aplica | 21 |
| Constante adaptativa | Não se aplica | 5 |

O método fixo utiliza o valor global 120. O método adaptativo utiliza uma vizinhança de 21 pixels e uma constante 5.

Como os objetos de interesse são escuros, as máscaras foram invertidas para que os objetos aparecessem em branco e o fundo em preto na etapa de análise de componentes conexos.

### 2.3. Resultados da segmentação

A tabela apresenta a quantidade de pixels brancos nas máscaras geradas diretamente pelos dois métodos.

| Imagem | Método | Pixels brancos | Proporção de pixels brancos |
|---|---|---:|---:|
| A | Fixo | 827.205 | 76,93% |
| A | Adaptativo | 943.782 | 87,78% |
| B | Fixo | 855.205 | 79,54% |
| B | Adaptativo | 913.248 | 84,94% |

Os valores representam a proporção de pixels classificados como brancos nas máscaras originais de segmentação. Como o fundo das imagens é claro, essa proporção não corresponde diretamente à área dos objetos escuros de interesse.

Após a inversão das máscaras, os resultados foram:

| Imagem | Método | Pixels brancos após inversão | Proporção após inversão |
|---|---|---:|---:|
| A | Fixo | 247.995 | 23,07% |
| A | Adaptativo | 131.418 | 12,22% |
| B | Fixo | 219.995 | 20,46% |
| B | Adaptativo | 161.952 | 15,06% |

A inversão permite utilizar os objetos escuros como primeiro plano na análise de componentes conexos. A diferença entre os resultados dos métodos mostra que a escolha do limiar influencia diretamente a quantidade de pixels selecionados.

O limiar fixo e o adaptativo produzem máscaras com proporções diferentes. Entretanto, apenas a proporção de pixels brancos não permite determinar qual método representa melhor os objetos reais. Para isso, também é necessário observar as máscaras e verificar a presença de ruídos, falhas nos objetos e regiões indevidamente selecionadas.

## 3. M2.2 — Componentes conexos e morfologia

### 3.1. Procedimento

O M2.2 recebe uma máscara binária e identifica seus componentes conexos. A análise pode utilizar conectividade 4 ou 8.

Na conectividade 4, cada pixel é considerado conectado aos pixels vizinhos que estão acima, abaixo, à esquerda e à direita. Na conectividade 8, também são considerados os vizinhos diagonais.

Para cada componente, são registrados os seguintes dados:

- Identificador do componente;
- Área em pixels;
- Coordenadas da caixa delimitadora;
- Largura e altura da caixa delimitadora;
- Coordenadas do centroide;
- Indicação de permanência segundo o limite de área configurado.

Os dados são exportados para arquivos CSV. O parâmetro `min_area` permite indicar quais componentes atendem ao critério mínimo de área. Esse filtro classifica os componentes no relatório, mas não remove seus pixels da máscara original.

### 3.2. Operações morfológicas

A sequência morfológica utilizada no projeto é composta por duas operações, com kernel retangular de 3 × 3 pixels:

1. **Fechamento morfológico (`closing`):** pode preencher pequenas lacunas e conectar regiões próximas.
2. **Abertura morfológica (`opening`):** pode remover pequenos componentes brancos e reduzir ruídos.

A ordem das operações influencia o resultado. O fechamento é aplicado primeiro para preencher lacunas ou aproximar regiões; em seguida, a abertura pode eliminar componentes pequenos.

O processamento gera máscaras intermediárias e finais, arquivos CSV com as características dos componentes, uma visualização dos componentes identificados e um resumo em JSON.

### 3.3. Configuração dos experimentos

As duas imagens utilizadas no M2.2 possuem resolução de 1200 × 896 pixels. Os experimentos utilizaram os seguintes parâmetros:

| Parâmetro | Valor |
|---|---|
| Conectividade selecionada | 8 |
| Área mínima | 20 pixels |
| Kernel morfológico | 3 × 3 |
| Sequência de operações | Fechamento seguido de abertura |

As máscaras iniciais utilizadas na análise foram invertidas para que os objetos escuros aparecessem como pixels brancos. Assim, a análise dos componentes foi realizada sobre o primeiro plano de interesse.

### 3.4. Resultados medidos

A tabela apresenta os resultados antes e depois da sequência morfológica.

| Medida | Imagem A — inicial | Imagem A — final | Imagem B — inicial | Imagem B — final |
|---|---:|---:|---:|---:|
| Pixels brancos | 247.995 | 249.395 | 219.995 | 237.230 |
| Componentes com conectividade 8 | 101 | 13 | 1.156 | 79 |
| Componentes com área ≥ 20 pixels | 14 | 13 | 76 | 52 |
| Componentes iniciais com conectividade 4 | 193 | — | 2.109 | — |

Na imagem A, a contagem de componentes com conectividade 8 caiu de 101 para 13, uma redução aproximada de 87,1%. A quantidade de pixels brancos aumentou de 247.995 para 249.395, uma diferença de 1.400 pixels.

Na imagem B, a contagem de componentes caiu de 1.156 para 79, uma redução aproximada de 93,2%. A quantidade de pixels brancos aumentou de 219.995 para 237.230, uma diferença de 17.235 pixels.

Esses resultados demonstram que as operações morfológicas modificaram a estrutura das máscaras. A redução da quantidade de componentes pode ocorrer pela união de regiões próximas, enquanto o aumento da área branca pode estar relacionado ao preenchimento de lacunas ou à alteração das regiões durante o processamento.

A diminuição da contagem de componentes não significa necessariamente que todos os objetos tenham sido segmentados corretamente. Regiões distintas podem ter sido unidas, e detalhes relevantes podem ter sido alterados.

### 3.5. Influência da conectividade

Antes da morfologia, a imagem A apresentou 193 componentes com conectividade 4 e 101 com conectividade 8. Na imagem B, foram identificados 2.109 componentes com conectividade 4 e 1.156 com conectividade 8.

A diferença ocorre porque a conectividade 8 considera os pixels que se tocam diagonalmente como parte do mesmo componente. Na conectividade 4, esses pixels podem pertencer a componentes separados.

Portanto, a escolha da conectividade influencia a quantidade de componentes identificados. Essa configuração deve ser considerada na interpretação dos resultados, principalmente quando existem regiões finas, fragmentadas ou que se tocam apenas pelos cantos.

### 3.6. Verificação da consistência das áreas

Foi realizada uma verificação entre a soma das áreas dos componentes registradas nos arquivos CSV e a quantidade de pixels brancos das máscaras correspondentes.

| Máscara | Pixels brancos | Soma das áreas no CSV | Resultado |
|---|---:|---:|---|
| Imagem A — inicial | 247.995 | 247.995 | Correto |
| Imagem A — final | 249.395 | 249.395 | Correto |
| Imagem B — inicial | 219.995 | 219.995 | Correto |
| Imagem B — final | 237.230 | 237.230 | Correto |

Os valores coincidiram nas quatro verificações. Isso confirma que, para os arquivos analisados, a soma das áreas dos componentes corresponde à quantidade de pixels brancos das respectivas máscaras.

Essa verificação confirma a consistência da contagem de pixels, mas não comprova que a segmentação corresponda perfeitamente aos objetos reais.

## 4. Testes

A suíte de testes contempla as operações de segmentação, a validação de parâmetros, a análise de componentes conexos e as operações morfológicas.

Os testes incluem:

- Comportamento do limiar fixo em diferentes valores;
- Validação das máscaras binárias;
- Validação de parâmetros de segmentação;
- Tratamento de imagens inexistentes ou inválidas;
- Identificação de componentes com conectividade 4 e 8;
- Tratamento de máscaras vazias;
- Análise de componentes que tocam as bordas;
- Remoção de ruído por abertura morfológica;
- Preenchimento de pequenos buracos por fechamento morfológico;
- Validação dos dados exportados para CSV;
- Validação de parâmetros morfológicos;
- Verificação do comportamento da interface de linha de comando.

Na execução anteriormente realizada, foram aprovados 23 testes. Para confirmar o resultado no ambiente de entrega, execute:

`python -m pytest -v`

O resultado final apresentado no relatório deve corresponder à execução realizada na versão do projeto que será entregue.

## 5. Limitações

O projeto apresenta algumas limitações que devem ser consideradas na interpretação dos resultados.

- Os resultados dependem da máscara inicial, dos parâmetros escolhidos e da conectividade utilizada.
- Objetos próximos ou encostados podem ser identificados como um único componente.
- Ruídos podem gerar componentes adicionais, enquanto operações morfológicas podem remover detalhes ou unir regiões distintas.
- O parâmetro de área mínima classifica componentes segundo um limite, mas não comprova que os componentes mantidos correspondam a objetos reais.
- Não foram utilizadas máscaras de referência para calcular métricas como precisão, revocação ou acurácia da segmentação.
- A redução na quantidade de componentes não deve ser interpretada isoladamente como evidência de melhoria da segmentação.

## 6. Conclusão

O M2.1 permite comparar a segmentação por limiar fixo e limiar adaptativo, demonstrando como a escolha do método influencia a quantidade de pixels selecionados. Os resultados das imagens A e B mostram que diferentes configurações produzem máscaras com proporções distintas de primeiro plano.

No M2.2, a análise por componentes conexos permite medir áreas, caixas delimitadoras e centroides, além de comparar os efeitos das operações morfológicas. Nos experimentos realizados, a quantidade de componentes diminuiu consideravelmente após o fechamento seguido da abertura, enquanto a área branca aumentou.

Os resultados demonstram que o processamento morfológico altera a estrutura das máscaras e pode reduzir ruídos, preencher lacunas ou unir regiões. Entretanto, essas alterações também podem modificar os objetos de interesse. Por isso, a interpretação deve considerar conjuntamente as máscaras, a quantidade de componentes, suas áreas e os parâmetros utilizados.

A verificação da soma das áreas dos componentes confirmou a consistência das contagens de pixels nos arquivos analisados. Ainda assim, sem máscaras de referência, não é possível afirmar que os resultados representam uma segmentação perfeita dos objetos reais.

## 7. Como reproduzir os resultados

Os comandos a seguir devem ser executados no terminal, a partir da raiz do projeto, com o ambiente virtual ativado e as dependências instaladas.

### 7.1. Consultar a interface de linha de comando

`python -m pdi_lab --help`

### 7.2. Executar a segmentação por limiar fixo

Imagem A:

`pdi_lab --input images/input/imagem_a.png --output results/imagem_a_fixed.png --operation segment --method fixed --threshold 120`

Imagem B:

`pdi_lab --input images/input/imagem_b.png --output results/imagem_b_fixed.png --operation segment --method fixed --threshold 120`

### 7.3. Executar a segmentação adaptativa

Imagem A:

`pdi_lab --input images/input/imagem_a.png --output results/imagem_a_adaptive.png --operation segment --method adaptive --block-size 21 --constant 5`

Imagem B:

`pdi_lab --input images/input/imagem_b.png --output results/imagem_b_adaptive.png --operation segment --method adaptive --block-size 21 --constant 5`

### 7.4. Executar a análise de componentes e a morfologia

Os comandos abaixo utilizam as máscaras invertidas geradas para a análise.

Imagem A:

`pdi_lab --input results/invertidas/imagem_a_fixed.png --output results/imagem_a --operation analyze --connectivity 8 --min-area 20 --kernel-size 3`

Imagem B:

`pdi_lab --input results/invertidas/imagem_b_fixed.png --output results/imagem_b --operation analyze --connectivity 8 --min-area 20 --kernel-size 3`

A análise gera arquivos com as máscaras inicial e final, os resultados intermediários da morfologia, os dados dos componentes em CSV, a visualização dos componentes e o resumo em JSON.

### 7.5. Executar os testes

`python -m pytest -v`

Os resultados podem ser comparados com as tabelas deste relatório. Para manter a rastreabilidade, é importante utilizar as mesmas imagens e os mesmos parâmetros descritos na configuração dos experimentos.
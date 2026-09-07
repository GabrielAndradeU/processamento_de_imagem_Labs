# REPORT.md — Mini Relatório Técnico

## Objetivo

Implementar, sem uso de funções prontas de alto nível, as operações
fundamentais de representação de imagens digitais por meio de acesso
direto aos pixels: inspeção de propriedades da imagem, cópia manual,
separação de canais de cor, conversão para níveis de cinza (por média
simples e por média ponderada) e quantização em diferentes quantidades
de níveis (16, 8, 4 e 2). O objetivo é consolidar a relação entre
dimensões, canais, intensidade e resolução radiométrica de uma imagem
digital.

## Operações implementadas

Todas implementadas em `src/pdi_lab/operations.py`, com percurso
explícito de pixels (`for y in range(altura): for x in range(largura)`),
sem uso de `img.copy()`, `cv2.split()`, `cv2.cvtColor(..., COLOR_BGR2GRAY)`
ou quantização vetorizada pronta.

1. **Inspeção da imagem** (`inspecionar_imagem`) — calcula largura,
   altura, número de canais, tipo, quantidade de pixels, e mínimo,
   máximo e média (por canal, se colorida), tudo por acumulação
   manual durante o percurso pixel a pixel.

2. **Cópia manual** (`copia_manual`) — aloca uma matriz nova
   (`np.zeros`) e copia cada pixel/canal individualmente.

3. **Separação manual dos canais** (`separar_canais`) — gera três
   imagens (`b`, `g`, `r`), cada uma preservando apenas o canal
   correspondente e zerando os demais. Segue a ordem BGR nativa do
   OpenCV.

4. **Conversão manual para níveis de cinza**
   (`escala_cinza_media_simples`, `escala_cinza_media_ponderada`) —
   implementa `g = (R+G+B)/3` e `g = 0,299R + 0,587G + 0,114B`,
   com arredondamento (`round`) e limitação ao intervalo [0, 255]
   antes de converter para `uint8`.

5. **Quantização** (`quantizar`) — reduz uma imagem em escala de
   cinza para `n` níveis, dividindo o intervalo [0, 255] em `n`
   faixas iguais e mapeando cada uma para um valor representante
   reescalado de volta a [0, 255]. Implementado para 16, 8, 4 e 2
   níveis.

## Testes

Implementados em `tests/test_manual.py`, sobre uma imagem sintética
4×4 (`images/input/synthetic.png`) construída com valores conhecidos
para permitir conferência manual (preto puro, branco puro, azul puro,
vermelho puro, valores ímpares para testar arredondamento, e valores
próximos aos limites 0 e 255).

Casos cobertos:

- **Cópia exata dos pixels**: compara a cópia pixel a pixel com o
  original e garante que não é a mesma referência de memória.
- **Ordem dos canais**: verifica que um pixel azul puro em BGR
  `(255,0,0)` fica isolado corretamente em `channel_b` e zerado nos
  demais, e o mesmo para um pixel vermelho puro.
- **As duas versões de escala de cinza**: confere valores calculados
  manualmente (ex.: pixel BGR `(255,0,0)` → 85 na média simples e 29
  na ponderada) e garante que, quando R=G=B, as duas versões
  coincidem, mas divergem em pixels saturados em um único canal.
- **Quantidade de níveis após quantização**: garante que o número de
  valores únicos na saída nunca excede a quantidade de níveis pedida.
- **Comportamento nos limites**: com 2 níveis, confirma que os únicos
  valores possíveis na saída são 0 e 255.
- **Quantidade de níveis inválida**: confirma que `quantizar` levanta
  exceção para `niveis=1`.

Todos os 7 testes passam na versão atual do código.

## Resultados

Processando a imagem sintética 4×4:

- **Inspeção**: 4×4 pixels, 3 canais, `uint8`; médias por canal
  B=98,31 / G=110,63 / R=118,75.
- **Cópia**: diferença máxima de 0 entre original e cópia (idêntica).
- **Separação de canais**: `channel_b.png`, `channel_g.png`,
  `channel_r.png` gerados corretamente, cada um preservando apenas o
  canal correspondente.
- **Escala de cinza**: `gray_average.png` e `gray_weighted.png`
  gerados; diferença média entre as duas versões de 12,88 nesta
  imagem — maior nos pixels de cor saturada (ex.: azul e vermelho
  puros), nula nos pixels acromáticos (onde R=G=B).
- **Quantização**: `quant_16.png`, `quant_8.png`, `quant_4.png` e
  `quant_2.png` gerados, todos com a quantidade de níveis únicos
  dentro do limite esperado; `quant_2.png` resulta apenas em preto
  (0) e branco (255).

Todas as 10 saídas mínimas pedidas no enunciado foram geradas em
`images/output/`.

## Análise técnica

**1. Diferença entre resolução espacial e resolução radiométrica.**
Resolução espacial é a quantidade de pixels que representam a imagem
(largura × altura) e determina o nível de detalhe geométrico.
Resolução radiométrica é a quantidade de níveis de intensidade
disponíveis por pixel (256 em uma imagem de 8 bits) e determina a
sutileza das variações de tom. A atividade de quantização atua apenas
sobre a resolução radiométrica, sem alterar a espacial.

**2. Por que a média ponderada produz resultado diferente da média
simples.** O olho humano não tem sensibilidade igual às três cores
primárias: é mais sensível ao verde, seguido do vermelho, e menos
sensível ao azul. A média simples pesa os três canais igualmente
(1/3 cada), enquanto a ponderada (0,299R + 0,587G + 0,114B) reflete
essa sensibilidade perceptual. Por isso, pixels saturados em um único
canal (como o azul puro testado) apresentam diferença grande entre as
duas versões, enquanto pixels acromáticos (R=G=B) não apresentam
diferença nenhuma.

**3. O que ocorre visualmente quando a quantidade de níveis é
reduzida.** A imagem perde gradações suaves e passa a apresentar
"faixas" de intensidade constante — efeito de posterização/banding.
Com 2 níveis, a imagem se torna essencialmente preto-e-branco puro,
sem tons intermediários.

**4. Em quais regiões a perda de informação fica mais evidente.** Em
regiões de gradiente suave (sombras, degradês, superfícies com
iluminação gradual), que dependiam de muitos níveis intermediários
para representar a transição. Em regiões de alto contraste, a perda é
menos perceptível, pois esses pixels já tendiam para os extremos
mesmo com poucos níveis.

**5. Como o tipo e o número de canais interferem no acesso a um
pixel.** Em uma imagem em escala de cinza (1 canal), um pixel é
acessado com dois índices (`img[y, x]`) e retorna um escalar. Em uma
imagem colorida (3 canais), é necessário um terceiro índice para o
canal (`img[y, x, c]`), e a ordem armazenada pelo OpenCV é BGR — não
RGB —, o que precisa ser considerado em qualquer fórmula que use R, G
e B explicitamente. O tipo `uint8` também exige atenção: somas
intermediárias podem ultrapassar 255, então os cálculos são feitos em
`int`/`float` antes de arredondar e limitar (`clamp`) o resultado de
volta ao intervalo [0, 255].

## Limitações

- A quantização assume uma imagem de entrada de 8 bits (`uint8`,
  intervalo [0, 255]); imagens com outra profundidade de bits não são
  tratadas.
- Imagens com canal alpha (4 canais) não são suportadas — apenas 1
  canal (cinza) ou 3 canais (BGR).
- A estratégia de quantização usada (faixas de tamanho igual, com
  representante reescalado) é uma entre várias possíveis; não
  implementamos, por exemplo, quantização baseada em truncamento
  direto de bits menos significativos, que produziria uma distribuição
  de níveis diferente.
- Os loops pixel a pixel em Python puro são intencionalmente não
  vetorizados (conforme exigido pelo enunciado), o que os torna lentos
  para imagens grandes — aceitável para fins didáticos, mas não para
  uso em produção.
- Os testes cobrem uma imagem sintética pequena; não há testes
  automatizados sobre imagens reais além da execução manual do
  `main.py`.

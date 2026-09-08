# Análise da Carga Elétrica no Brasil

Este projeto analisa o comportamento da carga elétrica dos subsistemas Norte, Nordeste, Sul e Sudeste entre 2000 e 2025.

A ideia é entender como a demanda por energia mudou ao longo dos anos, quais padrões aparecem dentro dos meses, semanas e horários e quais características precisam ser consideradas em uma série temporal desse tipo.

O projeto possui caráter descritivo e estatístico. Não foram utilizados modelos de Machine Learning nem técnicas de previsão.

## Fonte dos Dados

Os dados foram disponibilizados pelo [Operador Nacional do Sistema Elétrico — ONS](https://dados.ons.org.br/dataset/curva-carga), por meio do conjunto Curva de Carga Horária.

Cada linha representa a carga média registrada em um subsistema durante uma hora, medida em MWmed.

| Coluna | Descrição |
|---|---|
| id_subsistema | Sigla do subsistema elétrico |
| nom_subsistema | Nome do subsistema |
| din_instante | Data e hora de referência |
| val_cargaenergiahomwmed | Carga elétrica média no período, medida em MWmed |

O recorte utilizado possui:

- dados entre janeiro de 2000 e dezembro de 2025;
- frequência horária;
- quatro subsistemas: Norte, Nordeste, Sul e Sudeste;
- 911.608 registros após a consolidação dos arquivos anuais.

## Objetivo

O objetivo principal é compreender a evolução e os padrões da carga elétrica brasileira ao longo de 26 anos.

Durante a análise, foram investigadas as seguintes perguntas:

- Como a carga elétrica evoluiu ao longo dos anos?
- Quais subsistemas possuem as maiores cargas?
- Quais regiões apresentaram o maior crescimento proporcional?
- Existem padrões mensais, semanais e horários?
- O comportamento muda entre dias úteis e finais de semana?
- Como os subsistemas participam da carga total do SIN?
- A série diária possui tendência, sazonalidade e autocorrelação?
- A série pode ser considerada estacionária?

## Etapas do Projeto

O desenvolvimento foi dividido em quatro notebooks.

| Notebook | Etapa | Descrição |
|---|---|---|
| [1.data_understanding.ipynb](notebooks/1.data_understanding.ipynb) | Entendimento dos dados | Análise inicial do arquivo de 2025 para compreender a estrutura, as colunas e os subsistemas disponíveis. |
| [2.data_consolidation.ipynb](notebooks/2.data_consolidation.ipynb) | Consolidação e qualidade | União do histórico, correção dos tipos, análise de valores ausentes, duplicidades e continuidade temporal. |
| [3.exploratory_analysis.ipynb](notebooks/3.exploratory_analysis.ipynb) | Análise exploratória | Estudo da evolução histórica, distribuição, sazonalidade, perfis regionais, valores extremos e correlações. |
| [4.time_series_diagnostics.ipynb](notebooks/4.time_series_diagnostics.ipynb) | Diagnóstico temporal | Construção da série diária, decomposição, autocorrelação, testes de estacionariedade e análise dos resíduos. |

## Visualizações

Os gráficos exploratórios foram desenvolvidos com Plotly. Dessa forma, é possível aproximar períodos, selecionar intervalos e consultar os valores diretamente nos notebooks.

O Matplotlib foi mantido apenas nos gráficos de autocorrelação gerados pelo Statsmodels. Nesses casos, foi utilizado o estilo ggplot para manter uma aparência próxima dos demais gráficos do projeto.

## Qualidade dos Dados

Durante a consolidação, foram identificados alguns pontos importantes:

- a coluna de carga estava armazenada como texto entre 2000 e 2024;
- 259 campos vazios passaram a ser reconhecidos como valores ausentes depois da conversão numérica;
- uma carga igual a zero no subsistema Sul foi tratada como ausente;
- não foram encontrados registros duplicados;
- 260 cargas nulas estavam presentes em linhas existentes;
- 104 linhas horárias não existiam na base;
- parte das ausências estava relacionada ao início do horário de verão;
- três dias completos não possuíam carga válida para o cálculo do SIN.

Mesmo com essas ocorrências, a série horária do SIN apresentou cobertura de 99,960%.

Na série diária, os três dias completamente vazios foram estimados pela média do mesmo dia da semana anterior e posterior. Os dias com 23 horas foram mantidos sem alteração, pois correspondem às mudanças para o horário de verão.

## Principais Resultados

### Evolução histórica

- A carga média anual do SIN cresceu 95,06% entre 2000 e 2025.
- A taxa média composta de crescimento foi de 2,71% ao ano.
- O Sudeste permaneceu como o subsistema de maior carga durante todo o período.
- O Norte apresentou o maior crescimento proporcional, com aumento de 234,21%.
- A participação média do Sudeste no SIN caiu de 62,98% para 55,44%.
- A participação do Norte aumentou de 6,18% para 10,57%.

### Padrões temporais

- Fevereiro e março apresentaram as maiores cargas em relação à média de cada ano.
- Junho e julho ficaram entre os meses de menor carga.
- A carga diminuiu nos finais de semana, principalmente aos domingos.
- Nos dias úteis, a carga cresceu pela manhã e permaneceu elevada durante a tarde e o início da noite.
- O maior índice horário do SIN apareceu às 19h.
- Os subsistemas apresentaram perfis mensais e horários diferentes.

### Diagnóstico da série temporal

- A média e a variabilidade da série diária mudaram ao longo do tempo.
- A decomposição identificou componentes semanal e anual, além da tendência.
- A série original apresentou forte autocorrelação, principalmente em intervalos de sete dias.
- Os testes ADF e KPSS indicaram que a série original não é estacionária.
- A primeira diferença foi classificada como estacionária pelos dois testes.
- Os resíduos da decomposição ainda apresentaram valores extremos e autocorrelação.

## Tecnologias Utilizadas

- Python
- pandas
- NumPy
- Plotly
- Matplotlib
- Statsmodels
- PyArrow
- Requests
- JupyterLab

## Estrutura do Repositório

- data/raw: arquivos anuais coletados no formato Parquet;
- data/processed: dataset histórico consolidado;
- notebooks: notebooks de entendimento, consolidação, análise exploratória e diagnóstico temporal;
- src/collect.py: script responsável pela coleta dos arquivos no portal do ONS;
- requirements.txt: dependências utilizadas no projeto.

As pastas de dados não são versionadas no GitHub. Os arquivos podem ser coletados novamente pelo script disponível em src.

## Como Executar o Projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/nobertosousac/brazil-electric-load-analysis.git
cd brazil-electric-load-analysis
```

### 2. Criar e ativar o ambiente virtual

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Coletar os dados

Para baixar todo o período entre 2000 e 2025:

```bash
python src/collect.py
```

Também é possível escolher um intervalo:

```bash
python src/collect.py --start 2010 --stop 2025
```

Ou informar anos específicos:

```bash
python src/collect.py --years 2020 2021 2022
```

### 5. Abrir os notebooks

```bash
jupyter lab
```

Depois, execute os notebooks na ordem numérica. O segundo notebook cria o arquivo consolidado utilizado nas etapas seguintes.

## Limitações

- A abrangência do SIN e a metodologia dos dados mudaram durante o período analisado.
- A entrada de novas cargas no sistema pode afetar comparações entre anos distantes.
- O ciclo anual foi aproximado por um período de 365 dias.
- Os três dias preenchidos na série diária representam estimativas.
- Informações como temperatura, feriados, atividade econômica e acontecimentos operacionais não fazem parte da base.
- Os resultados descrevem o comportamento histórico e não devem ser interpretados como previsão.

## Autor

Projeto desenvolvido por **Noberto Sousa**.

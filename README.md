# 💰 Análise de Títulos Financeiros

Data app desenvolvido em **Python + Streamlit** para análise de títulos **quitados** e **em aberto** do setor financeiro, a partir de relatórios exportados do ERP **Consinco (TOTVS)**.

A aplicação transforma relatórios com milhares de linhas em indicadores e gráficos interativos, respondendo as perguntas recorrentes do contas a pagar:

- **Olhando para trás:** quanto foi pago no período, quais fornecedores concentram o desembolso, em quais dias ele se acumula e onde estão os juros.
- **Olhando para frente:** quanto está vencido, quanto vence nos próximos dias e como o desembolso progride até o fim do período.

---

## ✨ Funcionalidades

### 📂 Importação de dados
- Seletor de análise na barra lateral: **Títulos Quitados** ou **Títulos Abertos**
- Upload com arrastar e soltar, aceitando **XLSX**, **CSV** e **TXT** (PDF em desenvolvimento)
- Detecção automática de codificação (`UTF-8`, `CP1252`, `Latin-1`) e separador em arquivos de texto
- Aviso quando o relatório importado não corresponde à análise escolhida
- Filtros por **período**, **empresa** e **espécie**, aplicados a todos os indicadores e gráficos

### 📊 Títulos Quitados

**Aba Cartões** — totais gerais do período:

| Indicador | Indicador |
|---|---|
| Total Geral Original | Total Geral Abatimento |
| Total Geral Multa | Total Geral Compensação |
| Total Geral Juros | Total Geral Pago |
| Total Geral Desconto | Total Geral Líquido |

Além da quantidade de títulos e do valor líquido médio por título.

**Aba Métricas**
- Evolução dos gastos no tempo, com granularidade automática (mensal ou semanal, conforme o intervalo da base)
- Top 10 pessoas por gasto
- Tabela hierárquica de concentração por semana e dia (ou mês e semana)
- Top 10 pessoas por juros pagos
- Top 10 espécies de título
- Comparativo entre as empresas do grupo

Seletores permitem trocar o valor analisado (Líquido, Pago, Original etc.) e a data de referência (Quitação, Emissão, Vencimento ou Movimento).

### 📋 Títulos em Aberto

**Aba Resumo**
- Composição da carteira: Original, Em Aberto, Desconto e Líquido
- Títulos com pagamento parcial
- Vencidos × a vencer, em valor e quantidade
- Desembolso dos próximos 7 dias
- Valor médio por título e maior título, com alerta quando um único título concentra mais de 10% da carteira

**Aba Vencimentos**
- **Progressão do desembolso:** barras com o valor de cada dia de vencimento e linha com o total acumulado, com os dias vencidos destacados e uma marcação na data do relatório
- Distribuição por faixa de prazo (vencido, vence hoje, 1 a 7, 8 a 15, 16 a 30 e acima de 30 dias)
- Concentração por dia da semana do vencimento

### 🗂️ Aba Dados
Disponível nas duas análises: a base tratada, com busca e ordenação.

---

## 🛠️ Tecnologias

| Biblioteca | Uso |
|---|---|
| [Streamlit](https://streamlit.io/) | Interface web |
| [pandas](https://pandas.pydata.org/) | Leitura, tratamento e agregação dos dados |
| [NumPy](https://numpy.org/) | Operações numéricas |
| [Plotly](https://plotly.com/python/) | Gráficos interativos |
| [openpyxl](https://openpyxl.readthedocs.io/) | Leitura de arquivos XLSX |
| [pdfplumber](https://github.com/jsvine/pdfplumber) | Extração de tabelas em PDF (em desenvolvimento) |

---

## 🏗️ Arquitetura

O projeto é dividido em duas partes:

**Núcleo compartilhado (`src/core/`)** — o que vale para qualquer relatório: leitura de arquivos, tratamento, filtros, rankings, agregações temporais, gráficos e componentes de interface.

**Módulos de análise (`src/analises/`)** — uma pasta por análise, com o layout do seu relatório, os cálculos e as telas.

A ligação entre as duas partes é o objeto **`Layout`**, que descreve um relatório: como renomear suas colunas para o vocabulário padronizado, quais são as datas, os valores e as colunas obrigatórias, e qual data serve de referência para filtros e gráficos. O núcleo recebe essas regras por parâmetro e não conhece nenhuma análise em particular — adicionar um novo relatório é declarar um layout, não duplicar código.

```
titulos_financeiro_app/
│
├── app.py                          # Roteia a análise escolhida
├── requirements.txt
├── README.md
│
├── .streamlit/config.toml          # Tema e configurações do Streamlit
├── config/settings.py              # Vocabulário de colunas e parâmetros gerais
│
├── src/
│   ├── core/                       # NÚCLEO COMPARTILHADO
│   │   ├── layout.py               #   Descrição de um relatório
│   │   ├── extraction/             #   Leitura por extensão (XLSX, CSV, TXT, PDF)
│   │   ├── processing/             #   Tratamento, validação e filtros
│   │   ├── analytics/              #   Agregações temporais e rankings
│   │   ├── visualization/          #   Gráficos
│   │   └── ui/                     #   Barra lateral e componentes
│   │
│   ├── analises/
│   │   ├── registro.py             #   Análises disponíveis
│   │   ├── quitados/layout.py
│   │   └── abertos/                #   Layout, preparo, indicadores e abas
│   │
│   └── ui/                         # Abas dos títulos quitados
│
├── assets/
├── data/                           # Não versionada
├── notebooks/
└── tests/
```

Fluxo dos dados:

```
Análise escolhida → Upload → Leitura → Tratamento (pelo layout)
    → Validação → Preparo → Filtros → Indicadores e Gráficos
```

---

## 🚀 Instalação e execução

**Pré-requisito:** Python 3.10 ou superior.

### 1. Clonar o repositório

```bash
git clone https://github.com/oneriodev/titulos_financeiro_app.git
cd titulos_financeiro_app
```

### 2. Criar e ativar o ambiente virtual

**Linux / macOS**
```bash
python3 -m venv venv
source venv/bin/activate
```

> No Ubuntu/Debian/Mint, caso o `venv` não esteja disponível: `sudo apt install python3-venv`

**Windows (PowerShell)**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Executar

```bash
streamlit run app.py
```

A aplicação abre no navegador em `http://localhost:8501`.

---

## 📋 Formato esperado dos dados

Os nomes das colunas de cada relatório ficam no layout da sua análise (`src/analises/<analise>/layout.py`) e são convertidos para um vocabulário padronizado logo após a leitura. Para adaptar a aplicação a outro layout do Consinco, basta declarar um novo layout.

**Títulos quitados**

| Tipo | Colunas |
|---|---|
| Identificação | `Pessoa`, `Espécie`, `Nro Empresa` |
| Datas | `Dt. Emissão`, `Vencimento Programado`, `Dt. Movimento`, `Dt. Quitação` |
| Valores | `Vlr Original`, `Vlr Multa`, `Vlr Juros`, `Vlr Desconto`, `Vlr Abatimento`, `Vlr Compensação`, `Vlr Pago`, `Vlr Liquido` |

Relação validada entre as colunas:

```
Vlr Liquido = Vlr Pago + Vlr Juros − Vlr Desconto − Vlr Compensação
```

**Títulos em aberto**

| Tipo | Colunas |
|---|---|
| Identificação | `Pessoa`, `Espécie`, `Empr.` |
| Datas | `Dt. Emissão`, `Dt. Movimento`, `Vencimento Programado` |
| Valores | `Vlr Original`, `Valor Aberto`, `Desconto`, `Valor Líquido`, `Multa`, `Juros`, `Taxa Adm.` |
| Apoio | `Dias de Atraso` |

Relação validada entre as colunas:

```
Valor Líquido = Valor Aberto − Desconto
```

### Data de referência dos títulos em aberto

O relatório não informa a data em que foi extraído, e sem ela não é possível separar o que está vencido do que ainda vai vencer. A aplicação deduz essa data a partir dos próprios títulos atrasados:

```
data de extração = Vencimento Programado + Dias de Atraso
```

Em alguns títulos o Consinco calcula o atraso a partir de outra referência (como o vencimento original de um título reprogramado), o que empurra o resultado para depois da data real. Por isso a aplicação usa a **menor** data obtida. Sem nenhum título atrasado no arquivo, usa-se a data atual.

---

## 🔒 Privacidade dos dados

Relatórios financeiros contêm informações sensíveis da empresa e de fornecedores. Por isso:

- Planilhas e arquivos de texto **não são versionados**, em nenhuma pasta do projeto (ver `.gitignore`)
- O upload é processado **em memória**, sem gravação em disco
- Nenhuma base de dados real ou fictícia acompanha este repositório

---

## 👤 Autor

**Onerio**
Engenharia de Software · Análise e Desenvolvimento de Sistemas

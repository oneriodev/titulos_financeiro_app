# 💰 Análise de Títulos Financeiros

Data app desenvolvido em **Python + Streamlit** para análise de títulos **abertos e quitados** do setor financeiro, a partir de relatórios exportados do ERP **Consinco (TOTVS)**.

A aplicação transforma um relatório com milhares de linhas em indicadores e gráficos interativos, respondendo perguntas recorrentes do contas a pagar: quanto foi pago no período, quais fornecedores concentram os gastos, em quais dias o desembolso se acumula e onde estão os juros.

---

## ✨ Funcionalidades

### 📂 Importação de dados
- Upload pela barra lateral, com arrastar e soltar
- Formatos aceitos: **XLSX**, **CSV** e **TXT** (leitura de PDF em desenvolvimento)
- Detecção automática de codificação (`UTF-8`, `CP1252`, `Latin-1`) e separador em arquivos de texto
- Validação das colunas obrigatórias antes de qualquer cálculo

### 📊 Aba Cartões
Totais gerais do conjunto de dados:

| Indicador | Indicador |
|---|---|
| Total Geral Original | Total Geral Abatimento |
| Total Geral Multa | Total Geral Compensação |
| Total Geral Juros | Total Geral Pago |
| Total Geral Desconto | Total Geral Líquido |

Além da quantidade de títulos e do valor líquido médio por título.

### 📈 Aba Métricas
- **Evolução dos gastos no tempo**, com granularidade automática: mensal quando a base abrange vários meses, semanal quando abrange um único mês
- **Top 10 pessoas** (fornecedores/favorecidos) com maiores gastos
- **Tabela hierárquica** de concentração de gastos por semana e dia (ou mês e semana)
- **Participação nos juros** por pessoa, em gráfico de pizza
- **Top espécies** de título por gasto
- **Gastos por empresa**, ordenados do maior para o menor

Seletores permitem trocar o valor analisado (Líquido, Pago, Original etc.) e a data de referência (Quitação, Emissão, Vencimento ou Movimento).

### 🗂️ Aba Dados
Visualização da base tratada, com busca e ordenação.

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

## 📁 Estrutura do projeto

O código é organizado em camadas, para que uma mudança no formato do relatório afete apenas a camada de extração, sem quebrar cálculos e gráficos.

```
titulos_financeiro_app/
│
├── app.py                      # Ponto de entrada da aplicação
├── requirements.txt
├── README.md
│
├── .streamlit/
│   └── config.toml             # Tema e configurações do Streamlit
│
├── config/
│   └── settings.py             # Constantes: colunas, formatos, parâmetros
│
├── src/
│   ├── extraction/             # 1. Leitura dos arquivos
│   │   ├── file_reader.py      #    Roteador por extensão (XLSX, CSV, TXT)
│   │   ├── txt_reader.py
│   │   └── pdf_reader.py
│   │
│   ├── processing/             # 2. Tratamento
│   │   ├── cleaning.py         #    Tipos, datas, valores e colunas derivadas
│   │   └── schema.py           #    Validação da estrutura
│   │
│   ├── analytics/              # 3. Cálculos
│   │   ├── kpis.py             #    Totais dos cartões
│   │   └── metrics.py          #    Agregações dos gráficos
│   │
│   ├── visualization/          # 4. Gráficos
│   │   └── charts.py
│   │
│   └── ui/                     # 5. Interface
│       ├── sidebar.py
│       ├── tab_cards.py
│       ├── tab_metrics.py
│       └── components.py
│
├── assets/
├── data/                       # Não versionada
│   ├── raw/
│   └── processed/
├── notebooks/
└── tests/
```

Fluxo dos dados:

```
Upload → Extração → Tratamento → Validação → Cálculos → Gráficos e Cartões
```

---

## 🚀 Instalação e execução

**Pré-requisito:** Python 3.10 ou superior.

### 1. Clonar o repositório

```bash
git clone git@github.com:SEU_USUARIO/titulos_financeiro_app.git
cd titulos_financeiro_app
```

### 2. Criar e ativar o ambiente virtual

**Linux / macOS**
```bash
python3 -m venv venv
source venv/bin/activate
```

> No Ubuntu/Debian, caso o `venv` não esteja disponível: `sudo apt install python3-venv`

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

O arquivo importado deve conter, no mínimo, as colunas abaixo, conforme a exportação padrão do Consinco:

| Tipo | Colunas |
|---|---|
| Identificação | `Pessoa`, `Espécie`, `Nro Empresa`, `Título` |
| Datas | `Dt. Emissão`, `Vencimento Programado`, `Dt. Movimento`, `Dt. Quitação` |
| Valores | `Vlr Original`, `Vlr Multa`, `Vlr Juros`, `Vlr Desconto`, `Vlr Abatimento`, `Vlr Compensação`, `Vlr Pago`, `Vlr Liquido` |

Os nomes das colunas ficam centralizados em `config/settings.py`. Para adaptar a aplicação a outro layout de relatório, basta ajustar esse arquivo.

### Regra do valor líquido

Os totais são somados diretamente das colunas do relatório, sem recálculo. No layout do Consinco, a relação validada entre as colunas é:

```
Vlr Liquido = Vlr Pago + Vlr Juros − Vlr Desconto − Vlr Compensação
```

---

## 🔒 Privacidade dos dados

Relatórios financeiros contêm informações sensíveis da empresa e de fornecedores. Por isso:

- A pasta `data/` e arquivos de planilha **não são versionados** (ver `.gitignore`)
- O upload é processado **em memória**, sem gravação em disco
- Nenhuma base de dados real ou fictícia acompanha este repositório

---

## 👤 Autor

**Onerio**
Engenharia de Software · Análise e Desenvolvimento de Sistemas

"""
Configurações e constantes centrais do projeto.
Nomes de colunas confirmados a partir da exportação real do Consinco.
"""

# ---------------------------------------------------------------------
# Aplicação
# ---------------------------------------------------------------------
APP_TITLE = "Análise de Títulos Financeiros"
APP_ICON = "💰"
LAYOUT = "wide"
SUBTITULO = "Análise de títulos abertos e quitados — ERP Consinco (TOTVS)"

# ---------------------------------------------------------------------
# Upload
# ---------------------------------------------------------------------
EXTENSOES_ACEITAS = ["xlsx", "csv", "txt", "pdf"]
TAMANHO_MAX_MB = 50

# ---------------------------------------------------------------------
# Leitura de arquivos de texto (TXT e CSV)
# ---------------------------------------------------------------------
ENCODINGS_TENTATIVAS = ["utf-8", "cp1252", "latin-1"]
SEPARADORES_TENTATIVAS = ["\t", ";", "|", ","]

# ---------------------------------------------------------------------
# Colunas de identificação
# ---------------------------------------------------------------------
COLUNA_PESSOA = "Pessoa"
COLUNA_ESPECIE = "Espécie"
COLUNA_TITULO = "Título"
COLUNA_EMPRESA = "Nro Empresa"
COLUNA_DEPOSITARIO = "Depositário"

# ---------------------------------------------------------------------
# Colunas de data
# ---------------------------------------------------------------------
COLUNA_DT_EMISSAO = "Dt. Emissão"
COLUNA_DT_VENCIMENTO = "Vencimento Programado"
COLUNA_DT_MOVIMENTO = "Dt. Movimento"
COLUNA_DT_QUITACAO = "Dt. Quitação"

COLUNAS_DATAS = [
    COLUNA_DT_EMISSAO,
    COLUNA_DT_VENCIMENTO,
    COLUNA_DT_MOVIMENTO,
    COLUNA_DT_QUITACAO,
]

# Eixo temporal padrão dos gráficos
COLUNA_DATA_PADRAO = COLUNA_DT_QUITACAO

# ---------------------------------------------------------------------
# Colunas de valores — chave interna -> nome no arquivo
# ---------------------------------------------------------------------
COLUNAS_VALORES = {
    "original": "Vlr Original",
    "multa": "Vlr Multa",
    "juros": "Vlr Juros",
    "desconto": "Vlr Desconto",
    "abatimento": "Vlr Abatimento",
    "compensacao": "Vlr Compensação",
    "pago": "Vlr Pago",
    "liquido": "Vlr Liquido",
}

# Rótulos exibidos nos cartões
ROTULOS_CARTOES = {
    "original": "Total Geral Original",
    "multa": "Total Geral Multa",
    "juros": "Total Geral Juros",
    "desconto": "Total Geral Desconto",
    "abatimento": "Total Geral Abatimento",
    "compensacao": "Total Geral Compensação",
    "pago": "Total Geral Pago",
    "liquido": "Total Geral Líquido",
}

# Coluna usada como valor de referência nas métricas
COLUNA_VALOR_PADRAO = COLUNAS_VALORES["liquido"]

# ---------------------------------------------------------------------
# Colunas auxiliares (descartadas ou derivadas no tratamento)
# ---------------------------------------------------------------------
COLUNAS_DESCARTADAS = ["Column1"]
COLUNA_ANO_MES = "Ano-Mês"
COLUNA_DIA_SEMANA = "Dia da Semana"

DIAS_SEMANA = {
    0: "Segunda",
    1: "Terça",
    2: "Quarta",
    3: "Quinta",
    4: "Sexta",
    5: "Sábado",
    6: "Domingo",
}

# Mínimo necessário para a aplicação funcionar
COLUNAS_OBRIGATORIAS = [
    COLUNA_PESSOA,
    COLUNA_ESPECIE,
    COLUNA_DT_QUITACAO,
] + list(COLUNAS_VALORES.values())

# ---------------------------------------------------------------------
# Formatos e parâmetros de análise
# ---------------------------------------------------------------------
FORMATO_DATA = "%d/%m/%Y"
TOP_N = 5

# ---------------------------------------------------------------------
# Parâmetros dos gráficos
# ---------------------------------------------------------------------
TOP_N_PESSOAS = 10
TOP_N_ESPECIES = 10
TOP_N_PIZZA = 8

COR_PRIMARIA = "#1F4E79"
COR_SECUNDARIA = "#4E88C7"
ESCALA_CORES = "Blues"
ALTURA_GRAFICO = 420
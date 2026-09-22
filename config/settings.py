"""
Configurações e constantes centrais do projeto.

As colunas usam um vocabulário padronizado. Cada relatório do Consinco
é renomeado para esse vocabulário logo após a leitura, de modo que o
restante do código não depende dos nomes originais de cada exportação.
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
# Vocabulário padronizado — identificação
# ---------------------------------------------------------------------
COLUNA_PESSOA = "Pessoa"
COLUNA_ESPECIE = "Espécie"
COLUNA_EMPRESA = "Empresa"
COLUNA_DIAS_ATRASO = "Dias de Atraso"

# ---------------------------------------------------------------------
# Vocabulário padronizado — datas
# ---------------------------------------------------------------------
COLUNA_DT_EMISSAO = "Dt. Emissão"
COLUNA_DT_VENCIMENTO = "Dt. Vencimento"
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
# Vocabulário padronizado — valores (chave interna -> nome padronizado)
# ---------------------------------------------------------------------
COLUNAS_VALORES = {
    "original": "Vlr Original",
    "multa": "Vlr Multa",
    "juros": "Vlr Juros",
    "desconto": "Vlr Desconto",
    "abatimento": "Vlr Abatimento",
    "compensacao": "Vlr Compensação",
    "pago": "Vlr Pago",
    "liquido": "Vlr Líquido",
}
COLUNA_VLR_ABERTO = "Vlr Aberto"
COLUNA_VLR_TAXA_ADM = "Vlr Taxa Adm."

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

# ---------------------------------------------------------------------
# Parâmetros dos gráficos
# ---------------------------------------------------------------------
TOP_N_PESSOAS = 10
TOP_N_ESPECIES = 10
TOP_N_JUROS = 10

COR_PRIMARIA = "#4E88C7"
ESCALA_CORES = "Blues"
ALTURA_GRAFICO = 420
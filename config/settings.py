"""
Configurações e constantes centrais do projeto.
Qualquer ajuste de nome de coluna ou parâmetro deve ser feito aqui.
"""

# ---------------------------------------------------------------------
# Aplicação
# ---------------------------------------------------------------------
APP_TITLE = "Análise de Títulos Financeiros"
APP_ICON = "💰"
LAYOUT = "wide"

# ---------------------------------------------------------------------
# Upload
# ---------------------------------------------------------------------
EXTENSOES_ACEITAS = ["pdf", "csv", "xlsx"]

# ---------------------------------------------------------------------
# Colunas do relatório (PROVISÓRIO: ajustar após analisar o PDF do Consinco)
# ---------------------------------------------------------------------
COLUNA_DATA = "Data"
COLUNA_ESPECIE = "Espécie"
COLUNA_PESSOA = "Pessoa"

# Chave interna -> nome exibido no cartão
COLUNAS_VALORES = {
    "original": "Original",
    "multa": "Multa",
    "juros": "Juros",
    "desconto": "Desconto",
    "abatimento": "Abatimento",
    "compensacao": "Compensação",
    "pago": "Pago",
    "liquido": "Líquido",
}

# ---------------------------------------------------------------------
# Formatos e parâmetros de análise
# ---------------------------------------------------------------------
FORMATO_DATA = "%d/%m/%Y"
TOP_N = 5
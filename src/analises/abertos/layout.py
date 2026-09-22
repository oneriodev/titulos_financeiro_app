"""
Layout do relatório de títulos em aberto exportado do Consinco.
Serve tanto para a exportação em XLSX quanto em TXT: os nomes das
colunas são os mesmos nos dois formatos.
"""

from config.settings import (
    COLUNA_DIAS_ATRASO,
    COLUNA_DT_EMISSAO,
    COLUNA_DT_MOVIMENTO,
    COLUNA_DT_VENCIMENTO,
    COLUNA_EMPRESA,
    COLUNA_ESPECIE,
    COLUNA_PESSOA,
    COLUNA_VLR_ABERTO,
    COLUNA_VLR_TAXA_ADM,
    COLUNAS_VALORES,
)
from src.core.layout import Layout

VALORES_ABERTOS = {
    "original": COLUNAS_VALORES["original"],
    "multa": COLUNAS_VALORES["multa"],
    "juros": COLUNAS_VALORES["juros"],
    "desconto": COLUNAS_VALORES["desconto"],
    "taxa_adm": COLUNA_VLR_TAXA_ADM,
    "aberto": COLUNA_VLR_ABERTO,
    "liquido": COLUNAS_VALORES["liquido"],
}

LAYOUT_ABERTOS = Layout(
    nome="abertos",
    renomear={
        "Empr.": COLUNA_EMPRESA,
        "Vencimento Programado": COLUNA_DT_VENCIMENTO,
        "Multa": COLUNAS_VALORES["multa"],
        "Juros": COLUNAS_VALORES["juros"],
        "Desconto": COLUNAS_VALORES["desconto"],
        "Taxa Adm.": COLUNA_VLR_TAXA_ADM,
        "Valor Aberto": COLUNA_VLR_ABERTO,
        "Valor Líquido": COLUNAS_VALORES["liquido"],
    },
    datas=[COLUNA_DT_EMISSAO, COLUNA_DT_MOVIMENTO, COLUNA_DT_VENCIMENTO],
    valores=VALORES_ABERTOS,
    obrigatorias=[
        COLUNA_PESSOA,
        COLUNA_ESPECIE,
        COLUNA_EMPRESA,
        COLUNA_DT_VENCIMENTO,
        COLUNA_VLR_ABERTO,
        COLUNAS_VALORES["liquido"],
    ],
    data_referencia=COLUNA_DT_VENCIMENTO,
    descartadas=["Column1", "_1"],
    inteiros=[COLUNA_EMPRESA, COLUNA_DIAS_ATRASO],
)
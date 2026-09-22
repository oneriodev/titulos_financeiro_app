"""
Layout do relatório de títulos quitados exportado do Consinco.
"""

from config.settings import (
    COLUNA_DT_QUITACAO,
    COLUNA_DT_VENCIMENTO,
    COLUNA_EMPRESA,
    COLUNA_ESPECIE,
    COLUNA_PESSOA,
    COLUNAS_DATAS,
    COLUNAS_VALORES,
)
from src.core.layout import Layout

LAYOUT_QUITADOS = Layout(
    nome="quitados",
    renomear={
        "Nro Empresa": COLUNA_EMPRESA,
        "Vencimento Programado": COLUNA_DT_VENCIMENTO,
        "Vlr Liquido": COLUNAS_VALORES["liquido"],
    },
    datas=COLUNAS_DATAS,
    valores=COLUNAS_VALORES,
    obrigatorias=[
        COLUNA_PESSOA,
        COLUNA_ESPECIE,
        COLUNA_DT_QUITACAO,
        *COLUNAS_VALORES.values(),
    ],
    data_referencia=COLUNA_DT_QUITACAO,
    descartadas=["Column1"],
)
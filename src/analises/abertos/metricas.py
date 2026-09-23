"""
Agregações da aba Vencimentos dos títulos em aberto.
"""

import pandas as pd

from config.settings import COLUNA_DT_VENCIMENTO, DIAS_SEMANA
from src.analises.abertos.preparo import (
    COLUNA_FAIXA_PRAZO,
    COLUNA_SITUACAO,
    FAIXAS_PRAZO,
)

COLUNA_DATA = "Data"
COLUNA_TOTAL = "Total"
COLUNA_ACUMULADO = "Acumulado"
COLUNA_TITULOS = "Títulos"


def desembolso_diario(df: pd.DataFrame, coluna_valor: str) -> pd.DataFrame:
    """
    Valor a pagar em cada dia de vencimento, com o total acumulado.

    A situação vem de 'first' porque todos os títulos de um mesmo dia
    são necessariamente vencidos ou a vencer — nunca os dois.
    """
    base = df.dropna(subset=[COLUNA_DT_VENCIMENTO])

    agrupado = (
        base.groupby(base[COLUNA_DT_VENCIMENTO].dt.normalize())
        .agg(
            **{
                COLUNA_TOTAL: (coluna_valor, "sum"),
                COLUNA_TITULOS: (coluna_valor, "size"),
                COLUNA_SITUACAO: (COLUNA_SITUACAO, "first"),
            }
        )
        .reset_index()
        .rename(columns={COLUNA_DT_VENCIMENTO: COLUNA_DATA})
        .sort_values(COLUNA_DATA)
        .reset_index(drop=True)
    )

    agrupado[COLUNA_ACUMULADO] = agrupado[COLUNA_TOTAL].cumsum()
    return agrupado


def distribuicao_faixas(df: pd.DataFrame, coluna_valor: str) -> pd.DataFrame:
    """
    Valor por faixa de prazo, na ordem natural das faixas.
    Faixas sem nenhum título são omitidas.
    """
    agrupado = (
        df.groupby(COLUNA_FAIXA_PRAZO, observed=False)[coluna_valor]
        .agg(["sum", "size"])
        .reindex(FAIXAS_PRAZO)
        .reset_index()
        .rename(
            columns={
                COLUNA_FAIXA_PRAZO: "Faixa",
                "sum": COLUNA_TOTAL,
                "size": COLUNA_TITULOS,
            }
        )
    )
    return agrupado[agrupado[COLUNA_TITULOS] > 0].reset_index(drop=True)


def por_dia_semana(df: pd.DataFrame, coluna_valor: str) -> pd.DataFrame:
    """Valor por dia da semana do vencimento, de segunda a domingo."""
    base = df.dropna(subset=[COLUNA_DT_VENCIMENTO]).copy()
    base["Dia"] = base[COLUNA_DT_VENCIMENTO].dt.dayofweek.map(DIAS_SEMANA)

    agrupado = (
        base.groupby("Dia", observed=False)[coluna_valor]
        .agg(["sum", "size"])
        .reindex(list(DIAS_SEMANA.values()))
        .reset_index()
        .rename(columns={"sum": COLUNA_TOTAL, "size": COLUNA_TITULOS})
    )
    return agrupado[agrupado[COLUNA_TITULOS] > 0].reset_index(drop=True)
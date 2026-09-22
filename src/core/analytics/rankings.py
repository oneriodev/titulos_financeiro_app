"""
Rankings por categoria: pessoas, espécies e empresas.
"""

import pandas as pd

from config.settings import COLUNA_EMPRESA, COLUNA_ESPECIE, COLUNA_PESSOA


def ranking_por_categoria(
    df: pd.DataFrame,
    coluna_categoria: str,
    coluna_valor: str,
    top_n: int = 10,
) -> pd.DataFrame:
    """Soma os valores por categoria e devolve as maiores, em ordem decrescente."""
    agrupado = (
        df.groupby(coluna_categoria, as_index=False)[coluna_valor]
        .sum()
        .rename(columns={coluna_valor: "Total"})
    )
    agrupado = agrupado[agrupado["Total"] > 0]
    return agrupado.nlargest(top_n, "Total").reset_index(drop=True)


def top_pessoas(df: pd.DataFrame, coluna_valor: str, top_n: int = 10) -> pd.DataFrame:
    return ranking_por_categoria(df, COLUNA_PESSOA, coluna_valor, top_n)


def top_especies(df: pd.DataFrame, coluna_valor: str, top_n: int = 10) -> pd.DataFrame:
    return ranking_por_categoria(df, COLUNA_ESPECIE, coluna_valor, top_n)


def gastos_por_empresa(df: pd.DataFrame, coluna_valor: str) -> pd.DataFrame:
    """Todas as empresas, da maior para a menor."""
    agrupado = (
        df.groupby(COLUNA_EMPRESA, as_index=False)[coluna_valor]
        .sum()
        .rename(columns={coluna_valor: "Total"})
        .sort_values("Total", ascending=False)
        .reset_index(drop=True)
    )
    agrupado[COLUNA_EMPRESA] = "Empresa " + agrupado[COLUNA_EMPRESA].astype(str)
    return agrupado
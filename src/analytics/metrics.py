"""
Agregações que alimentam os gráficos da aba de métricas.
"""

from typing import Tuple

import pandas as pd

from config.settings import (
    COLUNA_DATA_PADRAO,
    COLUNA_EMPRESA,
    COLUNA_ESPECIE,
    COLUNA_PESSOA,
    DIAS_SEMANA,
)


# ---------------------------------------------------------------------
# Granularidade temporal
# ---------------------------------------------------------------------
def detectar_granularidade(df: pd.DataFrame, coluna_data: str) -> str:
    """
    Decide o agrupamento do eixo temporal.

    Mais de um mês distinto na base -> 'mensal'.
    Um único mês -> 'semanal'.
    """
    datas = df[coluna_data].dropna()
    if datas.empty:
        return "mensal"

    meses_distintos = datas.dt.to_period("M").nunique()
    return "mensal" if meses_distintos > 1 else "semanal"


def _rotulo_semana(periodo: pd.Period) -> str:
    """Converte um período semanal em 'dd/mm a dd/mm'."""
    inicio = periodo.start_time.strftime("%d/%m")
    fim = periodo.end_time.strftime("%d/%m")
    return f"{inicio} a {fim}"


def _rotulo_dia(datas: pd.Series) -> pd.Series:
    """
    Converte datas em 'dd/mm (Sáb)'.

    O código %a do strftime segue o idioma do sistema operacional e
    pode sair em inglês. O dicionário DIAS_SEMANA garante o português.
    """
    dia_semana = datas.dt.dayofweek.map(DIAS_SEMANA).str[:3]
    return datas.dt.strftime("%d/%m") + " (" + dia_semana + ")"


def _serie_periodo(datas: pd.Series, granularidade: str) -> Tuple[pd.Series, pd.Series]:
    """
    Devolve (rótulo exibido, chave de ordenação) para cada data.
    """
    if granularidade == "mensal":
        periodos = datas.dt.to_period("M")
        rotulos = periodos.dt.strftime("%m/%Y")
    else:
        periodos = datas.dt.to_period("W")
        rotulos = periodos.apply(_rotulo_semana)

    return rotulos, periodos.dt.start_time


# ---------------------------------------------------------------------
# Evolução no tempo
# ---------------------------------------------------------------------
def evolucao_temporal(
    df: pd.DataFrame,
    coluna_valor: str,
    coluna_data: str = COLUNA_DATA_PADRAO,
) -> Tuple[pd.DataFrame, str]:
    """
    Soma os valores por período. Retorna (dataframe, granularidade).
    """
    granularidade = detectar_granularidade(df, coluna_data)

    base = df[[coluna_data, coluna_valor]].dropna(subset=[coluna_data]).copy()
    base["Período"], base["_ordem"] = _serie_periodo(base[coluna_data], granularidade)

    agrupado = (
        base.groupby(["Período", "_ordem"], as_index=False)[coluna_valor]
        .sum()
        .sort_values("_ordem")
        .rename(columns={coluna_valor: "Total"})
        .drop(columns="_ordem")
        .reset_index(drop=True)
    )

    return agrupado, granularidade


# ---------------------------------------------------------------------
# Rankings por categoria
# ---------------------------------------------------------------------
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


# ---------------------------------------------------------------------
# Concentração hierárquica
# ---------------------------------------------------------------------
def concentracao_hierarquica(
    df: pd.DataFrame,
    coluna_valor: str,
    coluna_data: str = COLUNA_DATA_PADRAO,
) -> pd.DataFrame:
    """
    Tabela em dois níveis:
      base mensal  -> Mês > Semana
      base semanal -> Semana > Dia

    Traz total, participação percentual e quantidade de títulos.
    """
    granularidade = detectar_granularidade(df, coluna_data)

    base = df[[coluna_data, coluna_valor]].dropna(subset=[coluna_data]).copy()

    if granularidade == "mensal":
        nivel_1, nivel_2 = "Mês", "Semana"
        base[nivel_1] = base[coluna_data].dt.to_period("M").dt.strftime("%m/%Y")
        base[nivel_2] = base[coluna_data].dt.to_period("W").apply(_rotulo_semana)
    else:
        nivel_1, nivel_2 = "Semana", "Dia"
        base[nivel_1] = base[coluna_data].dt.to_period("W").apply(_rotulo_semana)
        base[nivel_2] = _rotulo_dia(base[coluna_data])

    base["_ordem"] = base[coluna_data]

    tabela = (
        base.groupby([nivel_1, nivel_2])
        .agg(Total=(coluna_valor, "sum"),
             Títulos=(coluna_valor, "size"),
             _ordem=("_ordem", "min"))
        .sort_values("_ordem")
        .drop(columns="_ordem")
    )

    total_geral = tabela["Total"].sum()
    tabela["% do Total"] = (
        tabela["Total"] / total_geral * 100 if total_geral else 0
    )

    return tabela
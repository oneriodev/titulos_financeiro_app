"""
Tratamento dos dados: tipos, colunas descartadas e colunas derivadas.
"""

import pandas as pd

from config.settings import (
    COLUNAS_DATAS,
    COLUNAS_DESCARTADAS,
    COLUNAS_VALORES,
    COLUNA_ANO_MES,
    COLUNA_DATA_PADRAO,
    COLUNA_DIA_SEMANA,
    COLUNA_EMPRESA,
    COLUNA_ESPECIE,
    COLUNA_PESSOA,
    DIAS_SEMANA,
)
from src.processing.schema import normalizar_nomes


def _para_numero(serie: pd.Series) -> pd.Series:
    """
    Converte valores para float.

    Já numérico (caso do XLSX): apenas garante o tipo.
    Texto no padrão brasileiro ("1.234,56", vindo de CSV/TXT):
    remove o separador de milhar e troca a vírgula decimal por ponto.
    """
    if pd.api.types.is_numeric_dtype(serie):
        return serie.astype(float)

    texto = (
        serie.astype(str)
        .str.strip()
        .str.replace(r"\.", "", regex=True)
        .str.replace(",", ".", regex=False)
        .replace({"": None, "nan": None, "-": None})
    )
    return pd.to_numeric(texto, errors="coerce").fillna(0.0)


def _para_inteiro(serie: pd.Series) -> pd.Series:
    """
    Converte códigos numéricos (como o número da empresa) para inteiro.

    Em CSV/TXT os códigos chegam como texto ("9"). Sem a conversão,
    "9" nunca é igual a 9 e os filtros não encontram nenhuma linha.
    O tipo Int64 aceita valores vazios, ao contrário do int comum.
    """
    return pd.to_numeric(serie, errors="coerce").astype("Int64")


def limpar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica o tratamento completo e devolve o DataFrame pronto para análise.
    """
    df = normalizar_nomes(df)

    # Remove colunas fantasma da exportação e as 100% vazias
    df = df.drop(columns=[c for c in COLUNAS_DESCARTADAS if c in df.columns])
    df = df.dropna(axis=1, how="all")

    # Remove linhas totalmente vazias
    df = df.dropna(how="all")

    # Datas
    for coluna in COLUNAS_DATAS:
        if coluna in df.columns:
            df[coluna] = pd.to_datetime(
                df[coluna], dayfirst=True, errors="coerce"
            )

    # Valores monetários
    for coluna in COLUNAS_VALORES.values():
        if coluna in df.columns:
            df[coluna] = _para_numero(df[coluna])

    # Códigos numéricos
    if COLUNA_EMPRESA in df.columns:
        df[COLUNA_EMPRESA] = _para_inteiro(df[COLUNA_EMPRESA])

    # Texto
    for coluna in (COLUNA_PESSOA, COLUNA_ESPECIE):
        if coluna in df.columns:
            df[coluna] = df[coluna].astype(str).str.strip()

    # Colunas derivadas para os gráficos
    if COLUNA_DATA_PADRAO in df.columns:
        df[COLUNA_ANO_MES] = df[COLUNA_DATA_PADRAO].dt.to_period("M").astype(str)
        df[COLUNA_DIA_SEMANA] = df[COLUNA_DATA_PADRAO].dt.dayofweek.map(DIAS_SEMANA)

    return df.reset_index(drop=True)
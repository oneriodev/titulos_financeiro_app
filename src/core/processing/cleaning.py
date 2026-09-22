"""
Tratamento dos dados: nomes, tipos, colunas descartadas e colunas derivadas.
As regras específicas de cada relatório vêm do Layout recebido.
"""

import pandas as pd

from config.settings import COLUNA_ANO_MES, COLUNA_DIA_SEMANA, DIAS_SEMANA
from src.core.layout import Layout
from src.core.processing.schema import normalizar_nomes, renomear_colunas


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


def limpar_dados(df: pd.DataFrame, layout: Layout) -> pd.DataFrame:
    """
    Aplica o tratamento completo e devolve o DataFrame pronto para análise.
    """
    df = normalizar_nomes(df)
    df = renomear_colunas(df, layout.renomear)

    # Remove colunas fantasma da exportação e as 100% vazias
    df = df.drop(columns=[c for c in layout.descartadas if c in df.columns])
    df = df.dropna(axis=1, how="all")

    # Remove linhas totalmente vazias
    df = df.dropna(how="all")

    for coluna in layout.datas:
        if coluna in df.columns:
            df[coluna] = pd.to_datetime(df[coluna], dayfirst=True, errors="coerce")

    for coluna in layout.valores.values():
        if coluna in df.columns:
            df[coluna] = _para_numero(df[coluna])

    for coluna in layout.inteiros:
        if coluna in df.columns:
            df[coluna] = _para_inteiro(df[coluna])

    for coluna in layout.textos:
        if coluna in df.columns:
            df[coluna] = df[coluna].astype(str).str.strip()

    # Colunas derivadas da data de referência
    data_ref = layout.data_referencia
    if data_ref in df.columns:
        df[COLUNA_ANO_MES] = df[data_ref].dt.to_period("M").astype(str)
        df[COLUNA_DIA_SEMANA] = df[data_ref].dt.dayofweek.map(DIAS_SEMANA)

    return df.reset_index(drop=True)
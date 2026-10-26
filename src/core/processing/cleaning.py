
"""
Tratamento dos dados importados do ERP Consinco.

O Layout define as regras de cada relatório.

Valores e datas inválidos provocam um erro de validação para
impedir que indicadores financeiros sejam calculados sobre
dados corrompidos ou convertidos silenciosamente.
"""

import pandas as pd

from config.settings import (
    COLUNA_ANO_MES,
    COLUNA_DIA_SEMANA,
    DIAS_SEMANA,
)
from src.core.layout import Layout
from src.core.processing.schema import (
    normalizar_nomes,
    renomear_colunas,
)


# Aceita números brasileiros com ou sem separador de milhar.
# Exemplos: 1234,56 | 1.234,56 | -250,00 | 100
PADRAO_NUMERO_BR = (
    r"[+-]?(?:\d{1,3}(?:\.\d{3})+|\d+)(?:,\d+)?"
)

# Representações de campos não preenchidos.
VALORES_VAZIOS = {"", "-", "nan", "none", "nat"}


def _mascara_vazios(serie: pd.Series) -> pd.Series:
    """
    Identifica valores ausentes.

    Centralizar essa regra impede que diferentes partes do
    tratamento interpretem campos vazios de formas distintas.
    """
    texto = serie.astype(str).str.strip().str.lower()

    return serie.isna() | texto.isin(VALORES_VAZIOS)


def _validar_obrigatorias(
    df: pd.DataFrame, layout: Layout
) -> None:
    """
    Verifica a existência e o preenchimento das colunas obrigatórias.

    A validação acontece antes da conversão para evitar que
    valores vazios sejam transformados em zero.
    """
    faltantes = [
        coluna
        for coluna in layout.obrigatorias
        if coluna not in df.columns
    ]

    if faltantes:
        raise ValueError(
            "Colunas obrigatórias ausentes: "
            + ", ".join(faltantes)
        )

    if df.empty:
        raise ValueError(
            "O relatório não possui registros para análise."
        )

    for coluna in layout.obrigatorias:
        vazios = _mascara_vazios(df[coluna])
        quantidade = int(vazios.sum())

        if quantidade:
            raise ValueError(
                f"A coluna obrigatória '{coluna}' possui "
                f"{quantidade} registro(s) vazio(s)."
            )


def _para_numero(serie: pd.Series) -> pd.Series:
    """
    Converte valores monetários para float.

    Valores numéricos de XLSX preservam seu significado.
    Textos seguem a notação brasileira.

    Uma representação monetária inválida interrompe o
    processamento, evitando transformá-la em R$ 0,00.

    Campos realmente vazios continuam equivalendo a zero
    nas colunas opcionais, preservando a regra anterior.
    """
    if pd.api.types.is_numeric_dtype(serie):
        return serie.astype(float)

    texto = serie.astype(str).str.strip()
    vazios = _mascara_vazios(serie)

    # Confere o formato antes de remover os separadores.
    formato_valido = texto.str.fullmatch(
        PADRAO_NUMERO_BR
    ).fillna(False)

    invalidos = ~vazios & ~formato_valido
    quantidade = int(invalidos.sum())

    if quantidade:
        raise ValueError(
            f"Foram encontrados {quantidade} valor(es) "
            "monetário(s) em formato inválido."
        )

    texto = (
        texto
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .mask(vazios)
    )

    return pd.to_numeric(
        texto, errors="raise"
    ).fillna(0.0)


def _para_inteiro(serie: pd.Series) -> pd.Series:
    """
    Converte códigos numéricos de identificação para inteiros.

    Utiliza Int64 para permitir valores ausentes em colunas
    que não sejam obrigatórias.
    """
    return pd.to_numeric(
        serie, errors="coerce"
    ).astype("Int64")


def _para_data(
    serie: pd.Series, nome_coluna: str
) -> pd.Series:
    """
    Converte datas e identifica conteúdos inválidos.

    Campos opcionais vazios são permitidos.
    Textos preenchidos que não representem uma data válida
    provocam erro antes dos cálculos temporais.
    """
    vazios = _mascara_vazios(serie)

    resultado = pd.to_datetime(
        serie,
        dayfirst=True,
        errors="coerce",
    )

    invalidos = ~vazios & resultado.isna()
    quantidade = int(invalidos.sum())

    if quantidade:
        raise ValueError(
            f"A coluna de data '{nome_coluna}' contém "
            f"{quantidade} registro(s) inválido(s)."
        )

    return resultado


def limpar_dados(
    df: pd.DataFrame, layout: Layout
) -> pd.DataFrame:
    """
    Executa o tratamento conforme as regras do relatório.

    A ordem foi escolhida para validar os dados antes de
    convertê-los, preservando a confiabilidade financeira.
    """
    df = normalizar_nomes(df)
    df = renomear_colunas(df, layout.renomear)

    # Remove colunas auxiliares indesejadas.
    df = df.drop(
        columns=[
            coluna
            for coluna in layout.descartadas
            if coluna in df.columns
        ]
    )

    # Remove linhas completamente vazias.
    df = df.dropna(how="all")

    # Valida o conteúdo antes das conversões.
    _validar_obrigatorias(df, layout)

    # Remove colunas opcionais inteiramente vazias.
    df = df.dropna(axis=1, how="all")

    # Conversão e validação das datas.
    for coluna in layout.datas:
        if coluna in df.columns:
            df[coluna] = _para_data(
                df[coluna], coluna
            )

    # Conversão e validação monetária.
    for coluna in layout.valores.values():
        if coluna in df.columns:
            try:
                df[coluna] = _para_numero(
                    df[coluna]
                )
            except ValueError as erro:
                raise ValueError(
                    f"Erro na coluna '{coluna}': {erro}"
                ) from erro

    # Conversão dos códigos numéricos.
    for coluna in layout.inteiros:
        if coluna in df.columns:
            df[coluna] = _para_inteiro(
                df[coluna]
            )

    # Normalização dos textos.
    for coluna in layout.textos:
        if coluna in df.columns:
            df[coluna] = (
                df[coluna]
                .astype(str)
                .str.strip()
            )

    # Colunas derivadas da data de referência.
    data_ref = layout.data_referencia

    if data_ref in df.columns:
        df[COLUNA_ANO_MES] = (
            df[data_ref]
            .dt.to_period("M")
            .astype(str)
        )

        df[COLUNA_DIA_SEMANA] = (
            df[data_ref]
            .dt.dayofweek
            .map(DIAS_SEMANA)
        )

    return df.reset_index(drop=True)

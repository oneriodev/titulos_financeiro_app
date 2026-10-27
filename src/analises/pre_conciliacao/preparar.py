
"""
Preparação dos dados para a pré-conciliação financeira.

Recebe os DataFrames já tratados pelo núcleo compartilhado.
Não altera os dados originais nem executa correspondências.

Os valores monetários são representados em centavos inteiros
para evitar diferenças de precisão durante a comparação.
"""

from decimal import Decimal, InvalidOperation

import pandas as pd

from config.settings import (
    COLUNA_EMPRESA,
    COLUNA_DT_QUITACAO,
    COLUNAS_VALORES,
)


def _converter_centavos(valor) -> int:
    """
    Converte um valor numérico em centavos inteiros.

    Rejeita valores com mais de duas casas decimais para
    impedir arredondamentos financeiros silenciosos.
    """
    try:
        numero = Decimal(str(valor))
    except (InvalidOperation, ValueError, TypeError) as erro:
        raise ValueError(
            "Valor monetário inválido na preparação."
        ) from erro

    if not numero.is_finite():
        raise ValueError("Valor monetário não finito.")

    centavos = numero * 100

    if centavos != centavos.to_integral_value():
        raise ValueError(
            "Valor monetário com mais de duas casas decimais."
        )

    return int(centavos)


def _validar_campos(df: pd.DataFrame, campos: list[str]) -> None:
    """Impede a preparação de relatórios sem campos essenciais."""
    faltantes = [
        campo for campo in campos
        if campo not in df.columns
    ]

    if faltantes:
        raise ValueError(
            "Colunas necessárias ausentes: "
            + ", ".join(faltantes)
        )

    if df.empty:
        raise ValueError("O relatório não contém registros.")

    if not df.columns.is_unique:
        raise ValueError(
            "O relatório possui nomes de colunas duplicados."
        )


def _validar_empresa(df: pd.DataFrame) -> None:
    """Exige um código de empresa válido em cada registro."""
    empresa = df[COLUNA_EMPRESA]

    if empresa.isna().any():
        raise ValueError(
            "Existem registros sem identificação da empresa."
        )

    if not pd.api.types.is_integer_dtype(empresa):
        raise ValueError(
            "A coluna Empresa deve estar normalizada "
            "como código inteiro."
        )


def _validar_data(df: pd.DataFrame, coluna: str) -> None:
    """Exige datas válidas já convertidas pelo núcleo."""
    if not pd.api.types.is_datetime64_any_dtype(df[coluna]):
        raise ValueError(
            f"A coluna '{coluna}' ainda não foi convertida em data."
        )

    if df[coluna].isna().any():
        raise ValueError(
            f"A coluna '{coluna}' possui datas ausentes."
        )


def preparar_conta_corrente(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepara os lançamentos da Conta Corrente Consinco.

    Mantém créditos e débitos, marcando apenas os débitos
    positivos em módulo como elegíveis para comparação.
    """
    _validar_campos(
        df,
        [
            COLUNA_EMPRESA,
            "Data Lançamento",
            "Valor",
            "Tipo de Lançamento",
        ],
    )

    resultado = df.copy().reset_index(drop=True)

    _validar_empresa(resultado)
    _validar_data(resultado, "Data Lançamento")

    # Normaliza os indicadores de débito e crédito.
    resultado["Tipo de Lançamento"] = (
        resultado["Tipo de Lançamento"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    tipos_validos = resultado[
        "Tipo de Lançamento"
    ].isin(["D", "C"])

    if not tipos_validos.all():
        raise ValueError(
            "A Conta Corrente possui tipos diferentes de C ou D."
        )

    # Cada registro mantém sua posição após a limpeza.
    resultado["id_registro"] = [
        f"CC{i:06d}"
        for i in range(1, len(resultado) + 1)
    ]

    resultado["data_comparacao"] = resultado[
        "Data Lançamento"
    ]

    resultado["valor_centavos"] = (
        resultado["Valor"]
        .map(_converter_centavos)
    )

    if (resultado["valor_centavos"] < 0).any():
        raise ValueError(
            "A Conta Corrente possui valores negativos "
            "na coluna Valor; verifique o layout."
        )

    # Preserva Valor e cria uma representação com sinal.
    resultado["valor_assinado_centavos"] = (
        resultado["valor_centavos"].where(
            resultado["Tipo de Lançamento"].eq("C"),
            -resultado["valor_centavos"],
        )
    )

    resultado["elegivel_conciliacao"] = (
        resultado["Tipo de Lançamento"].eq("D")
        & resultado["valor_centavos"].gt(0)
    )

    return resultado


def preparar_quitados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepara os títulos quitados para comparação.

    Utiliza o Vlr Líquido existente no DataFrame tratado.
    Não recalcula juros, descontos ou compensações.
    """
    coluna_liquido = COLUNAS_VALORES["liquido"]

    _validar_campos(
        df,
        [
            COLUNA_EMPRESA,
            COLUNA_DT_QUITACAO,
            coluna_liquido,
        ],
    )

    resultado = df.copy().reset_index(drop=True)

    _validar_empresa(resultado)
    _validar_data(resultado, COLUNA_DT_QUITACAO)

    resultado["id_registro"] = [
        f"Q{i:06d}"
        for i in range(1, len(resultado) + 1)
    ]

    resultado["data_comparacao"] = resultado[
        COLUNA_DT_QUITACAO
    ]

    resultado["valor_centavos"] = (
        resultado[coluna_liquido]
        .map(_converter_centavos)
    )

    # Valores negativos ou zerados são preservados,
    # mas não entram no cruzamento inicial de pagamentos.
    resultado["elegivel_conciliacao"] = (
        resultado["valor_centavos"].gt(0)
    )

    return resultado


def preparar_pre_conciliacao(
    df_conta_corrente: pd.DataFrame,
    df_quitados: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Retorna os dois relatórios preparados.

    Nenhuma linha é vinculada ou removida nesta etapa.
    """
    conta = preparar_conta_corrente(df_conta_corrente)
    quitados = preparar_quitados(df_quitados)

    return conta, quitados

"""
Cálculo dos totais gerais exibidos nos cartões.
"""

from typing import Dict

import pandas as pd

from config.settings import COLUNAS_VALORES


def calcular_totais(df: pd.DataFrame) -> Dict[str, float]:
    """
    Soma cada coluna de valor do arquivo.

    Retorna um dicionário no formato {chave_interna: total}.
    Os valores vêm somados direto do relatório, sem recálculo:
    a fórmula do Consinco já é Líquido = Pago + Juros - Desconto - Compensação.
    """
    totais: Dict[str, float] = {}

    for chave, coluna in COLUNAS_VALORES.items():
        if coluna in df.columns:
            totais[chave] = float(df[coluna].sum())
        else:
            totais[chave] = 0.0

    return totais


def contar_registros(df: pd.DataFrame) -> int:
    """Quantidade de títulos no conjunto de dados."""
    return len(df)
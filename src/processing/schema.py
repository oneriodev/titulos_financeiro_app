"""
Validação da estrutura do DataFrame lido.
"""

from typing import List, Tuple

import pandas as pd

from config.settings import COLUNAS_OBRIGATORIAS


def normalizar_nomes(df: pd.DataFrame) -> pd.DataFrame:
    """Remove espaços extras dos nomes das colunas."""
    df = df.copy()
    df.columns = [str(coluna).strip() for coluna in df.columns]
    return df


def validar_colunas(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Verifica se todas as colunas obrigatórias estão presentes.

    Retorna (valido, lista_de_colunas_faltantes).
    """
    faltantes = [c for c in COLUNAS_OBRIGATORIAS if c not in df.columns]
    return (len(faltantes) == 0, faltantes)
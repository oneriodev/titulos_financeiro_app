"""
Estrutura do DataFrame: limpeza de nomes, renomeação e validação.
"""

from typing import Dict, List, Tuple

import pandas as pd

def normalizar_nomes(df: pd.DataFrame) -> pd.DataFrame:
    """Remove espaços extras dos nomes das colunas."""
    df = df.copy()
    df.columns = [str(coluna).strip() for coluna in df.columns]
    return df


def renomear_colunas(df: pd.DataFrame, mapa: Dict[str, str]) -> pd.DataFrame:
    """
    Converte os nomes do relatório original para o vocabulário padronizado.

    Colunas ausentes no mapa mantêm o nome original. Entradas do mapa que
    não existem no arquivo são ignoradas.
    """
    return df.rename(columns=mapa)


def validar_colunas(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Verifica se todas as colunas obrigatórias estão presentes.

    Retorna (valido, lista_de_colunas_faltantes).
    """
    faltantes = [c for c in COLUNAS_OBRIGATORIAS if c not in df.columns]
    return (len(faltantes) == 0, faltantes)
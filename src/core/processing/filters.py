"""
Aplicação dos filtros sobre o DataFrame tratado.
Módulo sem dependência do Streamlit, para facilitar testes.
"""

from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional

import pandas as pd

from config.settings import COLUNA_EMPRESA, COLUNA_ESPECIE

@dataclass
class Filtros:
    """Seleções feitas pelo usuário. Campos vazios significam 'sem filtro'."""

    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None
    empresas: List[int] = field(default_factory=list)
    especies: List[str] = field(default_factory=list)

    @property
    def quantidade_ativos(self) -> int:
        """Quantos filtros estão restringindo a base."""
        periodo = self.data_inicio is not None or self.data_fim is not None
        return sum([periodo, bool(self.empresas), bool(self.especies)])


def aplicar_filtros(
    df: pd.DataFrame, filtros: Filtros, coluna_data: str
) -> pd.DataFrame:
    """
    Devolve apenas as linhas que atendem a todos os filtros ativos.
    coluna_data define a data do filtro de período.
    """
    mascara = pd.Series(True, index=df.index)

    datas = df[coluna_data].dt.date

    if filtros.data_inicio is not None:
        mascara &= datas >= filtros.data_inicio

    if filtros.data_fim is not None:
        mascara &= datas <= filtros.data_fim

    if filtros.empresas:
        mascara &= df[COLUNA_EMPRESA].isin(filtros.empresas)

    if filtros.especies:
        mascara &= df[COLUNA_ESPECIE].isin(filtros.especies)

    return df[mascara].reset_index(drop=True)
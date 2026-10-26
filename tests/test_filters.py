
"""
Testes dos filtros compartilhados pelas análises.

Os filtros devem preservar a integridade dos registros e valores
financeiros selecionados.
"""

from datetime import date

import pandas as pd
import pytest

from config.settings import (
    COLUNA_EMPRESA,
    COLUNA_ESPECIE,
    COLUNAS_VALORES,
)

from src.core.processing.filters import Filtros, aplicar_filtros


def criar_base_sintetica():
    """Cria uma pequena base reproduzível para testar filtros."""
    return pd.DataFrame(
        {
            "Dt. Quitação": pd.to_datetime(
                ["2026-10-01", "2026-10-10", "2026-10-20"]
            ),
            COLUNA_EMPRESA: [1, 2, 1],
            COLUNA_ESPECIE: ["BOL", "PIX", "BOL"],
            COLUNAS_VALORES["liquido"]: [
                100.00, 200.00, 300.00
            ],
        }
    )


def test_filtro_empresa():
    """Seleciona somente títulos da empresa informada."""
    dados = criar_base_sintetica()

    resultado = aplicar_filtros(
        dados,
        Filtros(empresas=[1]),
        "Dt. Quitação",
    )

    assert len(resultado) == 2
    assert resultado[COLUNAS_VALORES["liquido"]].sum() == pytest.approx(
        400.00
    )


def test_filtro_periodo():
    """Confere limites inicial e final inclusivos."""
    dados = criar_base_sintetica()

    resultado = aplicar_filtros(
        dados,
        Filtros(
            data_inicio=date(2026, 10, 1),
            data_fim=date(2026, 10, 10),
        ),
        "Dt. Quitação",
    )

    assert len(resultado) == 2
    assert resultado[COLUNAS_VALORES["liquido"]].sum() == pytest.approx(
        300.00
    )


def test_filtros_combinados():
    """Aplica empresa e espécie simultaneamente."""
    dados = criar_base_sintetica()

    resultado = aplicar_filtros(
        dados,
        Filtros(empresas=[1], especies=["BOL"]),
        "Dt. Quitação",
    )

    assert len(resultado) == 2
    assert resultado[COLUNAS_VALORES["liquido"]].sum() == pytest.approx(
        400.00
    )


def test_filtros_sem_restricoes():
    """Nenhum filtro ativo deve preservar a base completa."""
    dados = criar_base_sintetica()

    resultado = aplicar_filtros(
        dados, Filtros(), "Dt. Quitação"
    )

    assert len(resultado) == len(dados)
    assert resultado[COLUNAS_VALORES["liquido"]].sum() == pytest.approx(
        600.00
    )

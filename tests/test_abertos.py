
"""
Testes das regras de vencimento dos títulos em aberto.

A data de corte é fixa nos testes para garantir resultados
reproduzíveis, independentemente do dia de execução.
"""

import pandas as pd

from config.settings import (
    COLUNA_DIAS_ATRASO,
    COLUNA_DT_VENCIMENTO,
)

from src.analises.abertos.preparo import (
    COLUNA_DIAS_PARA_VENCER,
    COLUNA_FAIXA_PRAZO,
    COLUNA_SITUACAO,
    SITUACAO_A_VENCER,
    SITUACAO_VENCIDO,
    obter_data_corte,
    preparar_abertos,
)


def test_obter_data_corte():
    """Confere a inferência da data do relatório pelo atraso."""
    dados = pd.DataFrame(
        {
            COLUNA_DT_VENCIMENTO: pd.to_datetime(
                ["2026-10-20", "2026-10-25", "2026-11-02"]
            ),
            COLUNA_DIAS_ATRASO: [6, 1, 0],
        }
    )

    resultado = obter_data_corte(dados)

    assert resultado == pd.Timestamp("2026-10-26")


def test_classificacao_vencimentos():
    """Distingue títulos vencidos e títulos ainda a vencer."""
    dados = pd.DataFrame(
        {
            COLUNA_DT_VENCIMENTO: pd.to_datetime(
                ["2026-10-24", "2026-10-26", "2026-10-29"]
            )
        }
    )

    resultado = preparar_abertos(
        dados, pd.Timestamp("2026-10-26")
    )

    assert resultado[COLUNA_SITUACAO].tolist() == [
        SITUACAO_VENCIDO,
        SITUACAO_A_VENCER,
        SITUACAO_A_VENCER,
    ]

    assert resultado[COLUNA_DIAS_PARA_VENCER].tolist() == [
        -2, 0, 3
    ]


def test_faixas_de_prazo():
    """Confere os limites das seis faixas de vencimento."""
    corte = pd.Timestamp("2026-10-26")

    dados = pd.DataFrame(
        {
            COLUNA_DT_VENCIMENTO: [
                corte + pd.Timedelta(days=dias)
                for dias in [-1, 0, 7, 15, 30, 31]
            ]
        }
    )

    resultado = preparar_abertos(dados, corte)

    assert resultado[COLUNA_FAIXA_PRAZO].astype(str).tolist() == [
        "Vencido",
        "Vence hoje",
        "1 a 7 dias",
        "8 a 15 dias",
        "16 a 30 dias",
        "Acima de 30 dias",
    ]

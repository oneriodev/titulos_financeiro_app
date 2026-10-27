
"""
Testes do layout de Conta Corrente Consinco.

Utiliza somente dados sintéticos, sem arquivos reais.
"""

import pandas as pd
import pytest

from src.analises.pre_conciliacao.layout_conta_corrente import (
    LAYOUT_CONTA_CORRENTE,
)
from src.core.processing.cleaning import limpar_dados


def criar_extrato_sintetico():
    """Cria registros de débito e crédito para validar o layout."""
    return pd.DataFrame({
        "loja": ["1", "1", "2"],
        "Conta Corrente": ["001", "001", "002"],
        "Documento": ["", "", ""],
        "Serie": ["A", "A", "B"],
        "Data Lançamento": [
            "20/10/2026",
            "21/10/2026",
            "22/10/2026",
        ],
        "Operações": ["54", "911", "134"],
        "Data Conciliação": ["", "", ""],
        "Data Compensação": ["", "", ""],
        "Historico": [
            "PAGAMENTO FORNECEDOR",
            "CREDITO RECEBIDO",
            "PAGAMENTO PIX",
        ],
        "Concilado": ["N", "N", "N"],
        "Valor": ["1.500,00", "2.000,00", "750,50"],
        "Tipo de Lançamento": ["D", "C", "D"],
        "Saldo": ["-1.500,00", "500,00", "-750,50"],
        "Column1": [None, None, None],
    })


def test_padronizacao_conta_corrente():
    """Verifica nomes das colunas e tipos convertidos."""
    bruto = criar_extrato_sintetico()

    resultado = limpar_dados(
        bruto, LAYOUT_CONTA_CORRENTE
    )

    assert "Empresa" in resultado.columns
    assert "Operação" in resultado.columns
    assert "Histórico" in resultado.columns
    assert "Column1" not in resultado.columns

    assert len(resultado) == 3
    assert resultado["Empresa"].tolist() == [1, 1, 2]

    assert pd.api.types.is_datetime64_any_dtype(
        resultado["Data Lançamento"]
    )


def test_preservacao_dos_valores():
    """Garante que o layout não altere os sinais originais."""
    resultado = limpar_dados(
        criar_extrato_sintetico(),
        LAYOUT_CONTA_CORRENTE,
    )

    assert resultado["Valor"].tolist() == [
        1500.00,
        2000.00,
        750.50,
    ]

    assert resultado["Tipo de Lançamento"].tolist() == [
        "D", "C", "D"
    ]

    assert resultado["Saldo"].tolist() == [
        -1500.00,
        500.00,
        -750.50,
    ]


def test_rejeicao_valor_invalido():
    """Um valor inválido não pode virar zero silenciosamente."""
    bruto = criar_extrato_sintetico()

    bruto.loc[0, "Valor"] = "VALOR INVALIDO"

    with pytest.raises(ValueError):
        limpar_dados(bruto, LAYOUT_CONTA_CORRENTE)


def test_rejeicao_coluna_obrigatoria_ausente():
    """Uma coluna essencial ausente interrompe a preparação."""
    bruto = criar_extrato_sintetico()
    bruto = bruto.drop(columns=["Tipo de Lançamento"])

    with pytest.raises(ValueError):
        limpar_dados(bruto, LAYOUT_CONTA_CORRENTE)


"""
Testes da preparação da pré-conciliação.

Todos os registros são sintéticos e criados em memória.
"""

import pandas as pd
import pytest

from config.settings import COLUNAS_VALORES
from src.analises.pre_conciliacao.preparar import (
    preparar_pre_conciliacao,
    preparar_conta_corrente,
    preparar_quitados,
)


def criar_conta_corrente():
    """Simula dados já tratados pelo Layout Conta Corrente."""
    return pd.DataFrame({
        "Empresa": pd.Series([1, 1, 2], dtype="Int64"),
        "Data Lançamento": pd.to_datetime([
            "2026-10-20",
            "2026-10-21",
            "2026-10-22",
        ]),
        "Valor": [1500.00, 2000.00, 750.50],
        "Tipo de Lançamento": ["D", "C", "D"],
        "Operação": ["54", "911", "134"],
    })


def criar_quitados():
    """Simula dados tratados pelo Layout de Quitados."""
    return pd.DataFrame({
        "Empresa": pd.Series([1, 2], dtype="Int64"),
        "Dt. Quitação": pd.to_datetime([
            "2026-10-20",
            "2026-10-22",
        ]),
        COLUNAS_VALORES["liquido"]: [
            1500.00,
            750.50,
        ],
    })


def test_preserva_quantidade_de_registros():
    """A preparação não pode excluir lançamentos."""
    conta, quitados = preparar_pre_conciliacao(
        criar_conta_corrente(),
        criar_quitados(),
    )

    assert len(conta) == 3
    assert len(quitados) == 2


def test_conversao_centavos():
    """Verifica a conversão monetária sem alterar valores."""
    conta, quitados = preparar_pre_conciliacao(
        criar_conta_corrente(),
        criar_quitados(),
    )

    assert conta["valor_centavos"].tolist() == [
        150000, 200000, 75050
    ]

    assert quitados["valor_centavos"].tolist() == [
        150000, 75050
    ]

    assert conta["Valor"].sum() == 4250.50
    assert quitados["Vlr Líquido"].sum() == 2250.50


def test_debitos_creditos():
    """Somente os débitos participam da comparação inicial."""
    conta = preparar_conta_corrente(
        criar_conta_corrente()
    )

    assert conta["elegivel_conciliacao"].tolist() == [
        True, False, True
    ]

    assert conta[
        "valor_assinado_centavos"
    ].tolist() == [-150000, 200000, -75050]


def test_identificadores():
    """Verifica IDs distintos e sequenciais para cada origem."""
    conta, quitados = preparar_pre_conciliacao(
        criar_conta_corrente(),
        criar_quitados(),
    )

    assert conta["id_registro"].tolist() == [
        "CC000001", "CC000002", "CC000003"
    ]

    assert quitados["id_registro"].tolist() == [
        "Q000001", "Q000002"
    ]


def test_valor_invalido():
    """Valores com precisão monetária indevida são rejeitados."""
    df = criar_quitados()
    df.loc[0, "Vlr Líquido"] = 1500.123

    with pytest.raises(ValueError):
        preparar_quitados(df)


def test_tipo_invalido():
    """Não aceitar tipos de lançamentos desconhecidos."""
    df = criar_conta_corrente()
    df.loc[0, "Tipo de Lançamento"] = "X"

    with pytest.raises(ValueError):
        preparar_conta_corrente(df)


def test_data_ausente():
    """Data essencial ausente não deve gerar associação indevida."""
    df = criar_quitados()
    df.loc[0, "Dt. Quitação"] = pd.NaT

    with pytest.raises(ValueError):
        preparar_quitados(df)


def test_creditos_e_zeros_preservados():
    """Créditos e valores zero permanecem disponíveis."""
    conta = criar_conta_corrente()
    conta.loc[1, "Valor"] = 0

    resultado = preparar_conta_corrente(conta)

    assert len(resultado) == 3
    assert resultado.loc[1, "valor_centavos"] == 0
    assert not resultado.loc[1, "elegivel_conciliacao"]

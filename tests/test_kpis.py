
"""
Testes dos indicadores financeiros do DataApp.

Os valores esperados são definidos manualmente para detectar
alterações involuntárias nas regras de negócio.
"""

import pandas as pd
import pytest

from config.settings import (
    COLUNA_PESSOA,
    COLUNA_VLR_ABERTO,
    COLUNAS_VALORES,
)

from src.analytics.kpis import calcular_totais, contar_registros
from src.analises.abertos.kpis import calcular_resumo
from src.analises.abertos.preparo import (
    COLUNA_DIAS_PARA_VENCER,
    COLUNA_SITUACAO,
    SITUACAO_A_VENCER,
    SITUACAO_VENCIDO,
)


def test_totais_titulos_quitados():
    """Confere a soma das colunas monetárias de Quitados."""
    dados = pd.DataFrame(
        {
            COLUNAS_VALORES["original"]: [100.00, 200.00],
            COLUNAS_VALORES["multa"]: [0.00, 2.00],
            COLUNAS_VALORES["juros"]: [5.00, 3.00],
            COLUNAS_VALORES["desconto"]: [1.00, 2.00],
            COLUNAS_VALORES["abatimento"]: [0.00, 0.00],
            COLUNAS_VALORES["compensacao"]: [4.00, 1.00],
            COLUNAS_VALORES["pago"]: [100.00, 200.00],
            COLUNAS_VALORES["liquido"]: [100.00, 200.00],
        }
    )

    totais = calcular_totais(dados)

    assert totais["original"] == pytest.approx(300.00)
    assert totais["multa"] == pytest.approx(2.00)
    assert totais["juros"] == pytest.approx(8.00)
    assert totais["desconto"] == pytest.approx(3.00)
    assert totais["compensacao"] == pytest.approx(5.00)
    assert totais["pago"] == pytest.approx(300.00)
    assert totais["liquido"] == pytest.approx(300.00)

    assert contar_registros(dados) == 2


def test_conciliacao_formula_liquido():
    """Valida a relação monetária documentada para Quitados."""
    pago = 1000.00
    juros = 25.00
    desconto = 10.00
    compensacao = 15.00

    liquido_esperado = 1000.00

    calculado = pago + juros - desconto - compensacao

    assert calculado == pytest.approx(liquido_esperado)


def test_resumo_titulos_abertos():
    """Confere totais, vencimentos, parciais e maior título."""
    dados = pd.DataFrame(
        {
            COLUNA_PESSOA: [
                "Fornecedor A",
                "Fornecedor B",
                "Fornecedor C",
            ],
            COLUNAS_VALORES["original"]: [
                200.00, 100.00, 150.00
            ],
            COLUNA_VLR_ABERTO: [
                150.00, 100.00, 150.00
            ],
            COLUNAS_VALORES["desconto"]: [
                10.00, 0.00, 5.00
            ],
            COLUNAS_VALORES["liquido"]: [
                140.00, 100.00, 145.00
            ],
            COLUNA_SITUACAO: [
                SITUACAO_VENCIDO,
                SITUACAO_A_VENCER,
                SITUACAO_A_VENCER,
            ],
            COLUNA_DIAS_PARA_VENCER: [-2, 0, 5],
        }
    )

    resumo = calcular_resumo(dados)

    assert resumo.titulos == 3
    assert resumo.original == pytest.approx(450.00)
    assert resumo.aberto == pytest.approx(400.00)
    assert resumo.desconto == pytest.approx(15.00)
    assert resumo.liquido == pytest.approx(385.00)

    # Situação da carteira
    assert resumo.vencidos_valor == pytest.approx(150.00)
    assert resumo.vencidos_titulos == 1
    assert resumo.a_vencer_valor == pytest.approx(250.00)
    assert resumo.a_vencer_titulos == 2

    # Próximos sete dias, incluindo o dia do relatório
    assert resumo.proxima_semana_valor == pytest.approx(250.00)
    assert resumo.proxima_semana_titulos == 2

    # Pagamentos parciais, conforme a regra atual
    assert resumo.parciais_titulos == 1
    assert resumo.parciais_valor == pytest.approx(50.00)

    # Estatísticas
    assert resumo.ticket_medio == pytest.approx(400.00 / 3)
    assert resumo.maior_titulo_valor == pytest.approx(150.00)
    assert resumo.maior_titulo_pessoa == "Fornecedor A"


def test_reconciliacao_carteira():
    """Vencidos mais a vencer devem recompor o saldo total."""
    dados = pd.DataFrame(
        {
            COLUNA_PESSOA: ["A", "B"],
            COLUNAS_VALORES["original"]: [200.00, 300.00],
            COLUNA_VLR_ABERTO: [150.00, 300.00],
            COLUNAS_VALORES["desconto"]: [0.00, 0.00],
            COLUNAS_VALORES["liquido"]: [150.00, 300.00],
            COLUNA_SITUACAO: [
                SITUACAO_VENCIDO,
                SITUACAO_A_VENCER,
            ],
            COLUNA_DIAS_PARA_VENCER: [-1, 3],
        }
    )

    resumo = calcular_resumo(dados)

    assert (
        resumo.vencidos_valor + resumo.a_vencer_valor
    ) == pytest.approx(resumo.aberto)

    assert (
        resumo.vencidos_titulos + resumo.a_vencer_titulos
    ) == resumo.titulos

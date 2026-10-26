
"""
Testes do tratamento de dados importados do ERP Consinco.

Os exemplos são sintéticos e não contêm dados da empresa.
O objetivo é impedir regressões nas conversões de valores e datas.
"""

import io

import pandas as pd
import pytest

from src.analises.quitados.layout import LAYOUT_QUITADOS
from src.core.extraction.file_reader import ler_arquivo
from src.core.processing.cleaning import (
    _para_inteiro,
    _para_numero,
    limpar_dados,
)


@pytest.mark.parametrize(
    "entrada, esperado",
    [
        ("1.234,56", 1234.56),
        ("10.000,00", 10000.00),
        ("250,75", 250.75),
        ("0,00", 0.00),
        ("-150,50", -150.50),
        (" 1.500,25 ", 1500.25),
    ],
)
def test_conversao_valores_brasileiros(entrada, esperado):
    """Garante que a notação brasileira seja convertida corretamente."""
    serie = pd.Series([entrada])

    resultado = _para_numero(serie)

    assert resultado.iloc[0] == pytest.approx(esperado)


def test_valores_numericos_ja_convertidos():
    """Valores provenientes de XLSX não devem ser multiplicados ou divididos."""
    serie = pd.Series([1234.56, 200.00, -50.25])

    resultado = _para_numero(serie)

    assert resultado.tolist() == pytest.approx(
        [1234.56, 200.00, -50.25]
    )


def test_conversao_codigos_empresa():
    """Códigos das empresas precisam ser inteiros para funcionar nos filtros."""
    serie = pd.Series(["1", "9", None])

    resultado = _para_inteiro(serie)

    assert resultado.iloc[0] == 1
    assert resultado.iloc[1] == 9
    assert pd.isna(resultado.iloc[2])



def test_limpeza_relatorio_quitados():
    """Confere o tratamento de um relatório válido de Quitados."""
    dados = pd.DataFrame(
        {
            "Pessoa": ["Fornecedor Teste"],
            "Espécie": ["BOL"],
            "Nro Empresa": ["9"],
            "Dt. Quitação": ["15/10/2026"],
            "Vlr Original": ["1.234,56"],
            "Vlr Multa": ["0,00"],
            "Vlr Juros": ["10,00"],
            "Vlr Desconto": ["5,00"],
            "Vlr Abatimento": ["0,00"],
            "Vlr Compensação": ["5,00"],
            "Vlr Pago": ["1.200,00"],
            "Vlr Liquido": ["1.200,00"],
        }
    )

    resultado = limpar_dados(dados, LAYOUT_QUITADOS)

    assert resultado.loc[0, "Empresa"] == 9
    assert resultado.loc[0, "Vlr Original"] == pytest.approx(1234.56)
    assert resultado.loc[0, "Vlr Pago"] == pytest.approx(1200.00)
    assert resultado.loc[0, "Vlr Líquido"] == pytest.approx(1200.00)
    assert resultado.loc[0, "Dt. Quitação"] == pd.Timestamp(
        "2026-10-15"
    )

    assert resultado.loc[0, "Empresa"] == 9
    assert resultado.loc[0, "Vlr Original"] == pytest.approx(1234.56)
    assert resultado.loc[0, "Vlr Pago"] == pytest.approx(1200.00)
    assert resultado.loc[0, "Vlr Líquido"] == pytest.approx(1200.00)

    assert resultado.loc[0, "Dt. Quitação"] == pd.Timestamp(
        "2026-10-15"
    )


def test_leitura_csv_com_ponto_virgula_extra():
    """Verifica se os campos de CSV permanecem alinhados."""
    conteudo = (
        "Pessoa;Espécie;Nro Empresa;Vlr Pago\n"
        "Fornecedor A;BOL;9;1.250,50;\n"
        "Fornecedor B;BOL;2;300,00;\n"
    )

    arquivo = io.BytesIO(conteudo.encode("utf-8"))
    arquivo.name = "relatorio_sintetico.csv"

    resultado = ler_arquivo(arquivo)

    assert len(resultado) == 2
    assert resultado.loc[0, "Pessoa"] == "Fornecedor A"
    assert resultado.loc[0, "Nro Empresa"] == "9"
    assert resultado.loc[0, "Vlr Pago"] == "1.250,50"


@pytest.mark.parametrize(
    "valor_invalido",
    [
        "ABC123",
        "1.2.3,45",
        "1,2,3",
        "R$ 100,00",
        "12.34,56",
    ],
)
def test_rejeitar_valor_monetario_invalido(valor_invalido):
    """Conteúdos inválidos não podem virar zero silenciosamente."""
    serie = pd.Series([valor_invalido])

    with pytest.raises(ValueError):
        _para_numero(serie)


def test_rejeitar_coluna_obrigatoria_vazia():
    """Não aceita um relatório sem os valores financeiros exigidos."""
    dados = pd.DataFrame(
        {
            coluna: ["100,00"]
            for coluna in LAYOUT_QUITADOS.obrigatorias
        }
    )

    dados["Vlr Pago"] = [""]

    with pytest.raises(ValueError, match="Vlr Pago"):
        limpar_dados(dados, LAYOUT_QUITADOS)


def test_rejeitar_data_invalida():
    """Uma data inválida não deve desaparecer dos indicadores."""
    dados = pd.DataFrame(
        {
            coluna: ["100,00"]
            for coluna in LAYOUT_QUITADOS.obrigatorias
        }
    )

    dados["Dt. Quitação"] = ["31/02/2026"]

    with pytest.raises(ValueError, match="Dt. Quitação"):
        limpar_dados(dados, LAYOUT_QUITADOS)


def test_rejeitar_coluna_obrigatoria_ausente():
    """Identifica um relatório incompleto antes dos cálculos."""
    dados = pd.DataFrame(
        {
            "Pessoa": ["Fornecedor Teste"],
            "Espécie": ["BOL"],
        }
    )

    with pytest.raises(ValueError, match="obrigatórias ausentes"):
        limpar_dados(dados, LAYOUT_QUITADOS)


def test_preservar_zero_legitimo():
    """Um valor zero verdadeiro deve continuar sendo aceito."""
    serie = pd.Series(["0,00", "100,00", "-50,00"])

    resultado = _para_numero(serie)

    assert resultado.tolist() == pytest.approx(
        [0.0, 100.0, -50.0]
    )

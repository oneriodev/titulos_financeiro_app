"""
Preparo dos títulos em aberto: data de corte, situação e faixa de prazo.
"""

from datetime import date

import pandas as pd

from config.settings import COLUNA_DIAS_ATRASO, COLUNA_DT_VENCIMENTO

COLUNA_DIAS_PARA_VENCER = "Dias p/ Vencer"
COLUNA_SITUACAO = "Situação"
COLUNA_FAIXA_PRAZO = "Faixa de Prazo"

SITUACAO_VENCIDO = "Vencido"
SITUACAO_A_VENCER = "A vencer"

FAIXAS_PRAZO = [
    "Vencido",
    "Vence hoje",
    "1 a 7 dias",
    "8 a 15 dias",
    "16 a 30 dias",
    "Acima de 30 dias",
]
_LIMITES_FAIXAS = [-float("inf"), -1, 0, 7, 15, 30, float("inf")]


def obter_data_corte(df: pd.DataFrame) -> pd.Timestamp:
    """
    Deduz a data em que o relatório foi extraído do Consinco.

    Para os títulos atrasados, vencimento + dias de atraso = data da
    extração. O Consinco às vezes conta o atraso a partir de outra data
    (como o vencimento original de um título reprogramado), o que só
    empurra o resultado para depois. Por isso usa-se a menor data obtida.
    Sem títulos atrasados, não há como deduzir, e usa-se a data de hoje.
    """
    if COLUNA_DIAS_ATRASO not in df.columns:
        return pd.Timestamp(date.today())

    atraso = df[COLUNA_DIAS_ATRASO].fillna(0)
    atrasados = df[atraso > 0]

    if atrasados.empty:
        return pd.Timestamp(date.today())

    estimativas = atrasados[COLUNA_DT_VENCIMENTO] + pd.to_timedelta(
        atrasados[COLUNA_DIAS_ATRASO].astype(int), unit="D"
    )
    return estimativas.min().normalize()


def preparar_abertos(df: pd.DataFrame, data_corte: pd.Timestamp) -> pd.DataFrame:
    """
    Acrescenta as colunas de prazo em relação à data de corte:
    dias até o vencimento (negativo = vencido), situação e faixa.
    """
    df = df.copy()

    dias = (df[COLUNA_DT_VENCIMENTO] - data_corte).dt.days

    df[COLUNA_DIAS_PARA_VENCER] = dias.astype("Int64")

    df[COLUNA_SITUACAO] = SITUACAO_A_VENCER
    df.loc[dias < 0, COLUNA_SITUACAO] = SITUACAO_VENCIDO

    df[COLUNA_FAIXA_PRAZO] = pd.cut(
        dias, bins=_LIMITES_FAIXAS, labels=FAIXAS_PRAZO
    )

    return df
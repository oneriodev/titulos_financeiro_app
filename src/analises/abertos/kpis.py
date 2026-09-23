"""
Indicadores dos títulos em aberto.
"""

from dataclasses import dataclass

import pandas as pd

from config.settings import COLUNA_PESSOA, COLUNA_VLR_ABERTO, COLUNAS_VALORES
from src.analises.abertos.preparo import (
    COLUNA_DIAS_PARA_VENCER,
    COLUNA_SITUACAO,
    SITUACAO_VENCIDO,
)

DIAS_PROXIMA_SEMANA = 7

# Diferença mínima para considerar que houve pagamento parcial,
# evitando que arredondamentos de centavos contem como parcial.
TOLERANCIA = 0.01


@dataclass
class ResumoAbertos:
    """Indicadores exibidos na aba Resumo."""

    titulos: int
    original: float
    aberto: float
    desconto: float
    liquido: float

    vencidos_valor: float
    vencidos_titulos: int
    a_vencer_valor: float
    a_vencer_titulos: int

    proxima_semana_valor: float
    proxima_semana_titulos: int

    parciais_titulos: int
    parciais_valor: float

    ticket_medio: float
    maior_titulo_valor: float
    maior_titulo_pessoa: str


def calcular_resumo(df: pd.DataFrame) -> ResumoAbertos:
    """Calcula todos os indicadores da aba Resumo a partir da base filtrada."""
    original = df[COLUNAS_VALORES["original"]]
    aberto = df[COLUNA_VLR_ABERTO]

    vencidos = df[COLUNA_SITUACAO] == SITUACAO_VENCIDO
    a_vencer = ~vencidos

    dias = df[COLUNA_DIAS_PARA_VENCER]
    proxima_semana = (dias >= 0) & (dias <= DIAS_PROXIMA_SEMANA)

    # Títulos cujo valor em aberto é menor que o original: pagamento parcial
    diferenca = original - aberto
    parciais = diferenca > TOLERANCIA

    if len(df):
        indice_maior = aberto.idxmax()
        maior_valor = float(aberto.loc[indice_maior])
        maior_pessoa = str(df.loc[indice_maior, COLUNA_PESSOA])
    else:
        maior_valor, maior_pessoa = 0.0, "—"

    return ResumoAbertos(
        titulos=len(df),
        original=float(original.sum()),
        aberto=float(aberto.sum()),
        desconto=float(df[COLUNAS_VALORES["desconto"]].sum()),
        liquido=float(df[COLUNAS_VALORES["liquido"]].sum()),
        vencidos_valor=float(aberto[vencidos].sum()),
        vencidos_titulos=int(vencidos.sum()),
        a_vencer_valor=float(aberto[a_vencer].sum()),
        a_vencer_titulos=int(a_vencer.sum()),
        proxima_semana_valor=float(aberto[proxima_semana].sum()),
        proxima_semana_titulos=int(proxima_semana.sum()),
        parciais_titulos=int(parciais.sum()),
        parciais_valor=float(diferenca[parciais].sum()),
        ticket_medio=float(aberto.sum() / len(df)) if len(df) else 0.0,
        maior_titulo_valor=maior_valor,
        maior_titulo_pessoa=maior_pessoa,
    )
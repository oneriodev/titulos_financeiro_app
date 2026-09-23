"""
Aba Vencimentos: progressão do desembolso dos títulos em aberto.
"""

import pandas as pd
import streamlit as st

from src.analises.abertos.layout import VALORES_ABERTOS
from src.analises.abertos.metricas import (
    COLUNA_ACUMULADO,
    COLUNA_DATA,
    COLUNA_TOTAL,
    desembolso_diario,
    distribuicao_faixas,
    por_dia_semana,
)
from src.analises.abertos.preparo import SITUACAO_VENCIDO
from src.core.ui.components import formatar_moeda
from src.core.visualization.charts import (
    grafico_barras_ordenado,
    grafico_desembolso,
)

OPCOES_VALOR = [
    VALORES_ABERTOS["aberto"],
    VALORES_ABERTOS["liquido"],
    VALORES_ABERTOS["original"],
]


def renderizar_aba_vencimentos(df: pd.DataFrame, data_corte: pd.Timestamp) -> None:
    coluna_valor = st.selectbox("Valor analisado", options=OPCOES_VALOR)

    st.divider()

    # ---------------------------------------------------------------
    # Progressão do desembolso
    # ---------------------------------------------------------------
    diario = desembolso_diario(df, coluna_valor)

    st.plotly_chart(
        grafico_desembolso(
            diario,
            data_corte,
            SITUACAO_VENCIDO,
            "Progressão do desembolso por vencimento",
        ),
        width="stretch",
    )

    if not diario.empty:
        maior = diario.loc[diario[COLUNA_TOTAL].idxmax()]
        st.caption(
            f"Maior concentração em **{maior[COLUNA_DATA]:%d/%m/%Y}**, com "
            f"{formatar_moeda(maior[COLUNA_TOTAL])}. Total acumulado no "
            f"período: {formatar_moeda(diario[COLUNA_ACUMULADO].iloc[-1])}."
        )

    st.divider()

    # ---------------------------------------------------------------
    # Faixas de prazo
    # ---------------------------------------------------------------
    st.plotly_chart(
        grafico_barras_ordenado(
            distribuicao_faixas(df, coluna_valor),
            "Faixa",
            "Distribuição por faixa de prazo",
        ),
        width="stretch",
    )

    st.divider()

    # ---------------------------------------------------------------
    # Dia da semana
    # ---------------------------------------------------------------
    st.plotly_chart(
        grafico_barras_ordenado(
            por_dia_semana(df, coluna_valor),
            "Dia",
            "Concentração por dia da semana do vencimento",
        ),
        width="stretch",
    )
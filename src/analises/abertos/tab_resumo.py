"""
Aba Resumo dos títulos em aberto.
"""

import pandas as pd
import streamlit as st

from src.analises.abertos.kpis import DIAS_PROXIMA_SEMANA, calcular_resumo
from src.core.ui.components import cartao, formatar_inteiro, formatar_moeda


def renderizar_aba_resumo(df: pd.DataFrame, data_corte: pd.Timestamp) -> None:
    """Desenha os indicadores da carteira em aberto."""
    r = calcular_resumo(df)

    st.caption(
        f"Posição em **{data_corte.strftime('%d/%m/%Y')}**, "
        "data deduzida do próprio relatório."
    )

    # ---------------------------------------------------------------
    # Composição do valor
    # ---------------------------------------------------------------
    st.subheader("Composição da carteira")

    colunas = st.columns(4)
    with colunas[0]:
        cartao("Total Original", r.original,
               "Valor de face dos títulos, antes de pagamentos parciais.")
    with colunas[1]:
        cartao("Total em Aberto", r.aberto,
               "Saldo que ainda falta pagar.")
    with colunas[2]:
        cartao("Total Desconto", r.desconto,
               "Descontos previstos para o pagamento.")
    with colunas[3]:
        cartao("Total Líquido", r.liquido,
               "Valor em aberto menos os descontos.")

    if r.parciais_titulos:
        st.caption(
            f"↳ {formatar_inteiro(r.parciais_titulos)} título(s) com pagamento "
            f"parcial, somando {formatar_moeda(r.parciais_valor)} já quitados."
        )

    st.divider()

    # ---------------------------------------------------------------
    # Situação dos títulos
    # ---------------------------------------------------------------
    st.subheader("Situação")

    esquerda, direita = st.columns(2)
    with esquerda:
        st.metric(
            "Vencidos",
            formatar_moeda(r.vencidos_valor),
            f"{formatar_inteiro(r.vencidos_titulos)} título(s)",
            delta_color="off",
            help="Títulos com vencimento anterior à data do relatório.",
        )
    with direita:
        st.metric(
            "A vencer",
            formatar_moeda(r.a_vencer_valor),
            f"{formatar_inteiro(r.a_vencer_titulos)} título(s)",
            delta_color="off",
            help="Títulos que vencem na data do relatório ou depois.",
        )

    st.divider()

    # ---------------------------------------------------------------
    # Desembolso e dispersão
    # ---------------------------------------------------------------
    st.subheader("Desembolso e dispersão")

    colunas = st.columns(3)
    with colunas[0]:
        st.metric(
            f"Próximos {DIAS_PROXIMA_SEMANA} dias",
            formatar_moeda(r.proxima_semana_valor),
            f"{formatar_inteiro(r.proxima_semana_titulos)} título(s)",
            delta_color="off",
            help="Inclui os títulos que vencem na data do relatório.",
        )
    with colunas[1]:
        cartao("Valor Médio por Título", r.ticket_medio)
    with colunas[2]:
        st.metric(
            "Maior Título",
            formatar_moeda(r.maior_titulo_valor),
            r.maior_titulo_pessoa[:28],
            delta_color="off",
            help=r.maior_titulo_pessoa,
        )

    if r.aberto and r.maior_titulo_valor / r.aberto > 0.1:
        participacao = r.maior_titulo_valor / r.aberto * 100
        st.warning(
            f"Um único título representa {participacao:.1f}% da carteira. "
            "Ele domina os gráficos por valor."
        )
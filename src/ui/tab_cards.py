"""
Aba de cartões: totais gerais do conjunto de dados.
"""

import pandas as pd
import streamlit as st

from config.settings import ROTULOS_CARTOES
from src.analytics.kpis import calcular_totais, contar_registros
from src.ui.components import cartao, formatar_inteiro, formatar_moeda

# Ordem de exibição dos cartões, em duas linhas de quatro
ORDEM_CARTOES = [
    ["original", "multa", "juros", "desconto"],
    ["abatimento", "compensacao", "pago", "liquido"],
]

AJUDAS = {
    "original": "Valor de face dos títulos, antes de encargos e deduções.",
    "multa": "Multas por atraso aplicadas aos títulos.",
    "juros": "Juros incidentes sobre os títulos.",
    "desconto": "Descontos concedidos no pagamento.",
    "abatimento": "Abatimentos registrados nos títulos.",
    "compensacao": "Valores compensados com créditos existentes.",
    "pago": "Valor efetivamente pago, com encargos já embutidos.",
    "liquido": "Pago + Juros − Desconto − Compensação.",
}


def renderizar_aba_cartoes(df: pd.DataFrame) -> None:
    """Desenha os oito cartões de totais gerais."""
    totais = calcular_totais(df)

    st.subheader("Totais Gerais")

    for linha in ORDEM_CARTOES:
        colunas = st.columns(len(linha))
        for coluna, chave in zip(colunas, linha):
            with coluna:
                cartao(
                    titulo=ROTULOS_CARTOES[chave],
                    valor=totais[chave],
                    ajuda=AJUDAS.get(chave, ""),
                )

    st.divider()

    esquerda, direita = st.columns(2)
    with esquerda:
        st.metric("Quantidade de Títulos", formatar_inteiro(contar_registros(df)))
    with direita:
        ticket = totais["liquido"] / len(df) if len(df) else 0.0
        st.metric("Valor Líquido Médio por Título", formatar_moeda(ticket))
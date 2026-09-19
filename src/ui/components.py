"""
Componentes visuais reutilizáveis da interface.
"""

import streamlit as st


def formatar_moeda(valor: float) -> str:
    """
    Formata um número no padrão brasileiro: R$ 1.234.567,89.

    O Python usa vírgula para milhar e ponto para decimal, então a troca
    é feita por um marcador temporário para evitar sobrescrita.
    """
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "#").replace(".", ",").replace("#", ".")
    return f"R$ {texto}"


def formatar_inteiro(valor: int) -> str:
    """Formata um inteiro com separador de milhar brasileiro."""
    return f"{valor:,}".replace(",", ".")


def cartao(titulo: str, valor: float, ajuda: str = "") -> None:
    """Desenha um cartão de indicador com valor monetário."""
    st.metric(label=titulo, value=formatar_moeda(valor), help=ajuda or None),
"""
Construção dos gráficos com Plotly.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config.settings import (
    ALTURA_GRAFICO,
    COR_PRIMARIA,
    ESCALA_CORES,
)

# Formato monetário aplicado aos eixos e rótulos do Plotly
FORMATO_MOEDA = "R$ ,.2f"


def _aplicar_layout(fig: go.Figure, titulo: str) -> go.Figure:
    fig.update_layout(
        title=titulo,
        height=ALTURA_GRAFICO,
        margin=dict(l=40, r=20, t=60, b=40),
        separators=",.",  # vírgula decimal e ponto para milhar
        showlegend=False,
    )
    return fig


def grafico_evolucao(dados: pd.DataFrame, granularidade: str) -> go.Figure:
    """Linha com a evolução dos valores ao longo do tempo."""
    periodo = "mês" if granularidade == "mensal" else "semana"

    fig = px.line(
        dados,
        x="Período",
        y="Total",
        markers=True,
        color_discrete_sequence=[COR_PRIMARIA],
    )
    fig.update_traces(
        line=dict(width=3),
        hovertemplate="<b>%{x}</b><br>Total: R$ %{y:,.2f}<extra></extra>",
    )
    fig.update_yaxes(tickprefix="R$ ", tickformat=",.0f")
    return _aplicar_layout(fig, f"Evolução dos gastos por {periodo}")


def grafico_barras_vertical(
    dados: pd.DataFrame, coluna_categoria: str, titulo: str
) -> go.Figure:
    """Barras verticais ordenadas da maior para a menor."""
    fig = px.bar(
        dados,
        x=coluna_categoria,
        y="Total",
        color="Total",
        color_continuous_scale=ESCALA_CORES,
    )
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Total: R$ %{y:,.2f}<extra></extra>"
    )
    fig.update_xaxes(categoryorder="total descending", tickangle=-30, title=None)
    fig.update_yaxes(tickprefix="R$ ", tickformat=",.0f")
    fig.update_layout(coloraxis_showscale=False)
    return _aplicar_layout(fig, titulo)


def grafico_barras_horizontal(
    dados: pd.DataFrame, coluna_categoria: str, titulo: str
) -> go.Figure:
    """Barras horizontais, maior valor no topo."""
    fig = px.bar(
        dados.sort_values("Total"),
        x="Total",
        y=coluna_categoria,
        orientation="h",
        color="Total",
        color_continuous_scale=ESCALA_CORES,
    )
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Total: R$ %{x:,.2f}<extra></extra>"
    )
    fig.update_xaxes(tickprefix="R$ ", tickformat=",.0f")
    fig.update_yaxes(title=None)
    fig.update_layout(coloraxis_showscale=False)
    return _aplicar_layout(fig, titulo)


def grafico_pizza(dados: pd.DataFrame, coluna_categoria: str, titulo: str) -> go.Figure:
    """Pizza com participação percentual."""
    fig = px.pie(
        dados,
        names=coluna_categoria,
        values="Total",
        hole=0.35,
        color_discrete_sequence=px.colors.sequential.Blues_r,
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        hovertemplate="<b>%{label}</b><br>Juros: R$ %{value:,.2f}"
                      "<br>Participação: %{percent}<extra></extra>",
    )
    fig.update_layout(showlegend=True)
    return _aplicar_layout(fig, titulo)
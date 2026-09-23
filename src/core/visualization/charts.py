"""
Construção dos gráficos com Plotly.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from config.settings import (
    ALTURA_GRAFICO,
    COR_ACUMULADO,
    COR_ALERTA,
    COR_PRIMARIA,
    ESCALA_CORES,
)


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



def grafico_barras_ordenado(
    dados: pd.DataFrame, coluna_categoria: str, titulo: str
) -> go.Figure:
    """
    Barras verticais que preservam a ordem recebida.

    Diferente de grafico_barras_vertical, que ordena pelo valor: aqui a
    sequência das categorias é o que importa (faixas de prazo, dias da
    semana), e reordenar por valor atrapalharia a leitura.
    """
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
    fig.update_xaxes(categoryorder="array", categoryarray=dados[coluna_categoria],
                     title=None)
    fig.update_yaxes(tickprefix="R$ ", tickformat=",.0f")
    fig.update_layout(coloraxis_showscale=False)
    return _aplicar_layout(fig, titulo)


def grafico_desembolso(
    dados: pd.DataFrame,
    data_corte: pd.Timestamp,
    rotulo_vencido: str,
    titulo: str,
) -> go.Figure:
    """
    Barras com o valor de cada dia e linha com o total acumulado.

    As barras de dias já vencidos ganham cor de alerta, e uma linha
    tracejada marca a data do relatório, separando passado e futuro.
    """
    cores = [
        COR_ALERTA if situacao == rotulo_vencido else COR_PRIMARIA
        for situacao in dados["Situação"]
    ]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(
            x=dados["Data"],
            y=dados["Total"],
            marker_color=cores,
            name="Do dia",
            customdata=dados["Títulos"],
            hovertemplate="<b>%{x|%d/%m/%Y}</b><br>Do dia: R$ %{y:,.2f}"
                          "<br>Títulos: %{customdata}<extra></extra>",
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=dados["Data"],
            y=dados["Acumulado"],
            mode="lines+markers",
            line=dict(color=COR_ACUMULADO, width=3),
            name="Acumulado",
            hovertemplate="<b>%{x|%d/%m/%Y}</b>"
                          "<br>Acumulado: R$ %{y:,.2f}<extra></extra>",
        ),
        secondary_y=True,
    )

    # Meio dia antes do corte: a linha cai entre as barras, não sobre uma delas
    fig.add_vline(
        x=(data_corte - pd.Timedelta(hours=12)).strftime("%Y-%m-%dT%H:%M:%S"),
        line_dash="dash",
        line_color=COR_ALERTA,
        annotation_text=f"Posição em {data_corte.strftime('%d/%m')}",
        annotation_position="top left",
    )

    fig.update_xaxes(title=None, tickformat="%d/%m")
    fig.update_yaxes(tickprefix="R$ ", tickformat=",.0f", secondary_y=False)
    fig.update_yaxes(
        tickprefix="R$ ", tickformat=",.0f", showgrid=False, secondary_y=True
    )

    fig = _aplicar_layout(fig, titulo)
    fig.update_layout(
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
    )
    return fig
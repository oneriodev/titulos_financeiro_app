"""
Aba de métricas: gráficos analíticos do conjunto de dados.
"""

import pandas as pd
import streamlit as st

from config.settings import (
    COLUNA_DATA_PADRAO,
    COLUNA_EMPRESA,
    COLUNA_ESPECIE,
    COLUNA_PESSOA,
    COLUNA_VALOR_PADRAO,
    COLUNAS_DATAS,
    COLUNAS_VALORES,
    TOP_N_ESPECIES,
    TOP_N_JUROS,
    TOP_N_PESSOAS,
)
from src.analytics.metrics import (
    concentracao_hierarquica,
    evolucao_temporal,
    gastos_por_empresa,
    ranking_por_categoria,
    top_especies,
    top_pessoas,
)
from src.visualization.charts import (
    grafico_barras_horizontal,
    grafico_barras_vertical,
    grafico_evolucao,
)


def _seletores(df: pd.DataFrame):
    """Permite escolher a coluna de valor e a data de referência."""
    esquerda, direita = st.columns(2)

    with esquerda:
        rotulo_valor = st.selectbox(
            "Valor analisado",
            options=list(COLUNAS_VALORES.values()),
            index=list(COLUNAS_VALORES.values()).index(COLUNA_VALOR_PADRAO),
        )

    with direita:
        datas_disponiveis = [c for c in COLUNAS_DATAS if c in df.columns]
        coluna_data = st.selectbox(
            "Data de referência",
            options=datas_disponiveis,
            index=datas_disponiveis.index(COLUNA_DATA_PADRAO)
            if COLUNA_DATA_PADRAO in datas_disponiveis
            else 0,
        )

    return rotulo_valor, coluna_data


def renderizar_aba_metricas(df: pd.DataFrame) -> None:
    coluna_valor, coluna_data = _seletores(df)
    st.divider()

    # 1. Evolução no tempo
    dados_evolucao, granularidade = evolucao_temporal(df, coluna_valor, coluna_data)
    st.plotly_chart(
        grafico_evolucao(dados_evolucao, granularidade), use_container_width=True
    )
    st.caption(
        f"Agrupamento {granularidade} detectado automaticamente pelo "
        f"intervalo da coluna *{coluna_data}*."
    )

    st.divider()

    # 2. Top pessoas
    st.plotly_chart(
        grafico_barras_vertical(
            top_pessoas(df, coluna_valor, TOP_N_PESSOAS),
            COLUNA_PESSOA,
            f"Top {TOP_N_PESSOAS} pessoas por gasto",
        ),
        use_container_width=True,
    )

    st.divider()

    # 3. Concentração hierárquica
    nivel = "semana e dia" if granularidade == "semanal" else "mês e semana"
    st.subheader(f"Concentração de gastos por {nivel}")

    tabela = concentracao_hierarquica(df, coluna_valor, coluna_data)
    st.dataframe(
        tabela.style.format(
            {
                "Total": "R$ {:,.2f}".format,
                "% do Total": "{:.2f}%".format,
                "Títulos": "{:,.0f}".format,
            }
        ),
        use_container_width=True,
    )

    st.divider()

    # 4. Juros por pessoa (sempre sobre a coluna de juros)
    dados_juros = ranking_por_categoria(
        df, COLUNA_PESSOA, COLUNAS_VALORES["juros"], TOP_N_JUROS
    )
    if dados_juros.empty:
        st.info("Não há juros registrados neste conjunto de dados.")
    else:
        st.plotly_chart(
            grafico_barras_vertical(
                dados_juros,
                COLUNA_PESSOA,
                f"Top {TOP_N_JUROS} pessoas por juros pagos",
            ),
            use_container_width=True,
        )

    st.divider()

    # 5. Espécies
    st.plotly_chart(
        grafico_barras_vertical(
            top_especies(df, coluna_valor, TOP_N_ESPECIES),
            COLUNA_ESPECIE,
            f"Top {TOP_N_ESPECIES} espécies por gasto",
        ),
        use_container_width=True,
    )

    st.divider()

    # 6. Empresas
    st.plotly_chart(
        grafico_barras_horizontal(
            gastos_por_empresa(df, coluna_valor),
            COLUNA_EMPRESA,
            "Gastos por empresa",
        ),
        use_container_width=True,
    )
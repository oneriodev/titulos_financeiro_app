"""
Ponto de entrada da aplicação.
Execução: streamlit run app.py
"""

import pandas as pd
import streamlit as st

from config.settings import APP_TITLE, APP_ICON, LAYOUT, SUBTITULO
from src.analises.registro import ANALISES, QUITADOS, sugerir_analise
from src.core.extraction.file_reader import ler_arquivo
from src.core.layout import Layout
from src.core.processing.cleaning import limpar_dados
from src.core.processing.filters import aplicar_filtros
from src.core.processing.schema import validar_colunas
from src.analises.abertos.tab_vencimentos import renderizar_aba_vencimentos
from src.core.ui.components import formatar_inteiro
from src.core.ui.sidebar import (
    renderizar_filtros,
    renderizar_sidebar,
    selecionar_analise,
)
from src.ui.tab_cards import renderizar_aba_cartoes
from src.ui.tab_metrics import renderizar_aba_metricas
from src.analises.abertos.preparo import obter_data_corte
from src.analises.abertos.tab_resumo import renderizar_aba_resumo
from src.core.ui.auth import exigir_login, renderizar_usuario

st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout=LAYOUT)


@st.cache_data(show_spinner="Processando arquivo...")
def carregar_dados(arquivo, layout: Layout) -> pd.DataFrame:
    """Lê e trata o arquivo conforme o layout. O cache considera os dois."""
    bruto = ler_arquivo(arquivo)
    return limpar_dados(bruto, layout)


def main() -> None:
    if not exigir_login():
        return

    renderizar_usuario()

    st.title(f"{APP_ICON} {APP_TITLE}")
    st.caption(SUBTITULO)

    analise = ANALISES[selecionar_analise(list(ANALISES))]

    arquivo = renderizar_sidebar()

    if arquivo is None:
        st.info(
            f"⬅️ Importe o relatório de **{analise.nome}** na barra lateral "
            "para iniciar a análise."
        )
        return

    try:
        df = carregar_dados(arquivo, analise.layout)
    except Exception as erro:
        st.error(f"Falha ao processar o arquivo: {erro}")
        return

    valido, faltantes = validar_colunas(df, analise.layout.obrigatorias)
    if not valido:
        sugestao = sugerir_analise(df)
        if sugestao and sugestao != analise.nome:
            st.error(
                f"Este arquivo parece ser o relatório de **{sugestao}**, "
                f"mas a análise selecionada é **{analise.nome}**. "
                "Troque a análise na barra lateral ou importe o outro arquivo."
            )
        else:
            st.error(f"Colunas obrigatórias ausentes: {', '.join(faltantes)}")
        return

        data_corte = None
    if analise.preparo is not None:
        data_corte = obter_data_corte(df)
        df = analise.preparo(df)

    coluna_data = analise.layout.data_referencia
    filtros = renderizar_filtros(df, arquivo.name, coluna_data)
    df_filtrado = aplicar_filtros(df, filtros, coluna_data)

    if filtros.quantidade_ativos:
        st.caption(
            f"🔎 {filtros.quantidade_ativos} filtro(s) ativo(s) — exibindo "
            f"**{formatar_inteiro(len(df_filtrado))}** de "
            f"{formatar_inteiro(len(df))} títulos."
        )

    if df_filtrado.empty:
        st.warning("Nenhum título atende aos filtros selecionados.")
        return

    if analise.nome == QUITADOS:
        aba_cartoes, aba_metricas, aba_dados = st.tabs(
            ["📊 Cartões", "📈 Métricas", "🗂️ Dados"]
        )
        with aba_cartoes:
            renderizar_aba_cartoes(df_filtrado)
        with aba_metricas:
            renderizar_aba_metricas(df_filtrado)
    else:
        aba_resumo, aba_vencimentos, aba_dados = st.tabs(
            ["📋 Resumo", "📅 Vencimentos", "🗂️ Dados"]
        )
        with aba_resumo:
            renderizar_aba_resumo(df_filtrado, data_corte)
        with aba_vencimentos:
            renderizar_aba_vencimentos(df_filtrado, data_corte)

    with aba_dados:
        st.write(
            f"**{formatar_inteiro(len(df_filtrado))} registros** e "
            f"{df_filtrado.shape[1]} colunas."
        )
        st.dataframe(df_filtrado, width="stretch", height=500)


if __name__ == "__main__":
    main()
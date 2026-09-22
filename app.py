"""
Ponto de entrada da aplicação.
Execução: streamlit run app.py
"""

import pandas as pd
import streamlit as st

from config.settings import APP_TITLE, APP_ICON, LAYOUT, SUBTITULO
from src.analises.quitados.layout import LAYOUT_QUITADOS
from src.core.extraction.file_reader import ler_arquivo
from src.core.layout import Layout
from src.core.processing.cleaning import limpar_dados
from src.core.processing.filters import aplicar_filtros
from src.core.processing.schema import validar_colunas
from src.core.ui.components import formatar_inteiro
from src.core.ui.sidebar import renderizar_filtros, renderizar_sidebar
from src.ui.tab_cards import renderizar_aba_cartoes
from src.ui.tab_metrics import renderizar_aba_metricas

st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout=LAYOUT)


@st.cache_data(show_spinner="Processando arquivo...")
def carregar_dados(arquivo, layout: Layout) -> pd.DataFrame:
    """Lê e trata o arquivo conforme o layout. O cache considera os dois."""
    bruto = ler_arquivo(arquivo)
    return limpar_dados(bruto, layout)


def main() -> None:
    st.title(f"{APP_ICON} {APP_TITLE}")
    st.caption(SUBTITULO)

    layout = LAYOUT_QUITADOS

    arquivo = renderizar_sidebar()

    if arquivo is None:
        st.info("⬅️ Importe um arquivo na barra lateral para iniciar a análise.")
        return

    try:
        df = carregar_dados(arquivo, layout)
    except Exception as erro:
        st.error(f"Falha ao processar o arquivo: {erro}")
        return

    valido, faltantes = validar_colunas(df, layout.obrigatorias)
    if not valido:
        st.error(f"Colunas obrigatórias ausentes: {', '.join(faltantes)}")
        return

    filtros = renderizar_filtros(df, arquivo.name, layout.data_referencia)
    df_filtrado = aplicar_filtros(df, filtros, layout.data_referencia)

    if filtros.quantidade_ativos:
        st.caption(
            f"🔎 {filtros.quantidade_ativos} filtro(s) ativo(s) — exibindo "
            f"**{formatar_inteiro(len(df_filtrado))}** de "
            f"{formatar_inteiro(len(df))} títulos."
        )

    if df_filtrado.empty:
        st.warning("Nenhum título atende aos filtros selecionados.")
        return

    aba_cartoes, aba_metricas, aba_dados = st.tabs(
        ["📊 Cartões", "📈 Métricas", "🗂️ Dados"]
    )

    with aba_cartoes:
        renderizar_aba_cartoes(df_filtrado)

    with aba_metricas:
        renderizar_aba_metricas(df_filtrado)

    with aba_dados:
        st.write(
            f"**{formatar_inteiro(len(df_filtrado))} registros** e "
            f"{df_filtrado.shape[1]} colunas."
        )
        st.dataframe(df_filtrado, width="stretch", height=500)


if __name__ == "__main__":
    main()
"""
Ponto de entrada da aplicação.
Execução: streamlit run app.py
"""

import pandas as pd
import streamlit as st

from config.settings import APP_TITLE, APP_ICON, LAYOUT, SUBTITULO
from src.extraction.file_reader import ler_arquivo
from src.processing.cleaning import limpar_dados
from src.processing.schema import validar_colunas
from src.ui.sidebar import renderizar_sidebar
from src.ui.tab_cards import renderizar_aba_cartoes
from src.ui.tab_metrics import renderizar_aba_metricas

st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout=LAYOUT)


@st.cache_data(show_spinner="Processando arquivo...")
def carregar_dados(arquivo) -> pd.DataFrame:
    """Lê e trata o arquivo. O cache evita reprocessar a cada interação."""
    bruto = ler_arquivo(arquivo)
    return limpar_dados(bruto)


def main() -> None:
    st.title(f"{APP_ICON} {APP_TITLE}")
    st.caption(SUBTITULO)

    arquivo = renderizar_sidebar()

    if arquivo is None:
        st.info("⬅️ Importe um arquivo na barra lateral para iniciar a análise.")
        return

    try:
        df = carregar_dados(arquivo)
    except Exception as erro:
        st.error(f"Falha ao processar o arquivo: {erro}")
        return

    valido, faltantes = validar_colunas(df)
    if not valido:
        st.error(f"Colunas obrigatórias ausentes: {', '.join(faltantes)}")
        return

    st.session_state["df"] = df

    aba_cartoes, aba_metricas, aba_dados = st.tabs(
        ["📊 Cartões", "📈 Métricas", "🗂️ Dados"]
    )

    with aba_cartoes:
        renderizar_aba_cartoes(df)

    with aba_metricas:
        renderizar_aba_metricas(df)

    with aba_dados:
        st.write(f"**{len(df):,} registros** e {df.shape[1]} colunas.".replace(",", "."))
        st.dataframe(df, use_container_width=True, height=500)


if __name__ == "__main__":
    main()
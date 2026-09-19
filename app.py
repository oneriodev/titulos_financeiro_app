"""
Ponto de entrada da aplicação.
Execução: streamlit run app.py
"""

import streamlit as st

from config.settings import APP_TITLE, APP_ICON, LAYOUT, SUBTITULO

# Deve ser o primeiro comando Streamlit do script
st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout=LAYOUT)


def main() -> None:
    st.title(f"{APP_ICON} {APP_TITLE}")
    st.caption(SUBTITULO)

    aba_cartoes, aba_metricas = st.tabs(["📊 Cartões", "📈 Métricas"])

    with aba_cartoes:
        st.info("Aba de cartões em construção.")

    with aba_metricas:
        st.info("Aba de métricas em construção.")


if __name__ == "__main__":
    main()

"""
Componente de interface para exportar dados financeiros.

O componente é compartilhado entre Quitados e Abertos.
Não grava arquivos no servidor.
"""

from datetime import date

import pandas as pd
import streamlit as st

from src.core.exportacao import (
    exportar_csv,
    exportar_xlsx,
)


@st.dialog("Exportar Dados")
def _confirmar_exportacao(
    df: pd.DataFrame,
    identificador: str,
) -> None:
    """
    Apresenta as opções de exportação em uma janela.

    Os bytes são gerados somente após a escolha do formato.
    """
    st.write(
        "Escolha o formato para exportar os dados tratados."
    )

    st.caption(
        f"Serão exportados {len(df):,} registros, "
        "respeitando os filtros aplicados."
    )

    formato = st.radio(
        "Formato do arquivo",
        options=["CSV", "XLSX"],
        horizontal=True,
        key="formato_exportacao",
    )

    extensao = formato.lower()
    nome_arquivo = (
        f"titulos_{identificador}_"
        f"{date.today():%Y-%m-%d}.{extensao}"
    )

    if formato == "CSV":
        dados = exportar_csv(df)
        tipo_mime = "text/csv"
    else:
        dados = exportar_xlsx(df)
        tipo_mime = (
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )

    st.download_button(
        label=f"📥 Confirmar e baixar {formato}",
        data=dados,
        file_name=nome_arquivo,
        mime=tipo_mime,
        type="primary",
        use_container_width=True,
        on_click="ignore",
    )

    if st.button(
        "Cancelar",
        use_container_width=True,
    ):
        st.rerun()


def renderizar_exportacao(
    df: pd.DataFrame,
    identificador: str,
) -> None:
    """
    Exibe o botão de exportação da aba Dados.

    Recebe a base já tratada e filtrada para evitar
    divergências entre a tabela e o arquivo exportado.
    """
    st.divider()

    if st.button(
        "📤 Exportar Dados",
        key=f"exportar_{identificador}",
    ):
        _confirmar_exportacao(df, identificador)

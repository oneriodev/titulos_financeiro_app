"""
Barra lateral da aplicação: upload e validação inicial do arquivo.
"""

from typing import Optional

import streamlit as st

from config.settings import EXTENSOES_ACEITAS, TAMANHO_MAX_MB


def _tamanho_em_mb(arquivo) -> float:
    """Retorna o tamanho do arquivo enviado em megabytes."""
    return arquivo.size / (1024 * 1024)


def renderizar_sidebar() -> Optional[object]:
    """
    Desenha a barra lateral e devolve o arquivo enviado pelo usuário.

    Retorna None enquanto nenhum arquivo válido for carregado.
    """
    with st.sidebar:
        st.header("📂 Importar dados")

        arquivo = st.file_uploader(
            label="Selecione o relatório de títulos",
            type=EXTENSOES_ACEITAS,
            accept_multiple_files=False,
            help=f"Formatos aceitos: {', '.join(EXTENSOES_ACEITAS).upper()}. "
                 f"Tamanho máximo: {TAMANHO_MAX_MB} MB.",
        )

        if arquivo is None:
            st.info("Nenhum arquivo carregado.")
            return None

        tamanho = _tamanho_em_mb(arquivo)

        if tamanho > TAMANHO_MAX_MB:
            st.error(
                f"Arquivo com {tamanho:.1f} MB excede o limite "
                f"de {TAMANHO_MAX_MB} MB."
            )
            return None

        st.success("Arquivo carregado.")
        st.caption(f"**{arquivo.name}** — {tamanho:.2f} MB")

        if st.button("🗑️ Limpar dados", use_container_width=True):
            st.session_state.clear()
            st.rerun()

        return arquivo
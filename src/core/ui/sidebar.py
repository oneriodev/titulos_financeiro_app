"""
Barra lateral da aplicação: upload do arquivo e filtros.
"""

from typing import Optional

import pandas as pd
import streamlit as st

from config.settings import (
    COLUNA_EMPRESA,
    COLUNA_ESPECIE,
    EXTENSOES_ACEITAS,
    TAMANHO_MAX_MB,
)
from src.core.processing.filters import Filtros

CHAVE_PERIODO = "filtro_periodo"
CHAVE_EMPRESAS = "filtro_empresas"
CHAVE_ESPECIES = "filtro_especies"
CHAVE_ARQUIVO = "_arquivo_dos_filtros"
CHAVES_FILTROS = [CHAVE_PERIODO, CHAVE_EMPRESAS, CHAVE_ESPECIES]

# Versão do uploader: trocar a chave força o Streamlit a criar
# um uploader novo, descartando o arquivo carregado.
CHAVE_VERSAO_UPLOADER = "_versao_uploader"


# ---------------------------------------------------------------------
# Upload
# ---------------------------------------------------------------------
def _tamanho_em_mb(arquivo) -> float:
    """Retorna o tamanho do arquivo enviado em megabytes."""
    return arquivo.size / (1024 * 1024)


def _limpar_dados() -> None:
    """
    Zera todo o estado da aplicação e descarta o arquivo carregado.

    O contador de versão é preservado e incrementado, para que o
    uploader receba uma chave nova após o clear().
    """
    proxima_versao = st.session_state.get(CHAVE_VERSAO_UPLOADER, 0) + 1
    st.session_state.clear()
    st.session_state[CHAVE_VERSAO_UPLOADER] = proxima_versao


def renderizar_sidebar() -> Optional[object]:
    """
    Desenha a área de upload e devolve o arquivo enviado pelo usuário.

    Retorna None enquanto nenhum arquivo válido for carregado.
    """
    versao = st.session_state.setdefault(CHAVE_VERSAO_UPLOADER, 0)

    with st.sidebar:
        st.header("📂 Importar dados")

        arquivo = st.file_uploader(
            label="Selecione o relatório de títulos",
            type=EXTENSOES_ACEITAS,
            accept_multiple_files=False,
            help=f"Formatos aceitos: {', '.join(EXTENSOES_ACEITAS).upper()}. "
                 f"Tamanho máximo: {TAMANHO_MAX_MB} MB.",
            key=f"uploader_{versao}",
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

        if st.button("🗑️ Limpar dados", width="stretch"):
            _limpar_dados()
            st.rerun()

        return arquivo


# ---------------------------------------------------------------------
# Filtros
# ---------------------------------------------------------------------
def _limpar_filtros() -> None:
    for chave in CHAVES_FILTROS:
        st.session_state.pop(chave, None)


def renderizar_filtros(
    df: pd.DataFrame, nome_arquivo: str, coluna_data: str
) -> Filtros:
    """
    Desenha os filtros com base nos valores existentes no arquivo
    e devolve as seleções do usuário.
    """
    # Um arquivo novo pode ter outro intervalo de datas e outras empresas.
    # Filtros antigos causariam erro ou esconderiam dados, então são zerados.
    if st.session_state.get(CHAVE_ARQUIVO) != nome_arquivo:
        _limpar_filtros()
        st.session_state[CHAVE_ARQUIVO] = nome_arquivo

    data_min = df[COLUNA_DATA_PADRAO].min().date()
    data_max = df[COLUNA_DATA_PADRAO].max().date()

    empresas = sorted(int(e) for e in df[COLUNA_EMPRESA].dropna().unique())
    especies = sorted(df[COLUNA_ESPECIE].dropna().unique())

    with st.sidebar:
        st.divider()
        st.header("🔎 Filtros")

        # O botão vem antes dos widgets para poder zerá-los com segurança
        if st.button("↺ Limpar filtros", width="stretch"):
            _limpar_filtros()
            st.rerun()

        periodo = st.date_input(
            f"Período ({COLUNA_DATA_PADRAO})",
            value=(data_min, data_max),
            min_value=data_min,
            max_value=data_max,
            format="DD/MM/YYYY",
            key=CHAVE_PERIODO,
        )

        empresas_sel = st.multiselect(
            "Empresa",
            options=empresas,
            format_func=lambda e: f"Empresa {e}",
            placeholder="Todas",
            key=CHAVE_EMPRESAS,
        )

        especies_sel = st.multiselect(
            "Espécie",
            options=especies,
            placeholder="Todas",
            key=CHAVE_ESPECIES,
        )

    # Enquanto o usuário escolhe o intervalo, o date_input devolve só a
    # data inicial. Nesse caso, a data final continua sendo a máxima.
    if isinstance(periodo, (tuple, list)):
        inicio = periodo[0] if len(periodo) > 0 else data_min
        fim = periodo[1] if len(periodo) > 1 else data_max
    else:
        inicio, fim = periodo, data_max

    # Intervalo completo não conta como filtro ativo
    return Filtros(
        data_inicio=inicio if inicio != data_min else None,
        data_fim=fim if fim != data_max else None,
        empresas=list(empresas_sel),
        especies=list(especies_sel),
    )
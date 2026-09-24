"""
Controle de acesso à aplicação.

As credenciais ficam fora do código, em .streamlit/secrets.toml
(ignorado pelo Git) ou no painel de Secrets do Streamlit Cloud.
Apenas o hash da senha é armazenado, nunca a senha em si.
"""

import hashlib
import hmac
from typing import Optional

import streamlit as st

CHAVE_USUARIO = "_usuario_autenticado"
SECAO_CREDENCIAIS = "credenciais"


def gerar_hash(senha: str) -> str:
    """Converte a senha em hash SHA-256."""
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()


def _buscar_credenciais() -> Optional[dict]:
    """Lê a seção de credenciais dos secrets, se existir."""
    try:
        return dict(st.secrets[SECAO_CREDENCIAIS])
    except Exception:
        return None


def _validar(usuario: str, senha: str) -> Optional[dict]:
    """
    Confere usuário e senha.

    O compare_digest compara os hashes em tempo constante, sem revelar
    pelo tempo de resposta quantos caracteres estavam certos.
    """
    credenciais = _buscar_credenciais()
    if not credenciais:
        return None

    dados = credenciais.get(usuario.strip().lower())
    if not dados:
        return None

    if hmac.compare_digest(gerar_hash(senha), dados.get("senha_hash", "")):
        return {"usuario": usuario.strip().lower(), **dict(dados)}

    return None


def exigir_login() -> bool:
    """
    Desenha a tela de login enquanto o usuário não estiver autenticado.

    Retorna True quando o acesso está liberado.
    """
    if st.session_state.get(CHAVE_USUARIO):
        return True

    if _buscar_credenciais() is None:
        st.error(
            "Credenciais não configuradas. Defina a seção "
            "`[credenciais]` em `.streamlit/secrets.toml` (execução local) "
            "ou no painel de Secrets do Streamlit Cloud."
        )
        return False

    _, centro, _ = st.columns([1, 2, 1])

    with centro:
        st.subheader("Acesso restrito")
        st.caption("Informe suas credenciais para continuar.")

        with st.form("login"):
            usuario = st.text_input("Usuário")
            senha = st.text_input("Senha", type="password")
            entrar = st.form_submit_button("Entrar", width="stretch")

        if entrar:
            dados = _validar(usuario, senha)
            if dados:
                st.session_state[CHAVE_USUARIO] = dados
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos.")

    return False


def renderizar_usuario() -> None:
    """Mostra o usuário conectado e o botão de sair na barra lateral."""
    dados = st.session_state.get(CHAVE_USUARIO, {})

    with st.sidebar:
        st.caption(
            f"**{dados.get('nome', dados.get('usuario', ''))}**  \n"
            f"{dados.get('papel', '')}"
        )
        if st.button("Sair", width="stretch"):
            st.session_state.clear()
            st.rerun()
        st.divider()
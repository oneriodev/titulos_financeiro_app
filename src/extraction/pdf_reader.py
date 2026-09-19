"""
Leitura bruta do arquivo enviado, sem tratamento.
Escolhe o leitor conforme a extensão e devolve um DataFrame.
"""

import io

import pandas as pd

from config.settings import ENCODINGS_TENTATIVAS, SEPARADORES_TENTATIVAS


def _ler_xlsx(arquivo) -> pd.DataFrame:
    return pd.read_excel(arquivo, engine="openpyxl")


def _ler_texto(arquivo) -> pd.DataFrame:
    """
    Lê CSV ou TXT delimitado, testando codificações e separadores.
    Um resultado com apenas uma coluna indica separador incorreto.
    """
    bytes_arquivo = arquivo.getvalue()

    for encoding in ENCODINGS_TENTATIVAS:
        try:
            texto = bytes_arquivo.decode(encoding)
        except UnicodeDecodeError:
            continue

        for separador in SEPARADORES_TENTATIVAS:
            df = pd.read_csv(io.StringIO(texto), sep=separador, dtype=str)
            if df.shape[1] > 1:
                return df

    raise ValueError(
        "Não foi possível identificar a codificação ou o separador do arquivo."
    )


def _ler_pdf(arquivo) -> pd.DataFrame:
    raise NotImplementedError(
        "A leitura de PDF ainda não foi implementada. "
        "Utilize a exportação em XLSX, CSV ou TXT."
    )


LEITORES = {
    "xlsx": _ler_xlsx,
    "csv": _ler_texto,
    "txt": _ler_texto,
    "pdf": _ler_pdf,
}


def ler_arquivo(arquivo) -> pd.DataFrame:
    """Roteia o arquivo enviado para o leitor correspondente à extensão."""
    extensao = arquivo.name.rsplit(".", 1)[-1].lower()

    leitor = LEITORES.get(extensao)
    if leitor is None:
        raise ValueError(f"Extensão não suportada: .{extensao}")

    return leitor(arquivo)
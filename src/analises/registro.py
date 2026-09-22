"""
Registro das análises disponíveis.

Cada análise reúne o layout do seu relatório, o preparo dos dados e as
colunas que identificam o arquivo. O app consulta este registro em vez
de conhecer cada análise individualmente.
"""

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

import pandas as pd

from src.analises.abertos.layout import LAYOUT_ABERTOS
from src.analises.abertos.preparo import preparar
from src.analises.quitados.layout import LAYOUT_QUITADOS
from src.core.layout import Layout

QUITADOS = "Títulos Quitados"
ABERTOS = "Títulos Abertos"


@dataclass(frozen=True)
class Analise:
    """Uma análise oferecida pela aplicação."""

    nome: str
    layout: Layout

    # Colunas do arquivo original que só existem neste relatório.
    # Servem para avisar quando o usuário importa o arquivo da outra análise.
    assinatura: List[str] = field(default_factory=list)

    # Colunas calculadas após o tratamento, quando a análise precisa
    preparo: Optional[Callable[[pd.DataFrame], pd.DataFrame]] = None


ANALISES: Dict[str, Analise] = {
    QUITADOS: Analise(
        nome=QUITADOS,
        layout=LAYOUT_QUITADOS,
        assinatura=["Dt. Quitação", "Vlr Pago"],
    ),
    ABERTOS: Analise(
        nome=ABERTOS,
        layout=LAYOUT_ABERTOS,
        assinatura=["Valor Aberto"],
        preparo=preparar,
    ),
}


def sugerir_analise(df: pd.DataFrame) -> Optional[str]:
    """
    Identifica a qual análise o arquivo pertence pelas colunas presentes.

    Usado quando a validação falha: como a renomeação da análise errada
    não encontra as colunas do arquivo, os nomes originais permanecem
    intactos e permitem reconhecer o relatório.
    """
    for nome, analise in ANALISES.items():
        if analise.assinatura and all(c in df.columns for c in analise.assinatura):
            return nome
    return None
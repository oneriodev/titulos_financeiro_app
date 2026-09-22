"""
Descrição de um relatório do Consinco.

Cada análise declara um Layout com as regras do seu arquivo. O núcleo
recebe o layout por parâmetro e aplica as regras sem saber de qual
análise se trata.
"""

from dataclasses import dataclass, field
from typing import Dict, List

from config.settings import COLUNA_EMPRESA, COLUNA_ESPECIE, COLUNA_PESSOA


@dataclass(frozen=True)
class Layout:
    """Regras de leitura e tratamento de um relatório."""

    nome: str
    renomear: Dict[str, str]          # nome no arquivo -> nome padronizado
    datas: List[str]                  # colunas convertidas para data
    valores: Dict[str, str]           # chave interna -> coluna monetária
    obrigatorias: List[str]           # sem elas a análise não funciona
    data_referencia: str              # data do filtro de período
    descartadas: List[str] = field(default_factory=list)
    inteiros: List[str] = field(default_factory=lambda: [COLUNA_EMPRESA])
    textos: List[str] = field(
        default_factory=lambda: [COLUNA_PESSOA, COLUNA_ESPECIE]
    )
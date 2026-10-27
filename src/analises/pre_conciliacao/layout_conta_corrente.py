
"""
Layout do relatório de Conta Corrente exportado do TOTVS Consinco.

Utiliza o núcleo compartilhado de tratamento para padronizar
arquivos TXT, CSV e XLSX sem duplicar regras de leitura.

Os débitos e créditos são mantidos como valores positivos neste
layout. O sinal financeiro será calculado em uma etapa posterior.
"""

from config.settings import COLUNA_EMPRESA
from src.core.layout import Layout


LAYOUT_CONTA_CORRENTE = Layout(
    nome="conta_corrente",

    # Nomes originais do relatório -> nomes internos.
    renomear={
        "loja": COLUNA_EMPRESA,
        "Conta Corrente": "Conta Corrente",
        "Documento": "Documento",
        "Serie": "Série",
        "Data Lançamento": "Data Lançamento",
        "Operações": "Operação",
        "Data Conciliação": "Data Conciliação",
        "Data Compensação": "Data Compensação",
        "Historico": "Histórico",
        "Concilado": "Conciliado ERP",
        "Valor": "Valor",
        "Tipo de Lançamento": "Tipo de Lançamento",
        "Saldo": "Saldo",
    },

    # Datas reconhecidas pelo processamento compartilhado.
    datas=[
        "Data Lançamento",
        "Data Conciliação",
        "Data Compensação",
    ],

    # Campos monetários presentes no extrato.
    valores={
        "movimento": "Valor",
        "saldo": "Saldo",
    },

    # Sem essas informações não é possível preparar
    # o relatório para uma comparação financeira segura.
    obrigatorias=[
        COLUNA_EMPRESA,
        "Conta Corrente",
        "Data Lançamento",
        "Valor",
        "Tipo de Lançamento",
    ],

    # Data utilizada como referência para os filtros.
    data_referencia="Data Lançamento",

    # Coluna auxiliar gerada durante algumas exportações.
    descartadas=["Column1"],

    # Somente a empresa será convertida para inteiro.
    # Operação e conta podem conter códigos significativos.
    inteiros=[COLUNA_EMPRESA],

    # Preserva códigos e descrições como texto.
    textos=[
        "Conta Corrente",
        "Documento",
        "Série",
        "Operação",
        "Histórico",
        "Conciliado ERP",
        "Tipo de Lançamento",
    ],
)

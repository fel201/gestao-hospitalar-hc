import unicodedata


def remover_acentos(texto: str):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )
    
# retorna "0" se caso o valor for menor que 0.000
def padronizar_casas_decimais(valor: float):
    return f"{valor:.3f}".rstrip("0").rstrip(".")
    
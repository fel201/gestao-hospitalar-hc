def divisao_segura(numerador: float, denominador: float, default: float = 0) -> float:
    if not denominador:
        return default
    return numerador / denominador
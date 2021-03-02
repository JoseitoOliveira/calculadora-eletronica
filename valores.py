from typing import Iterable
res = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8,
        2, 2.2, 2.4, 2.7, 3, 3.3, 3.6, 3.9,
        4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5,
        8.2, 9.1]

cap = [1.0, 1.2, 2.2, 3.3, 4.7, 5.6, 6.8, 8.2]


def resistores_mul(mult:Iterable):
    """
    Retorna resistores com os multiplicadores passados
    """
    return [m*v for m in mult for v in res]

def capacitores_mul(mult:Iterable):
    """
    Retorna capacitores com os multiplicadores passados
    """
    return [m*v for m in mult for v in cap]
from collections import namedtuple
from math import inf, pi, sqrt
from typing import Tuple

from tqdm import tqdm
from pprint import pprint

from valores import capacitores_mul, resistores_mul

dois_pi = 2*pi

fc_ref = 2000
Q_ref = 2

resistores = resistores_mul([1000])
capacitores = capacitores_mul([1e-6])


def sallen_key(r1, r2, c1, c2):
    fc = 1./(dois_pi*sqrt(r1*r2*c1*c2))
    q = 1./(dois_pi*fc*c1*(r1+r2))
    return fc, q


class Salle_Key:
    def __init__(self, r1, r2, c1, c2) -> None:
        self.r1 = r1
        self.r2 = r2
        self.c1 = c1
        self.c2 = c2

    def calculate_fc_Q(self) -> Tuple[float, float]:
        self.fc = 1./(dois_pi*sqrt(self.r1*self.r2*self.c1*self.c2))
        self.q = 1./(dois_pi*self.fc*self.c1*(self.r1+self.r2))
        return self.fc, self.q

    def __repr__(self) -> str:
        return f"fc:{self.fc}, Q:{self.q}, r1:{self.r1}, r2:{self.r2}, c1:{self.c1}, c2:{self.c2}"

    def __eq__(self, o: object) -> bool:
        if (self.r1 == o.r1 and
            self.r2 == o.r2 and
            self.c1 == o.c1 and
                self.c2 == o.c2):
            return True
        else:
            return False

    def __hash__(self) -> int:
        return hash(f'{self.r1}{self.r2}{self.c1}{self.c2}')


def calc(resistores,
         capacitores,
         m_r1=None,
         m_r2=None,
         m_c1=None,
         m_c2=None,
         m_erro=inf,
         filtros=set()):

    erro_pct = fc_ref/100
    for r1 in tqdm(resistores + [m_r1] if m_r1 else resistores):
        for r2 in resistores + [m_r2] if m_r2 else resistores:
            for c1 in capacitores + [m_c1] if m_c1 else capacitores:
                for c2 in capacitores + [m_c2] if m_c2 else capacitores:
                    sk = Salle_Key(r1, r2, c1, c2)
                    fc, Q = sk.calculate_fc_Q()
                    erro_fc = (fc_ref-fc)**2
                    erro_Q = (Q_ref-Q)**2

                    erro = erro_fc + erro_Q

                    if erro < m_erro:
                        m_r1 = r1
                        m_r2 = r2
                        m_c1 = c1
                        m_c2 = c2
                        m_erro = erro

                    elif erro < fc/100 and sk not in filtros:
                        filtros.add(sk)

    if m_c1 == min(capacitores) or m_c2 == min(capacitores):
        return calc(resistores, [c/10 for c in capacitores], m_c1=m_c1, m_c2=m_c2, m_erro=m_erro, filtros=filtros)

    elif m_r1 == max(resistores) or m_r2 == max(resistores):
        return calc([r*10 for r in resistores], capacitores, m_r1=m_c1, m_r2=m_c2, m_erro=m_erro, filtros=filtros)

    elif m_r1 == min(resistores) or m_r2 == min(resistores):
        return calc([r/10 for r in resistores], capacitores, m_r1=m_c1, m_r2=m_c2, m_erro=m_erro, filtros=filtros)

    elif m_c1 == max(capacitores) or m_c2 == max(capacitores):
        return calc(resistores, [c*10 for c in capacitores], m_c1=m_c1, m_c2=m_c2, m_erro=m_erro, filtros=filtros)
    
    return filtros


filtros = calc(resistores, capacitores)
pprint(filtros)

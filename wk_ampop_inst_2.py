from browser import bind, self

from resistores import valores


def amplificador_instrumentação(v_mais, v_menos, r1, r2):
    vout1 = v_menos * (1+(r2/r1)) * (-r1/r2)
    vout2 = v_mais * (1+(r1/r2))
    return vout2 + vout1


def send_result(vout1, vout2, m_r1, m_r2):
    self.send({
        'type': 'result',
        'r1': m_r1,
        'r2': m_r2,
        'vout1': vout1,
        'vout2': vout2,
    })


@bind(self, "message")
def worker(ev):
    vin_mais_1 = ev.data['vin_mais_1']
    vin_menos_1 = ev.data['vin_menos_1']
    vout_ref_1 = ev.data['vout_ref_1']

    vin_mais_2 = ev.data['vin_mais_2']
    vin_menos_2 = ev.data['vin_menos_2']
    vout_ref_2 = ev.data['vout_ref_2']

    mult = ev.data['mult']

    resistores = [m*v for m in mult for v in valores]

    m_erro = 1000
    m_r1 = int()
    m_r2 = int()

    i_max = len(resistores)**2 / 100
    i = 0

    for r1 in resistores:
        for r2 in resistores:
            vout_1 = amplificador_instrumentação(vin_mais_1,
                                                    vin_menos_1,
                                                    r1, r2)
            vout_2 = amplificador_instrumentação(vin_mais_2,
                                                    vin_menos_2,
                                                    r1, r2)

            erro_1 = abs(vout_ref_1-vout_1)
            erro_2 = abs(vout_ref_2-vout_2)

            erro = erro_1 + erro_2

            if erro < 0.0005:
                send_result(vout_1, vout_2, r1, r2)

            if erro < m_erro:
                m_erro = erro
                m_r1 = r1
                m_r2 = r2


            i += 1
            pct = int(i/i_max)
            if pct % 5 == 0:
                self.send({
                    'type': 'progress',
                    'value': pct
                })

    vout_1 = amplificador_instrumentação(vin_mais_1, vin_menos_1,
                                         m_r1, m_r2)
    vout_2 = amplificador_instrumentação(vin_mais_2, vin_menos_2,
                                         m_r1, m_r2)
    send_result(vout_1, vout_2, m_r1, m_r2)

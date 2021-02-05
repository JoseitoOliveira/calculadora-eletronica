from browser import bind, self

from resistores import valores


def divisor_resistivo(vin, r1, r2):
    return vin*r2/(r1+r2)


def send_result(r1, r2, erro, vout):
    self.send({
        'type': 'result',
        'r1': r1,
        'r2': r2,
        'erro': erro,
        'vout': vout
    })


@bind(self, "message")
def worker(ev):
    vout_ref = ev.data['vout_ref']
    vin = ev.data['vin']
    mult = ev.data['mult']

    resistores = [m*v for m in mult for v in valores]

    m_erro = 1000
    m_r1 = 0
    m_r2 = 0

    i_max = len(resistores) / 100
    i = 0
    for r1 in resistores:
        for r2 in resistores:
            vout = divisor_resistivo(vin, r1, r2)
            erro = abs(vout_ref-vout)
            if erro <= m_erro:
                m_erro = erro
                m_r1 = r1
                m_r2 = r2

            if erro < 0.01:
                send_result(r1, r2, erro, vout)

        i += 1
        pct = int(i/i_max)
        if pct % 25 == 0:
            self.send({
                'type': 'progress',
                'value': pct
            })

    vout = divisor_resistivo(vin, m_r1, m_r2)
    send_result(m_r1, m_r2, m_erro, vout)

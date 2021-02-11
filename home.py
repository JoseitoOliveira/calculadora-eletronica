from typing import Dict

pages = [
    {
        'title': 'Divisor Resistivo',
        'text': 'Cálculo de divisor resistivo com resistores comerciais.',
        'href': 'divisor_resistivo.html',
        'img': 'Voltage_divider.svg',
    },
    {
        'title': 'INA Clássico',
        'text': 'Cálculo de INA clássico com resistores comerciais.',
        'href': 'ampop_inst.html',
        'img': 'Op-Amp_Instrumentation.svg'
    },
    {
        'title': 'INA 2 Amp-ops',
        'text': 'Cálculo de INA com 2 amp-ops com resistores comerciais.',
        'href': 'ampop_inst_2.html',
        'img': 'Amp-op_inst_reduzido.png'
    },
]


def nav_item(c: Dict):
    return (
        f"""
        <li class="nav-item">
            <a class="nav-link" id="sources/{c['href']}">{c['title']}</a>
        </li>
        """
    )


def card(c: Dict):
    return (
        f"""<div class="card">
                <img src="images/{c["img"]}" class="card-img-top" alt="{c["title"]}">
                <div class="card-body">
                    <h5 class="card-title">{c["title"]}</h5>
                    <p class="card-text">{c["text"]}</p>
                    <a href="sources/{c["href"]}" class="btn btn-primary">Ir</a>
                </div>
            </div>"""
    )

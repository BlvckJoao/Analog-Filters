import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing(file='rc_highpass_diagram.svg') as d:
    d.config(unit=3)
    # Fonte senoidal
    vin = d.add(elm.SourceSin().label('Vin', loc='left'))
    # Capacitor em série
    c = d.add(elm.Capacitor().right().label('C'))
    # Nó de saída +
    d.add(elm.Dot(open=True).at(c.end).label('Vout+', loc='right'))
    # Resistor para o terra
    r = d.add(elm.Resistor().down().label('R'))
    d.add(elm.Dot(open=True).at(r.end).label('Vout-', loc='right'))
    d.add(elm.Line().left())
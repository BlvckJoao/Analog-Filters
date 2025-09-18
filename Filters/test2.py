import matplotlib.pyplot as plt
import numpy as np
import PySpice.Logging.Logging as Logging
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

logger = Logging.setup_logging()

# Criar circuito RC passa-baixa
circuit = Circuit("Filtro RC Passa-Baixa")

# Fonte AC (para sweep de frequência)
circuit.SinusoidalVoltageSource('input', 'in', circuit.gnd, amplitude=1@u_V)

# Componentes RC
R = 1@u_kΩ
C = 1@u_uF
circuit.R(1, 'in', 'out', R)
circuit.C(1, 'out', circuit.gnd, C)

# Simulação AC (resposta em frequência)
simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.ac(start_frequency=10@u_Hz,
                        stop_frequency=1@u_MHz,
                        number_of_points=100,
                        variation='dec')

# Plotar resposta
frequencies = np.array(analysis.frequency)
gain = 20 * np.log10(np.absolute(analysis.out))

plt.semilogx(frequencies, gain)
plt.title("Filtro RC Passa-Baixa")
plt.xlabel("Frequência [Hz]")
plt.ylabel("Ganho [dB]")
plt.grid(True, which="both", ls="--")
plt.show()

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

order = 2               # Ordem do filtro
filter_type = 'high'         # Tipo: 'low', 'high', 'bandpass', 'bandstop'

cutoff = 1000              

if isinstance(cutoff, list):
    Wn = [2*np.pi*f for f in cutoff]
else:
    Wn = 2*np.pi*cutoff

b, a = signal.butter(N=order, Wn=Wn, btype=filter_type, analog=True)

w, h = signal.freqs(b, a)
plt.figure(figsize=(8,4))
plt.semilogx(w/(2*np.pi), 20*np.log10(abs(h)))
plt.title(f'Resposta em frequência ({filter_type})')
plt.xlabel('Frequência [Hz]')
plt.ylabel('Magnitude [dB]')
plt.grid(True, which='both', ls='--')
plt.show()

t = np.linspace(0, 0.01, 1000)
x = np.sin(2*np.pi*500*t) + np.sin(2*np.pi*2000*t)  # 500 Hz + 2000 Hz

system = signal.lti(b, a)
t_out, y, _ = signal.lsim(system, U=x, T=t)

plt.figure(figsize=(10,4))
plt.plot(t, x, label='Sinal Original')
plt.plot(t_out, y, label='Sinal Filtrado', linewidth=2)
plt.xlabel('Tempo [s]')
plt.ylabel('Amplitude')
plt.title('Sinal antes e depois do filtro analógico')
plt.grid(True)
plt.legend()
plt.show()

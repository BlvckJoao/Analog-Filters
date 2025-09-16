import numpy as np
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm
from scipy.signal import TransferFunction, bode, step

# PARÂMETROS
R = 100.0       # ohms
L = 10e-3       # H (10 mH)
C = 1e-6        # F  (1 uF)

# ---------------------------
# Desenho do circuito
# ---------------------------
with schemdraw.Drawing(file='rlc_notch_diagram.svg') as d:
    d.config(unit=3)
    vin = d.add(elm.SourceSin().label('Vin', loc='left'))
    d.add(elm.Dot(open=True).label('Vout+', loc='left'))

    r = d.add(elm.Resistor().right().label('R'))
    d.add(elm.Dot(open=True).at(r.end).label('Vout-', loc='right'))

    # ramo paralelo L || C
    d.push()
    l = d.add(elm.Inductor().down().label('L'))
    d.add(elm.Capacitor().down().at(l.end).label('C'))
    d.pop()

print("Diagrama salvo em 'rlc_notch_diagram.svg'")

# ---------------------------
# Função de transferência (Notch)
# ---------------------------
w0 = 1.0 / np.sqrt(L * C)       # frequência central
Q  = np.sqrt(L/C) / R

num = [1.0, 0.0, w0**2]         # numerador
den = [1.0, w0/Q, w0**2]        # denominador
H = TransferFunction(num, den)

# frequências de corte aproximadas
wc1 = w0 * (np.sqrt(1 + 1/(2*Q**2)) - 1/(2*Q))
wc2 = w0 * (np.sqrt(1 + 1/(2*Q**2)) + 1/(2*Q))

print(f"ω0 = {w0:.4e} rad/s, ωc1 = {wc1:.4e} rad/s, ωc2 = {wc2:.4e} rad/s")

# ---------------------------
# Bode — Magnitude
# ---------------------------
n_points = 4000
w_log = np.logspace(np.log10(w0*1e-2), np.log10(w0*1e2), n_points)
w_bode, mag_db, phase_deg = bode(H, w=w_log)

mag_linear = 10**(mag_db / 20.0)
mag_norm = mag_linear / np.max(mag_linear)

plt.figure(figsize=(12,6))
plt.semilogx(w_bode, mag_norm, label='|H(jω)| normalizado', linewidth=2)

# linhas verticais
plt.axvline(wc1, color='g', linestyle='--', linewidth=1.5, label=rf'$\omega_{{c1}}$ = {wc1:.2e}')
plt.axvline(wc2, color='b', linestyle='--', linewidth=1.5, label=rf'$\omega_{{c2}}$ = {wc2:.2e}')
plt.axvline(w0,  color='r', linestyle='-',  linewidth=1.5, label=rf'$\omega_0$ = {w0:.2e}')

plt.title("Filtro Rejeita-Faixa RLC — Magnitude normalizada")
plt.xlabel("ω [rad/s]")
plt.ylabel("|H(jω)| (normalizado)")
plt.grid(which='both', linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()

# ---------------------------
# Bode — Fase
# ---------------------------
plt.figure(figsize=(12,6))
plt.semilogx(w_bode, phase_deg, label='∠H(jω)', linewidth=2)
plt.axvline(w0, color='r', linestyle='--', linewidth=1.2, label=rf'$\omega_0$ = {w0:.2e}')

plt.title("Filtro Rejeita-Faixa RLC — Fase")
plt.xlabel("ω [rad/s]")
plt.ylabel("Fase [graus]")
plt.grid(which='both', linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()

# ---------------------------
# Resposta ao degrau
# ---------------------------
t_step, y_step = step(H)

plt.figure(figsize=(12,6))
plt.plot(t_step, y_step, linewidth=1.6, label='Resposta ao degrau')
plt.title("Filtro Rejeita-Faixa RLC — Resposta ao Degrau")
plt.xlabel("Tempo [s]")
plt.ylabel("Amplitude [Vout/Vin]")
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()

# ---------------------------
# Resumo
# ---------------------------
print("Resumo:")
print(f"  R = {R} Ω, L = {L} H, C = {C} F")
print(f"  ω0 = {w0:.4e} rad/s")
print(f"  ωc1 = {wc1:.4e} rad/s")
print(f"  ωc2 = {wc2:.4e} rad/s")
print("Arquivos gerados: 'rlc_notch_diagram.svg' (diagrama).")

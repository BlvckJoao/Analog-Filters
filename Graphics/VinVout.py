import numpy as np
import matplotlib.pyplot as plt

# desenhar circuito é opcional — tentamos importar schemdraw, se não existir seguimos sem erro
try:
    import schemdraw
    import schemdraw.elements as elm
    schemdraw_available = True
except Exception as e:
    schemdraw_available = False
    schemdraw_err = e

from scipy.signal import lti, lsim, freqs

# PARÂMETROS
R = 1e5          # ohms
C = 5.3e-9      # F
wc = 1.0 / (R * C)   # frequência de corte (rad/s)

# -----------------------------
# Desenho do circuito (opcional)
# -----------------------------
if schemdraw_available:
    with schemdraw.Drawing() as d:
        d.config(unit=3)
        d.add(elm.SourceSin().label('Vin', loc='left'))
        c = d.add(elm.Capacitor().right().label('C'))
        d.add(elm.Dot(open=True).at(c.end).label('Vout+', loc='right'))
        r = d.add(elm.Resistor().down().label('R'))
        d.add(elm.Dot(open=True).at(r.end).label('Vout-', loc='right'))
        d.add(elm.Line().left())
        d.save('rc_highpass_diagram.svg')
    print("Diagrama salvo em 'rc_highpass_diagram.svg'")
else:
    print("schemdraw não disponível — pulei o desenho. Erro:", schemdraw_err)

# -----------------------------
# Função de transferência (analógica)
# H(s) = (R*C s) / (R*C s + 1)  => numerador [R*C, 0], denominador [R*C, 1]
# -----------------------------
num = [R * C, 0.0]
den = [R * C, 1.0]
sys = lti(num, den)   # forma compatível com lsim

print(f"ωc = {wc:.4e} rad/s")

# -----------------------------
# Análise de frequência (usando freqs — mais robusto para filtros analógicos)
# -----------------------------
n_points = 2000
w_log = np.logspace(np.log10(wc * 1e-2), np.log10(wc * 1e2), n_points)
w_bode, Hjw = freqs(num, den, w_log)   # H(jw) complexo
mag_db = 20 * np.log10(np.abs(Hjw))
phase_deg = np.angle(Hjw, deg=True)

# magnitude normalizada
mag_linear = np.abs(Hjw)
mag_norm = mag_linear / np.max(mag_linear)

# PLOT 1 — Magnitude normalizada
plt.figure(figsize=(12, 5))
plt.semilogx(w_bode, mag_norm, label='|H(jω)| normalizado', linewidth=2)
plt.axvline(wc, color='r', linestyle='--', linewidth=1.5, label=rf'$\omega_c$ = {wc:.2e}')
plt.title("Filtro RC Passa-Alta — Magnitude normalizada")
plt.xlabel("ω [rad/s]")
plt.ylabel("|H(jω)| (normalizado)")
plt.grid(which='both', linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()

# PLOT 2 — Fase
plt.figure(figsize=(12, 5))
plt.semilogx(w_bode, phase_deg, label='∠H(jω)', linewidth=2)
plt.axvline(wc, color='r', linestyle='--', linewidth=1.5, label=rf'$\omega_c$ = {wc:.2e}')
plt.title("Filtro RC Passa-Alta — Fase")
plt.xlabel("ω [rad/s]")
plt.ylabel("Fase [graus]")
plt.grid(which='both', linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()

# -----------------------------
# Simulação no tempo — sinal de entrada e saída
# -----------------------------
fs = 20000                      # taxa de amostragem para o sinal (Hz) — suficientemente alta
t = np.arange(0, 0.5, 1 / fs)   # 0.5 s de simulação
# sinal de entrada: soma de um senóide de baixa freq (5 Hz) + componente alta (200 Hz)
vin = np.sin(2 * np.pi * 5 * t) + 0.5 * np.sin(2 * np.pi * 200 * t)

# lsim(sys, U, T) — garante que len(U) == len(T)
t_out, vout, _ = lsim(sys, U=vin, T=t)

# PLOT 3 — Entrada vs Saída (zoom nos primeiros 50 ms para ver detalhes)
plt.figure(figsize=(12, 5))
plt.plot(t, vin, label='Vin(t)', alpha=0.7)
plt.plot(t_out, vout, label='Vout(t)', alpha=0.9)
plt.xlim(0, 0.05)
plt.title("Resposta temporal do filtro RC passa-alta (zoom: 0–50 ms)")
plt.xlabel("t [s]")
plt.ylabel("Amplitude")
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()

# -----------------------------
# Resumo
# -----------------------------
print("Resumo:")
print(f"  R = {R:.2e} Ω, C = {C:.2e} F")
print(f"  ωc = {wc:.4e} rad/s")
print("Arquivos gerados (se aplicável): 'rc_highpass_diagram.svg' (diagrama).")
import numpy as np
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm
from scipy.signal import TransferFunction, bode

def main(R_pb, C_pb):

    # PARÂMETROS
    R = R_pb       # ohms
    C = C_pb      # F
    wc = 1.0 / (R * C)   # frequência de corte rad/s

    # -----------------------------
    # Desenho do circuito
    # -----------------------------
    with schemdraw.Drawing(file='rc_highpass_diagram.svg') as d:
        d.config(unit=3)
        # Fonte senoidal
        vin = d.add(elm.SourceSin().label('Vin', loc='left'))
        # Capacitor em série
        r = d.add(elm.Resistor().right().label('C'))
        # Nó de saída +
        d.add(elm.Dot(open=True).at(r.end).label('Vout+', loc='right'))
        # Resistor para o terra
        c = d.add(elm.Capacitor().down().label('R'))
        d.add(elm.Dot(open=True).at(c.end).label('Vout-', loc='right'))
        d.add(elm.Line().left())

    print("Diagrama salvo em 'rc_lowpass_diagram.svg'")

    # -----------------------------
    # Função de transferência
    # -----------------------------
    num = [1.0]          # Numerador = 1
    den = [R*C, 1.0]     # Denominador = sRC + 1
    H = TransferFunction(num, den)

    print(f"ωc = {wc:.4e} rad/s")

    # -----------------------------
    # Análise de frequência (Bode)
    # -----------------------------
    n_points = 2000
    w_log = np.logspace(np.log10(wc*1e-2), np.log10(wc*1e2), n_points)
    w_bode, mag_db, phase_deg = bode(H, w=w_log)

    # Magnitude normalizada
    mag_linear = 10**(mag_db / 20.0)
    mag_norm = mag_linear / np.max(mag_linear)

    # PLOT 1 — Magnitude
    plt.figure(figsize=(12,6))
    plt.semilogx(w_bode, mag_norm, label='|H(jω)| normalizado', linewidth=2)

    # linha de corte
    plt.axvline(wc, color='r', linestyle='--', linewidth=1.5, label=rf'$\omega_c$ = {wc:.2e}')

    plt.title("Filtro RC Passa-Baixa — Magnitude normalizada")
    plt.xlabel("ω [rad/s]")
    plt.ylabel("|H(jω)| (normalizado)")
    plt.grid(which='both', linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # PLOT 2 — Fase
    plt.figure(figsize=(12,6))
    plt.semilogx(w_bode, phase_deg, label='∠H(jω)', linewidth=2)
    plt.axvline(wc, color='r', linestyle='--', linewidth=1.5, label=rf'$\omega_c$ = {wc:.2e}')

    plt.title("Filtro RC Passa-Baixa — Fase")
    plt.xlabel("ω [rad/s]")
    plt.ylabel("Fase [graus]")
    plt.grid(which='both', linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # -----------------------------
    # Resumo
    # -----------------------------
    print("Resumo:")
    print(f"  R = {R:.2e} Ω, C = {C:.2e} F")
    print(f"  ωc = {wc:.4e} rad/s")
    print("Arquivos gerados: 'rc_lowpass_diagram.svg' (diagrama).")
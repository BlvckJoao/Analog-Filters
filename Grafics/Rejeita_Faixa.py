import numpy as np
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm
from scipy.signal import TransferFunction, bode, step
from scipy.optimize import brentq

def main(R_rf, L_rf, C_rf):

    # PARÂMETROS
    R = R_rf       # ohms
    L = L_rf       # H (10 mH)
    C = C_rf        # F  (1 uF)

    # ---------------------------
    # Desenho do circuito
    # ---------------------------
    with schemdraw.Drawing(file='rlc_notch_diagram.svg') as d:
        d.config(unit=3)
        # Fonte senoidal
        vin = d.add(elm.SourceSin().label('Vin', loc='right')) #Talvez mudança aqui.
        # Resistor
        r = d.add(elm.Resistor().right().label('R'))
        # Nó de entrada
        d.add(elm.Dot(open=True).at(r.end).label('Vout+', loc='right'))
        # Indutor
        l = d.add(elm.Inductor().down().label('L'))
        # Capacitor
        c = d.add(elm.Capacitor().left().label('C'))
        #Nó de saída
        d.add(elm.Dot(open=True).at(c.end).label('Vout-', loc='left'))

    print("Diagrama salvo em 'rlc_notch_diagram.svg'")

    # -----------------------------------
    # FUNÇÃO DE TRANSFERÊNCIA
    # -----------------------------------
    w0 = 1.0 / np.sqrt(L * C)       # frequência central
    BW = R / L                      # largura de banda (rad/s)
    Q  = w0 / BW                    # fator de qualidade

    # Numerador e denominador normalizados
    num = [1.0, 0.0, w0**2]         # zeros em ±jω0
    den = [1.0, w0/Q, w0**2]        # pólos complexos conjugados
    H = TransferFunction(num, den)

    # -----------------------------------
    # CÁLCULO DAS FREQUÊNCIAS DE CORTE
    # -----------------------------------
    # |H(jw)| normalizado
    def H_abs(w):
        _, mag_db, _ = bode(H, w=[w])
        mag_lin = 10**(mag_db[0]/20.0)
        return mag_lin

    H_max = H_abs(1e-6)  # ganho em baixa frequência (≈ máximo)
    target = H_max/np.sqrt(2)  # ponto de -3 dB

    # Encontrar wc1 < w0 < wc2 resolvendo numericamente
    wc1 = brentq(lambda w: H_abs(w) - target, w0/10, w0) 
    wc2 = brentq(lambda w: H_abs(w) - target, w0, w0*10)

    # -----------------------------------
    # BODE — MAGNITUDE
    # -----------------------------------
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

    # adiciona Q e BW na legenda
    plt.plot([], [], ' ', label=rf'$Q$ = {Q:.2f}')
    plt.plot([], [], ' ', label=rf'$BW$ = {BW:.2e} rad/s')

    # linha para largura de banda
    y_pos = (1/np.sqrt(2))
    plt.hlines(y=y_pos, xmin=wc1, xmax=wc2, colors='purple', linestyles='-', linewidth=2)
    plt.text(np.sqrt(wc1*wc2), y_pos*1.05, 'BW', color='purple',
            ha='center', va='bottom', fontsize=12)

    plt.title("Filtro Rejeita-Faixa RLC — Magnitude normalizada")
    plt.xlabel("ω [rad/s]")
    plt.ylabel("|H(jω)| (normalizado)")
    plt.grid(which='both', linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # -----------------------------------
    # BODE — FASE
    # -----------------------------------
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

    # -----------------------------------
    # RESUMO
    # -----------------------------------
    print("\nResumo do filtro:")
    print(f"  R  = {R:.2f} Ω")
    print(f"  L  = {L:.2e} H")
    print(f"  C  = {C:.2e} F")
    print(f"  ω0 = {w0:.4e} rad/s")
    print(f"  BW = {BW:.4e} rad/s")
    print(f"  Q  = {Q:.4f}")
    print(f"  ωc1 = {wc1:.4e} rad/s")
    print(f"  ωc2 = {wc2:.4e} rad/s")
    print("Arquivos gerados: 'rlc_notch_diagram.svg'")
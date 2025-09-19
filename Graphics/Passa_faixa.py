import numpy as np
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm
from scipy.signal import TransferFunction, bode, impulse, step

def main(R_pf, L_pf, C_pf):

    # PARÂMETROS
    R = R_pf       # ohms
    L = L_pf       # H (10 mH)
    C = C_pf        # F  (1 uF)

    # Desenho do circuito (salva 'rlc_user_diagram.svg')
    with schemdraw.Drawing(file='rlc_user_diagram_fixed.svg') as d:
        d.config(unit=3)
        # Fonte senoidal
        vin = d.add(elm.SourceSin().label('Vin', loc='left')) #Talvez mudança aqui.
        #Nó de entrada
        d.add(elm.Dot(open=True).label('Vout+', loc='left'))
        # Resistor
        r = d.add(elm.Resistor().right().label('R'))
        # Nó de saída
        d.add(elm.Dot(open=True).at(r.end).label('Vout-', loc='right'))
        # Indutor
        l = d.add(elm.Inductor().down().label('L'))
        # Capacitor
        c = d.add(elm.Capacitor().left().label('C'))

    print("Diagrama salvo em 'rlc_user_diagram.svg'")

    # Função de transferência (saída no resistor R)
    num = [R / L, 0.0]                 # numerador
    den = [1.0, R / L, 1.0 / (L * C)]  # denominador
    H = TransferFunction(num, den)

    # Frequências características
    # ressonância central
    w0 = 1.0 / np.sqrt(L * C)

    # frequências de corte aproximadas (para o passa-faixa de 2ª ordem)
    # derivadas considerando os polos (conforme fórmulas usuais)
    wc1 = (R / (2.0 * L)) * (np.sqrt(1.0 + 4.0 * L / (R**2 * C)) - 1.0)
    wc2 = (R / (2.0 * L)) * (np.sqrt(1.0 + 4.0 * L / (R**2 * C)) + 1.0)

    print(f"ω0 = {w0:.4e} rad/s, ωc1 = {wc1:.4e} rad/s, ωc2 = {wc2:.4e} rad/s")

    # Vetores de frequência
    n_points = 4000
    # log-spaced (para Bode/plots log)
    w_min_log = max(1e-2, w0 * 1e-3)   # evita começar demasiado perto de 0
    w_max = w0 * 1e3
    w_log = np.logspace(np.log10(w_min_log), np.log10(w_max), n_points)

    # Bode (scipy retorna magnitude em dB e fase em graus)
    w_bode, mag_db, phase_deg = bode(H, w=w_log)

    # converter mag dB para mag linear e normalizar (máx = 1)
    mag_linear = 10**(mag_db / 20.0)
    mag_norm = mag_linear / np.max(mag_linear)

    # PLOT 1 — Magnitude normalizada (log)
    plt.figure(figsize=(12,6))
    plt.semilogx(w_bode, mag_norm, label='|H(jω)| normalizado', linewidth=2)

    # linhas verticais
    l1 = plt.axvline(wc1, color='g', linestyle='--', linewidth=1.5)
    l2 = plt.axvline(wc2, color='b', linestyle='--', linewidth=1.5)
    l3 = plt.axvline(w0,  color='r', linestyle='-',  linewidth=1.5)

    # largura de banda
    BW = wc2 - wc1
    Q = w0 / BW   # fator de qualidade

    # segmento roxo mostrando a banda
    y_bw = 0.707  # nível de -3 dB na curva normalizada
    plt.hlines(y_bw, wc1, wc2, colors='m', linewidth=2)

    # Glossário com cores correspondentes
    plt.title("Filtro Passa-Faixa RLC — Magnitude normalizada")

    l1.set_label(rf'$\omega_{{c1}}$ = {wc1:.2e} rad/s')
    l2.set_label(rf'$\omega_{{c2}}$ = {wc2:.2e} rad/s')
    l3.set_label(rf'$\omega_0$   = {w0:.2e} rad/s')

    # linhas invisíveis só para legenda
    plt.plot([], [], color='m', linestyle='-', linewidth=2, 
            label=rf'$BW$ = {BW:.2e} rad/s')
    plt.plot([], [], ' ', label=rf'$Q$ = {Q:.2f}')   # fator de qualidade

    plt.xlabel("ω [rad/s]")
    plt.ylabel("|H(jω)| (normalizado)")
    plt.xlim(w_min_log, w_max)
    plt.ylim(-0.05, 1.05)
    plt.grid(which='both', linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # PLOT 2 — Fase com assíntotas aproximadas
    plt.figure(figsize=(12,6))
    line_phase, = plt.semilogx(w_bode, phase_deg, label='∠H(jω) (real)', linewidth=2)

    # assíntotas horizontais (aproximações didáticas)
    a1 = plt.axhline(90,  color='gray', linestyle='--', linewidth=0.8, alpha=0.7)
    a2 = plt.axhline(0,   color='gray', linestyle='--', linewidth=0.8, alpha=0.7)
    a3 = plt.axhline(-90, color='gray', linestyle='--', linewidth=0.8, alpha=0.7)

    # linhas verticais de referência
    l1 = plt.axvline(wc1, color='g', linestyle='--', linewidth=1.2)
    l2 = plt.axvline(wc2, color='b', linestyle='--', linewidth=1.2)
    l3 = plt.axvline(w0,  color='r', linestyle='-',  linewidth=1.2)

    # Glossário
    plt.title("Filtro Passa-Faixa RLC — Fase (com assíntotas)")
    plt.xlabel("ω [rad/s]")
    plt.ylabel("Fase [graus]")
    plt.ylim(-120, 120)
    plt.xlim(w_min_log, w_max)
    plt.grid(which='both', linestyle='--', alpha=0.6)

    # valores iniciais e finais da fase
    fase_ini = - np.round(np.min(phase_deg), 1)  
    fase_fim = - np.round(np.max(phase_deg), 1)   

    # setando os labels diretamente nos objetos
    l1.set_label(rf'$\omega_{{c1}}$ = {wc1:.2e} rad/s')
    l2.set_label(rf'$\omega_{{c2}}$ = {wc2:.2e} rad/s')
    l3.set_label(rf'$\omega_0$   = {w0:.2e} rad/s')

    # handle invisível para valores de fase
    plt.plot([], [], ' ', label=rf'Fase inicial = {fase_ini:.1f}°')
    plt.plot([], [], ' ', label=rf'Fase final   = {fase_fim:.1f}°')

    plt.legend()
    plt.tight_layout()
    plt.show()

    # Resumo impresso para o usuário
    print("Resumo:")
    print(f"  R = {R} Ω, L = {L} H, C = {C} F")
    print(f"  ω0 = {w0:.4e} rad/s")
    print(f"  ωc1 = {wc1:.4e} rad/s")
    print(f"  ωc2 = {wc2:.4e} rad/s")
    print("Arquivos gerados: 'rlc_user_diagram.svg' (diagrama).")

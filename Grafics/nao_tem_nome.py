import tkinter as tk
from tkinter import ttk

# importa os arquivos
import Passa_baixa
import Passa_alta
import Passa_faixa
import Rejeita_Faixa

def rodar_filtro():
    tipo = combo_tipo.get()
    try:
        R = float(entry_R.get())
        C = float(entry_C.get())

        if tipo in ["Passa-Faixa", "Rejeita-Faixa"]:
            L = float(entry_L.get())

        if tipo == "Passa-Baixa":
            Passa_baixa.main(R, C)
        elif tipo == "Passa-Alta":
            Passa_alta.main(R, C)
        elif tipo == "Passa-Faixa":
            Passa_faixa.main(R, L, C)
        elif tipo == "Rejeita-Faixa":
            Rejeita_Faixa.main(R, L, C)
    except ValueError:
        print("Erro: Digite valores numéricos válidos.")

def atualizar_campos(event):
    tipo = combo_tipo.get()
    if tipo in ["Passa-Faixa", "Rejeita-Faixa"]:
        label_L.grid(row=2, column=0, sticky="w")
        entry_L.grid(row=2, column=1)
    else:
        label_L.grid_remove()
        entry_L.grid_remove()

# --- Interface Tkinter ---
root = tk.Tk()
root.title("Simulador de Filtros RLC/RC")

tk.Label(root, text="Tipo de filtro:").grid(row=0, column=0, sticky="w")
combo_tipo = ttk.Combobox(root, values=["Passa-Baixa", "Passa-Alta", "Passa-Faixa", "Rejeita-Faixa"])
combo_tipo.grid(row=0, column=1)
combo_tipo.bind("<<ComboboxSelected>>", atualizar_campos)

tk.Label(root, text="R [Ω]:").grid(row=1, column=0, sticky="w")
entry_R = tk.Entry(root)
entry_R.insert(0, "100")
entry_R.grid(row=1, column=1)

label_L = tk.Label(root, text="L [H]:")
entry_L = tk.Entry(root)
entry_L.insert(0, "1e-3")
label_L.grid_remove()
entry_L.grid_remove()

tk.Label(root, text="C [F]:").grid(row=3, column=0, sticky="w")
entry_C = tk.Entry(root)
entry_C.insert(0, "1e-6")
entry_C.grid(row=3, column=1)

btn = tk.Button(root, text="Rodar", command=rodar_filtro)
btn.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()

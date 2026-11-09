"""
Simulador de Escenarios HMM y Analisis Estadistico Q1
Genera datos, metricas con intervalos de confianza del 95%, tablas y graficas de 300 DPI.
Autor: Wilfran Camilo Valencia Goez
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from typing import Dict, List
from hmm_model import HiddenMarkovModel

# Directorio de resultados
RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# -------------------------------------------------------------------------
# DEFINICION DEL CASO INDUSTRIAL:
# Monitoreo y Diagnostico de Estado de Salud en Rodamientos Industriales
# Estados Ocultos:
#   S_0: Operacion Normal / Sano
#   S_1: Degradacion Incipiente / Falla Leve
#   S_2: Falla Severa / Critica
# Observaciones Visibles (Cuantizacion de senales de vibracion y temperatura):
#   V_0: Vibracion Baja (Nivel normal)
#   V_1: Vibracion Media (Alertas de desbalance)
#   V_2: Vibracion Alta / Picos de aceleracion y temperatura
# -------------------------------------------------------------------------

STATES = ["Sano (S0)", "Degradacion (S1)", "Falla Severa (S2)"]
OBSERVATIONS = ["Vibracion Baja (V0)", "Vibracion Media (V1)", "Vibracion Alta (V2)"]

def get_scenarios():
    """
    Define 3 escenarios operacionales contrastados para evaluar la dinamica del sistema:
      - Escenario 1: Operacion Nominal con Mantenimiento Preventivo (Alta permanencia en S0)
      - Escenario 2: Operacion Severa con Sobrecarga Mecanica (Rapida transicion a falla S1 y S2)
      - Escenario 3: Sensores Ruidosos / Incertidumbre de Medicion (Emision con alta entropia)
    """
    pi_default = np.array([0.85, 0.12, 0.03])
    
    # Escenario 1: Operacion Nominal
    A_1 = np.array([
        [0.92, 0.07, 0.01],
        [0.05, 0.85, 0.10],
        [0.02, 0.08, 0.90]
    ])
    B_1 = np.array([
        [0.80, 0.16, 0.04],
        [0.12, 0.73, 0.15],
        [0.02, 0.18, 0.80]
    ])
    
    # Escenario 2: Operacion Severa (Sobrecarga)
    A_2 = np.array([
        [0.70, 0.24, 0.06],
        [0.03, 0.65, 0.32],
        [0.01, 0.04, 0.95]
    ])
    B_2 = np.array([
        [0.78, 0.17, 0.05],
        [0.10, 0.70, 0.20],
        [0.02, 0.13, 0.85]
    ])
    
    # Escenario 3: Incertidumbre / Sensores con Ruido (Alta confusion en B)
    A_3 = np.array([
        [0.88, 0.10, 0.02],
        [0.04, 0.82, 0.14],
        [0.01, 0.09, 0.90]
    ])
    B_3 = np.array([
        [0.48, 0.32, 0.20],
        [0.25, 0.50, 0.25],
        [0.15, 0.35, 0.50]
    ])
    
    scenarios = {
        "Escenario 1: Operacion Nominal": HiddenMarkovModel(STATES, OBSERVATIONS, A_1, B_1, pi_default),
        "Escenario 2: Operacion Severa":  HiddenMarkovModel(STATES, OBSERVATIONS, A_2, B_2, pi_default),
        "Escenario 3: Sensores con Ruido": HiddenMarkovModel(STATES, OBSERVATIONS, A_3, B_3, pi_default),
    }
    return scenarios

def run_monte_carlo_experiments(num_replications: int = 200, T: int = 150, base_seed: int = 42):
    """
    Ejecuta simulaciones Monte Carlo para cada escenario garantizando reproducibilidad:
      - num_replications: numero de trayectorias independientes
      - T: horizonte temporal de cada trayectoria (instantes de medicion)
      - base_seed: semilla inicial
    """
    scenarios = get_scenarios()
    metrics_summary = []
    raw_data_records = []
    
    sample_trajectory = {}

    for sc_name, model in scenarios.items():
        accuracies = []
        prop_healthy = []
        prop_degraded = []
        prop_failed = []
        time_to_first_failure = []
        
        for rep in range(num_replications):
            seed = base_seed + rep * 17
            true_states, obs = model.simulate(T=T, seed=seed)
            decoded_states, _ = model.viterbi(obs)
            
            acc = model.compute_accuracy(true_states, decoded_states)
            accuracies.append(acc)
            
            p_s0 = np.mean(true_states == 0)
            p_s1 = np.mean(true_states == 1)
            p_s2 = np.mean(true_states == 2)
            
            prop_healthy.append(p_s0)
            prop_degraded.append(p_s1)
            prop_failed.append(p_s2)
            
            # Tiempo hasta primera transicion a estado de Falla Severa (S2)
            idx_fail = np.where(true_states == 2)[0]
            ttff = idx_fail[0] if len(idx_fail) > 0 else T
            time_to_first_failure.append(ttff)
            
            # Guardar datos crudos para exportacion
            raw_data_records.append({
                "Escenario": sc_name,
                "Replicacion": rep + 1,
                "Exactitud_Viterbi": acc,
                "Prop_Sano_S0": p_s0,
                "Prop_Degradacion_S1": p_s1,
                "Prop_Falla_S2": p_s2,
                "Tiempo_Primera_Falla": ttff
            })
            
            # Guardar la primera trayectoria como ejemplo demostrativo
            if rep == 0:
                sample_trajectory[sc_name] = {
                    "true_states": true_states,
                    "obs": obs,
                    "decoded_states": decoded_states
                }

        # Calculo de estadisticos rigurosos e Intervalos de Confianza (95%)
        # IC = mean +/- 1.96 * (std / sqrt(N))
        n = num_replications
        z_crit = 1.96
        
        def compute_stats(arr):
            mean = float(np.mean(arr))
            std = float(np.std(arr, ddof=1))
            se = std / np.sqrt(n)
            ci_low = mean - z_crit * se
            ci_high = mean + z_crit * se
            return {
                "mean": mean,
                "std": std,
                "min": float(np.min(arr)),
                "max": float(np.max(arr)),
                "ci_95": f"[{ci_low:.4f}, {ci_high:.4f}]",
                "ci_low": ci_low,
                "ci_high": ci_high
            }

        stats_acc = compute_stats(accuracies)
        stats_s0 = compute_stats(prop_healthy)
        stats_s1 = compute_stats(prop_degraded)
        stats_s2 = compute_stats(prop_failed)
        stats_ttff = compute_stats(time_to_first_failure)
        
        metrics_summary.append({
            "Escenario": sc_name,
            "Exactitud_Media": stats_acc["mean"],
            "Exactitud_Std": stats_acc["std"],
            "Exactitud_IC95": stats_acc["ci_95"],
            "Prop_Sano_Media": stats_s0["mean"],
            "Prop_Degradacion_Media": stats_s1["mean"],
            "Prop_Falla_Media": stats_s2["mean"],
            "Tiempo_Falla_Medio": stats_ttff["mean"],
            "Tiempo_Falla_Std": stats_ttff["std"],
            "Tiempo_Falla_IC95": stats_ttff["ci_95"]
        })
        
    df_metrics = pd.DataFrame(metrics_summary)
    df_raw = pd.DataFrame(raw_data_records)
    
    return df_metrics, df_raw, sample_trajectory

def generate_scientific_plots(scenarios, sample_trajectory, df_raw):
    """Genera figuras en formato de revista indexada (300 DPI, tipografias sobrias)."""
    plt.rcParams.update({
        'font.family': 'serif',
        'font.size': 10,
        'axes.labelsize': 11,
        'axes.titlesize': 11,
        'xtick.labelsize': 9,
        'ytick.labelsize': 9,
        'legend.fontsize': 9,
        'figure.titlesize': 12
    })
    
    # -------------------------------------------------------------
    # FIGURA 1: Matrices A y B para los tres escenarios (Heatmaps)
    # -------------------------------------------------------------
    fig, axes = plt.subplots(2, 3, figsize=(13, 7))
    cmap_A = 'Blues'
    cmap_B = 'Greens'
    
    sc_keys = list(scenarios.keys())
    for col, sc_key in enumerate(sc_keys):
        model = scenarios[sc_key]
        
        # Matriz A
        imA = axes[0, col].imshow(model.A, cmap=cmap_A, vmin=0, vmax=1)
        axes[0, col].set_title(f"{sc_key.split(':')[0]}\nMatriz Transicion A")
        axes[0, col].set_xticks(range(3))
        axes[0, col].set_yticks(range(3))
        axes[0, col].set_xticklabels(['S0', 'S1', 'S2'])
        axes[0, col].set_yticklabels(['S0', 'S1', 'S2'])
        for i in range(3):
            for j in range(3):
                val = model.A[i, j]
                axes[0, col].text(j, i, f"{val:.2f}", ha='center', va='center', 
                                  color='white' if val > 0.5 else 'black')
        
        # Matriz B
        imB = axes[1, col].imshow(model.B, cmap=cmap_B, vmin=0, vmax=1)
        axes[1, col].set_title(f"Matriz Emision B")
        axes[1, col].set_xticks(range(3))
        axes[1, col].set_yticks(range(3))
        axes[1, col].set_xticklabels(['V0', 'V1', 'V2'])
        axes[1, col].set_yticklabels(['S0', 'S1', 'S2'])
        for i in range(3):
            for j in range(3):
                val = model.B[i, j]
                axes[1, col].text(j, i, f"{val:.2f}", ha='center', va='center', 
                                  color='white' if val > 0.5 else 'black')
                                  
    axes[0, 0].set_ylabel("Estado Origen")
    axes[1, 0].set_ylabel("Estado Oculto")
    fig.tight_layout()
    fig1_path = os.path.join(RESULTS_DIR, "figura1_matrices_hmm.png")
    fig.savefig(fig1_path, dpi=300)
    plt.close(fig)

    # -------------------------------------------------------------
    # FIGURA 2: Decodificacion Viterbi vs Estado Oculto Real
    # -------------------------------------------------------------
    fig, axes = plt.subplots(3, 1, figsize=(11, 7), sharex=True)
    t_range = np.arange(80) # Primeros 80 instantes
    
    for idx, sc_key in enumerate(sc_keys):
        traj = sample_trajectory[sc_key]
        true_s = traj["true_states"][:80]
        dec_s = traj["decoded_states"][:80]
        
        ax = axes[idx]
        ax.step(t_range, true_s, label='Estado Oculto Real', color='#1f77b4', linewidth=1.8, where='mid')
        ax.plot(t_range, dec_s, 'o--', label='Decodificacion Viterbi', color='#d62728', markersize=3.5, alpha=0.8)
        ax.set_yticks([0, 1, 2])
        ax.set_yticklabels(['S0 (Sano)', 'S1 (Alerta)', 'S2 (Falla)'])
        ax.set_title(f"{sc_key} (Trayectoria T=1 a 80)")
        ax.grid(True, linestyle=':', alpha=0.6)
        if idx == 0:
            ax.legend(loc='upper right', framealpha=0.9)
            
    axes[-1].set_xlabel("Paso Temporal de Muestreo (t)")
    fig.tight_layout()
    fig2_path = os.path.join(RESULTS_DIR, "figura2_viterbi_trayectorias.png")
    fig.savefig(fig2_path, dpi=300)
    plt.close(fig)

    # -------------------------------------------------------------
    # FIGURA 3: Distribucion de Exactitud de Viterbi y Tiempo a Falla
    # -------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    
    # Exactitud boxplot
    data_acc = [df_raw[df_raw["Escenario"] == k]["Exactitud_Viterbi"].values for k in sc_keys]
    bp1 = axes[0].boxplot(data_acc, patch_artist=True, labels=['Escenario 1', 'Escenario 2', 'Escenario 3'])
    axes[0].set_title("Exactitud de Decodificacion (Viterbi)")
    axes[0].set_ylabel("Exactitud (Proporcion)")
    axes[0].grid(True, linestyle=':', alpha=0.6)
    colors = ['#aec7e8', '#ffbb78', '#98df8a']
    for patch, c in zip(bp1['boxes'], colors):
        patch.set_facecolor(c)
        
    # Tiempo a primera falla
    data_ttff = [df_raw[df_raw["Escenario"] == k]["Tiempo_Primera_Falla"].values for k in sc_keys]
    bp2 = axes[1].boxplot(data_ttff, patch_artist=True, labels=['Escenario 1', 'Escenario 2', 'Escenario 3'])
    axes[1].set_title("Tiempo hasta Primera Falla Severa (TTFF)")
    axes[1].set_ylabel("Paso Temporal (t)")
    axes[1].grid(True, linestyle=':', alpha=0.6)
    for patch, c in zip(bp2['boxes'], colors):
        patch.set_facecolor(c)

    fig.tight_layout()
    fig3_path = os.path.join(RESULTS_DIR, "figura3_metricas_boxplot.png")
    fig.savefig(fig3_path, dpi=300)
    plt.close(fig)
    
    return [fig1_path, fig2_path, fig3_path]

def export_results_to_excel(df_metrics: pd.DataFrame, df_raw: pd.DataFrame, filepath: str):
    """Guarda tablas y datos de simulacion en un archivo Excel formal."""
    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        df_metrics.to_excel(writer, sheet_name="Resumen_Estadistico", index=False)
        df_raw.to_excel(writer, sheet_name="Datos_Monte_Carlo_Crudos", index=False)

if __name__ == "__main__":
    print("Iniciando simulacion Monte Carlo para modelo HMM...")
    scenarios = get_scenarios()
    df_metrics, df_raw, sample_trajectory = run_monte_carlo_experiments(num_replications=200, T=150, base_seed=42)
    
    excel_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resultados_hmm_escenarios.xlsx")
    export_results_to_excel(df_metrics, df_raw, excel_path)
    print(f"Datos exportados a: {excel_path}")
    
    plots = generate_scientific_plots(scenarios, sample_trajectory, df_raw)
    for p in plots:
        print(f"Grafica guardada en: {p}")
        
    print("\nResumen de Metricas Estadisticas:")
    print(df_metrics.to_string())


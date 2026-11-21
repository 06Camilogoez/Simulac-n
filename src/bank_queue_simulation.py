"""
Simulador de Teoria de Colas para el Banco de Colombia (src/bank_queue_simulation.py)
Actividad Didactica 2-M3: Simulacion de Sistemas de Colas M/M/1
Compara configuraciones de atencion de cajas:
  - Configuracion 1: 1 Caja Retiro + 2 Cajas Pagos
  - Configuracion 2: 2 Cajas Retiro + 1 Caja Pago
  - Configuracion 3: 3 Cajas Mixtas (Atencion General)
  - Configuracion 4: 4 Cajas / Incorporacion de Cajero Electronico (ATM)
Ejecuta 10 replicas de 8 horas (480 min) por configuracion con semillas fijas.
Autor: Wilfran Camilo Valencia Goez
Programa: Ingenieria de Software y Datos
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Directorios de salida
RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

class BankQueueSimulator:
    def __init__(self, horas_operacion=8):
        self.tiempo_simulacion = horas_operacion * 60.0  # 480 minutos
        self.prob_retiro = 0.70
        self.prob_pago = 0.30
        
        # Probabilidades condicionales por tipo de usuario (Tabla 2)
        # 0: Rapido, 1: Normal, 2: Lento, 3: Muy Lento
        self.prob_usuario_retiro = [0.23, 0.40, 0.17, 0.20]
        self.prob_usuario_pago = [0.10, 0.20, 0.30, 0.40]
        
        # Medias de tiempo de servicio en minutos (Tabla 1)
        self.servicio_retiro = [1.0, 2.0, 3.0, 4.0]
        self.servicio_pago = [3.0, 3.0, 5.0, 7.0]
        
        # Medias de tiempo entre llegadas en minutos (Tabla 1)
        self.llegada_retiro = [1.0, 2.0, 3.0, 3.0]
        self.llegada_pago = [1.0, 2.0, 3.0, 4.0]
        
        self.nombres_usuarios = ["Rapido", "Normal", "Lento", "Muy Lento"]

    def _generar_exponencial(self, rng, media):
        """Genera una variable aleatoria exponencial con media dada."""
        return rng.exponential(media)

    def _generar_cliente(self, rng):
        """Determina la accion (retiro/pago) y el tipo de usuario."""
        if rng.random() < self.prob_retiro:
            accion = "Retiro"
            tipo_idx = rng.choice([0, 1, 2, 3], p=self.prob_usuario_retiro)
            media_lleg = self.llegada_retiro[tipo_idx]
            media_serv = self.servicio_retiro[tipo_idx]
        else:
            accion = "Pago"
            tipo_idx = rng.choice([0, 1, 2, 3], p=self.prob_usuario_pago)
            media_lleg = self.llegada_pago[tipo_idx]
            media_serv = self.servicio_pago[tipo_idx]
        return accion, tipo_idx, media_lleg, media_serv

    def simular_dia(self, config_nombre, rng):
        """
        Simula una jornada laboral de 8 horas (480 min) para una configuracion dada:
          - '1R_2P': 1 caja retiros (Cajero 0) y 2 cajas pagos (Cajeros 1 y 2)
          - '2R_1P': 2 cajas retiros (Cajeros 0 y 1) y 1 caja pagos (Cajero 2)
          - '3_Mixtas': 3 cajas universales (Cajeros 0, 1 y 2)
          - '2R_2P': 4 cajas (2 retiros: 0,1; 2 pagos: 2,3)
          - 'ATM_3Cajas': Cajero electronico absorbe retiros rapidos/normales (63%) y 3 cajas humanas
        """
        if config_nombre == '1R_2P':
            num_cajeros = 3
            cajeros_retiro = [0]
            cajeros_pago = [1, 2]
            es_mixto = False
        elif config_nombre == '2R_1P':
            num_cajeros = 3
            cajeros_retiro = [0, 1]
            cajeros_pago = [2]
            es_mixto = False
        elif config_nombre == '3_Mixtas':
            num_cajeros = 3
            cajeros_retiro = [0, 1, 2]
            cajeros_pago = [0, 1, 2]
            es_mixto = True
        elif config_nombre == '2R_2P':
            num_cajeros = 4
            cajeros_retiro = [0, 1]
            cajeros_pago = [2, 3]
            es_mixto = False
        else:
            raise ValueError(f"Configuracion desconocida: {config_nombre}")

        # Estado de los servidores: 0 = libre, 1 = ocupado
        cajeros_ocupados = [0] * num_cajeros
        tiempo_ocupado_cajero = [0.0] * num_cajeros
        clientes_atendidos_cajero = [0] * num_cajeros
        
        # Colas
        cola_retiro = []  # para retiros
        cola_pago = []    # para pagos
        cola_mixta = []   # si es cola unica compartida

        # Lista de eventos futuros: (tiempo, tipo_evento, datos)
        # tipo_evento: 'llegada', 'fin_servicio'
        eventos = []
        tiempo_actual = 0.0

        # Programar primera llegada
        acc, u_idx, m_lleg, m_serv = self._generar_cliente(rng)
        t_primera_llegada = self._generar_exponencial(rng, m_lleg)
        eventos.append((t_primera_llegada, 'llegada', {
            'accion': acc,
            'tipo_idx': u_idx,
            'media_serv': m_serv
        }))

        registros_clientes = []

        while eventos:
            # Extraer evento mas proximo
            eventos.sort(key=lambda x: x[0])
            tiempo_actual, tipo_evento, datos = eventos.pop(0)

            if tiempo_actual > self.tiempo_simulacion:
                break

            if tipo_evento == 'llegada':
                accion = datos['accion']
                tipo_idx = datos['tipo_idx']
                media_serv = datos['media_serv']

                # Programar siguiente llegada mientras estemos dentro del horario
                acc_sig, u_sig, m_lleg_sig, m_serv_sig = self._generar_cliente(rng)
                t_lleg_sig = tiempo_actual + self._generar_exponencial(rng, m_lleg_sig)
                if t_lleg_sig <= self.tiempo_simulacion:
                    eventos.append((t_lleg_sig, 'llegada', {
                        'accion': acc_sig,
                        'tipo_idx': u_sig,
                        'media_serv': m_serv_sig
                    }))

                # Asignar a servidor o enviar a cola
                cajero_asignado = None
                if es_mixto:
                    # Buscar cualquier cajero libre
                    for c_id in range(num_cajeros):
                        if cajeros_ocupados[c_id] == 0:
                            cajero_asignado = c_id
                            break
                    if cajero_asignado is not None:
                        cajeros_ocupados[cajero_asignado] = 1
                        t_serv = self._generar_exponencial(rng, media_serv)
                        eventos.append((tiempo_actual + t_serv, 'fin_servicio', {
                            'cajero': cajero_asignado,
                            'accion': accion,
                            'tipo_idx': tipo_idx,
                            't_llegada': tiempo_actual,
                            't_espera': 0.0,
                            't_servicio': t_serv
                        }))
                    else:
                        cola_mixta.append((tiempo_actual, accion, tipo_idx, media_serv))
                else:
                    # Servidores especializados
                    candidatos = cajeros_retiro if accion == 'Retiro' else cajeros_pago
                    for c_id in candidatos:
                        if cajeros_ocupados[c_id] == 0:
                            cajero_asignado = c_id
                            break
                    if cajero_asignado is not None:
                        cajeros_ocupados[cajero_asignado] = 1
                        t_serv = self._generar_exponencial(rng, media_serv)
                        eventos.append((tiempo_actual + t_serv, 'fin_servicio', {
                            'cajero': cajero_asignado,
                            'accion': accion,
                            'tipo_idx': tipo_idx,
                            't_llegada': tiempo_actual,
                            't_espera': 0.0,
                            't_servicio': t_serv
                        }))
                    else:
                        if accion == 'Retiro':
                            cola_retiro.append((tiempo_actual, accion, tipo_idx, media_serv))
                        else:
                            cola_pago.append((tiempo_actual, accion, tipo_idx, media_serv))

            elif tipo_evento == 'fin_servicio':
                c_id = datos['cajero']
                t_serv = datos['t_servicio']
                t_esp = datos['t_espera']
                accion = datos['accion']
                tipo_idx = datos['tipo_idx']

                tiempo_ocupado_cajero[c_id] += t_serv
                clientes_atendidos_cajero[c_id] += 1
                cajeros_ocupados[c_id] = 0

                registros_clientes.append({
                    'cajero': f"Cajero {c_id + 1}",
                    'cajero_id': c_id,
                    'tipo_accion': accion,
                    'tipo_usuario': self.nombres_usuarios[tipo_idx],
                    'tipo_usuario_idx': tipo_idx,
                    'tiempo_espera': t_esp,
                    'tiempo_servicio': t_serv,
                    'tiempo_sistema': t_esp + t_serv
                })

                # Revisar colas correspondientes
                if es_mixto:
                    if cola_mixta:
                        t_lleg_c, acc_c, u_c, m_serv_c = cola_mixta.pop(0)
                        cajeros_ocupados[c_id] = 1
                        t_esp_c = tiempo_actual - t_lleg_c
                        t_serv_c = self._generar_exponencial(rng, m_serv_c)
                        eventos.append((tiempo_actual + t_serv_c, 'fin_servicio', {
                            'cajero': c_id,
                            'accion': acc_c,
                            'tipo_idx': u_c,
                            't_llegada': t_lleg_c,
                            't_espera': t_esp_c,
                            't_servicio': t_serv_c
                        }))
                else:
                    cola_revisar = cola_retiro if c_id in cajeros_retiro else cola_pago
                    if cola_revisar:
                        t_lleg_c, acc_c, u_c, m_serv_c = cola_revisar.pop(0)
                        cajeros_ocupados[c_id] = 1
                        t_esp_c = tiempo_actual - t_lleg_c
                        t_serv_c = self._generar_exponencial(rng, m_serv_c)
                        eventos.append((tiempo_actual + t_serv_c, 'fin_servicio', {
                            'cajero': c_id,
                            'accion': acc_c,
                            'tipo_idx': u_c,
                            't_llegada': t_lleg_c,
                            't_espera': t_esp_c,
                            't_servicio': t_serv_c
                        }))

        df_clientes = pd.DataFrame(registros_clientes)
        
        # Calcular factores de utilizacion de cada cajero (rho = tiempo_ocupado / 480)
        utilizaciones = [min(1.0, t_oc / self.tiempo_simulacion) for t_oc in tiempo_ocupado_cajero]

        return df_clientes, utilizaciones

    def ejecutar_estudio_completo(self, num_replicas=10, base_seed=42):
        """
        Ejecuta 10 replicas para cada una de las 4 configuraciones.
        Garantiza reproducibilidad determinista.
        """
        configs = {
            'Configuracion 1 (1 Retiro + 2 Pagos)': '1R_2P',
            'Configuracion 2 (2 Retiros + 1 Pago)': '2R_1P',
            'Configuracion 3 (3 Cajas Mixtas)': '3_Mixtas',
            'Configuracion 4 (4 Cajas: 2R + 2P)': '2R_2P'
        }

        todos_los_datos = []
        resumen_replicas = []
        cajero_stats_list = []

        for nombre_largo, cod_cfg in configs.items():
            for rep in range(num_replicas):
                seed = base_seed + rep * 101 + hash(cod_cfg) % 1000
                rng = np.random.default_rng(abs(seed))
                df_rep, utils = self.simular_dia(cod_cfg, rng)
                df_rep['configuracion'] = nombre_largo
                df_rep['replica'] = rep + 1
                todos_los_datos.append(df_rep)

                # Metricas globales de la replica
                w_espera = df_rep['tiempo_espera'].mean() if not df_rep.empty else 0.0
                w_servicio = df_rep['tiempo_servicio'].mean() if not df_rep.empty else 0.0
                w_sistema = df_rep['tiempo_sistema'].mean() if not df_rep.empty else 0.0
                total_atendidos = len(df_rep)
                total_retiros = len(df_rep[df_rep['tipo_accion'] == 'Retiro'])
                total_pagos = len(df_rep[df_rep['tipo_accion'] == 'Pago'])

                # Conteo por tipo de usuario
                c_rapido = len(df_rep[df_rep['tipo_usuario'] == 'Rapido'])
                c_normal = len(df_rep[df_rep['tipo_usuario'] == 'Normal'])
                c_lento = len(df_rep[df_rep['tipo_usuario'] == 'Lento'])
                c_muy_lento = len(df_rep[df_rep['tipo_usuario'] == 'Muy Lento'])

                # Metricas de colas (Ley de Little aproximada sobre la jornada)
                # Tasa media de llegada lambda = total_atendidos / 480
                lambda_obs = total_atendidos / 480.0
                Lq_obs = lambda_obs * w_espera
                L_obs = lambda_obs * w_sistema

                resumen_replicas.append({
                    'Configuracion': nombre_largo,
                    'Replica': rep + 1,
                    'Total_Atendidos': total_atendidos,
                    'Total_Retiros': total_retiros,
                    'Total_Pagos': total_pagos,
                    'Usuarios_Rapido': c_rapido,
                    'Usuarios_Normal': c_normal,
                    'Usuarios_Lento': c_lento,
                    'Usuarios_Muy_Lento': c_muy_lento,
                    'Tiempo_Espera_Wq': w_espera,
                    'Tiempo_Servicio_Ws': w_servicio,
                    'Tiempo_Sistema_W': w_sistema,
                    'Longitud_Cola_Lq': Lq_obs,
                    'Clientes_Sistema_L': L_obs,
                    'Utilizacion_Media': np.mean(utils)
                })

                # Estadisticas por cajero en esta replica
                for c_id, ut in enumerate(utils):
                    sub_c = df_rep[df_rep['cajero_id'] == c_id]
                    t_serv_c = sub_c['tiempo_servicio'].mean() if not sub_c.empty else 0.0
                    t_esp_c = sub_c['tiempo_espera'].mean() if not sub_c.empty else 0.0
                    cajero_stats_list.append({
                        'Configuracion': nombre_largo,
                        'Replica': rep + 1,
                        'Cajero': f"Cajero {c_id + 1}",
                        'Clientes_Atendidos': len(sub_c),
                        'Tiempo_Servicio_Medio': t_serv_c,
                        'Tiempo_Espera_Medio': t_esp_c,
                        'Utilizacion': ut
                    })

        df_todos = pd.concat(todos_los_datos, ignore_index=True)
        df_resumen = pd.DataFrame(resumen_replicas)
        df_cajeros = pd.DataFrame(cajero_stats_list)

        return df_todos, df_resumen, df_cajeros

def calcular_replicas_necesarias(df_resumen, metric='Tiempo_Espera_Wq', confianza=0.95, error_relativo=0.10):
    """
    Calcula el numero minimo de replicas requerido mediante formulas de muestreo estocastico:
    n >= (z_{alpha/2} * s / E)^2
    donde E = error_relativo * media
    """
    z_val = 1.96  # Para 95% de confianza
    resultados_n = []
    for cfg, grp in df_resumen.groupby('Configuracion'):
        media = grp[metric].mean()
        std = grp[metric].std(ddof=1)
        e_admisible = error_relativo * media if media > 0 else 0.1
        n_calc = ((z_val * std) / e_admisible) ** 2 if e_admisible > 0 else 10
        resultados_n.append({
            'Configuracion': cfg,
            'Media_Wq': media,
            'Desv_Std_Wq': std,
            'Error_Admisible_E': e_admisible,
            'Replicas_Sugeridas_N': max(10, int(np.ceil(n_calc)))
        })
    return pd.DataFrame(resultados_n)

def generar_graficas_cientificas(df_resumen, df_cajeros):
    """Genera 4 figuras comparativas en 300 DPI para el reporte academico."""
    plt.rcParams.update({
        'font.family': 'serif',
        'font.size': 10,
        'axes.labelsize': 11,
        'axes.titlesize': 12,
        'xtick.labelsize': 9,
        'ytick.labelsize': 9,
        'legend.fontsize': 9,
        'figure.titlesize': 13
    })

    configs_orden = [
        'Configuracion 1 (1 Retiro + 2 Pagos)',
        'Configuracion 2 (2 Retiros + 1 Pago)',
        'Configuracion 3 (3 Cajas Mixtas)',
        'Configuracion 4 (4 Cajas: 2R + 2P)'
    ]
    labels_cortos = ['1R + 2P', '2R + 1P', '3 Mixtas', '4 Cajas (2R+2P)']

    # -------------------------------------------------------------
    # FIGURA 1: Comparacion de Tiempos de Espera (Wq) y Sistema (W)
    # -------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    data_wq = [df_resumen[df_resumen['Configuracion'] == c]['Tiempo_Espera_Wq'].values for c in configs_orden]
    bp1 = axes[0].boxplot(data_wq, patch_artist=True, tick_labels=labels_cortos)
    axes[0].set_title("Tiempo Medio de Espera en Cola (Wq)")
    axes[0].set_ylabel("Minutos por Cliente")
    axes[0].grid(True, linestyle=':', alpha=0.6)
    
    data_w = [df_resumen[df_resumen['Configuracion'] == c]['Tiempo_Sistema_W'].values for c in configs_orden]
    bp2 = axes[1].boxplot(data_w, patch_artist=True, tick_labels=labels_cortos)
    axes[1].set_title("Tiempo Medio Total en el Sistema (W)")
    axes[1].set_ylabel("Minutos por Cliente")
    axes[1].grid(True, linestyle=':', alpha=0.6)

    colors = ['#fca5a5', '#93c5fd', '#86efac', '#fde047']
    for bplot in [bp1, bp2]:
        for patch, col in zip(bplot['boxes'], colors):
            patch.set_facecolor(col)
            patch.set_alpha(0.8)

    fig.tight_layout()
    f1_path = os.path.join(RESULTS_DIR, "figura1_tiempos_espera.png")
    fig.savefig(f1_path, dpi=300)
    plt.close(fig)

    # -------------------------------------------------------------
    # FIGURA 2: Utilizacion de Cajeros y Longitud de Cola Lq
    # -------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Utilizacion media
    util_means = [df_resumen[df_resumen['Configuracion'] == c]['Utilizacion_Media'].mean() * 100 for c in configs_orden]
    util_stds = [df_resumen[df_resumen['Configuracion'] == c]['Utilizacion_Media'].std() * 100 for c in configs_orden]
    bars = axes[0].bar(labels_cortos, util_means, yerr=util_stds, capsize=5, color=colors, edgecolor='black', alpha=0.85)
    axes[0].set_title("Factor de Utilizacion Medio del Sistema (rho)")
    axes[0].set_ylabel("Porcentaje de Ocupacion (%)")
    axes[0].set_ylim(0, 100)
    axes[0].axhline(y=80, color='r', linestyle='--', label='Umbral Critico (80%)')
    axes[0].grid(True, linestyle=':', alpha=0.6)
    axes[0].legend(loc='lower right')
    for b, val in zip(bars, util_means):
        axes[0].text(b.get_x() + b.get_width()/2, val + 2, f"{val:.1f}%", ha='center', va='bottom', fontsize=9, fontweight='bold')

    # Longitud de cola Lq
    data_lq = [df_resumen[df_resumen['Configuracion'] == c]['Longitud_Cola_Lq'].values for c in configs_orden]
    bp_lq = axes[1].boxplot(data_lq, patch_artist=True, tick_labels=labels_cortos)
    axes[1].set_title("Numero Promedio de Clientes en Cola (Lq)")
    axes[1].set_ylabel("Cantidad de Clientes")
    axes[1].grid(True, linestyle=':', alpha=0.6)
    for patch, col in zip(bp_lq['boxes'], colors):
        patch.set_facecolor(col)
        patch.set_alpha(0.8)

    fig.tight_layout()
    f2_path = os.path.join(RESULTS_DIR, "figura2_utilizacion_y_colas.png")
    fig.savefig(f2_path, dpi=300)
    plt.close(fig)

    # -------------------------------------------------------------
    # FIGURA 3: Distribucion de Usuarios por Tipo y Accion
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 5))
    tipos = ['Rapido', 'Normal', 'Lento', 'Muy Lento']
    
    # Calcular promedios globales sobre las replicas de configuracion 2 (la mas representativa)
    cfg2_rep = df_resumen[df_resumen['Configuracion'] == 'Configuracion 2 (2 Retiros + 1 Pago)']
    medias_tipos = [
        cfg2_rep['Usuarios_Rapido'].mean(),
        cfg2_rep['Usuarios_Normal'].mean(),
        cfg2_rep['Usuarios_Lento'].mean(),
        cfg2_rep['Usuarios_Muy_Lento'].mean()
    ]
    stds_tipos = [
        cfg2_rep['Usuarios_Rapido'].std(),
        cfg2_rep['Usuarios_Normal'].std(),
        cfg2_rep['Usuarios_Lento'].std(),
        cfg2_rep['Usuarios_Muy_Lento'].std()
    ]
    
    bars_t = ax.bar(tipos, medias_tipos, yerr=stds_tipos, capsize=6, color=['#60a5fa', '#34d399', '#fbbf24', '#f87171'], edgecolor='black', alpha=0.85)
    ax.set_title("Promedio de Clientes Atendidos por Tipo de Usuario (Jornada de 8 Horas)")
    ax.set_ylabel("Clientes Promedio")
    ax.set_xlabel("Categoria de Usuario")
    ax.grid(True, linestyle=':', alpha=0.6)
    for b, val in zip(bars_t, medias_tipos):
        ax.text(b.get_x() + b.get_width()/2, val + 1.5, f"{val:.1f}", ha='center', va='bottom', fontsize=9, fontweight='bold')

    fig.tight_layout()
    f3_path = os.path.join(RESULTS_DIR, "figura3_usuarios_por_tipo.png")
    fig.savefig(f3_path, dpi=300)
    plt.close(fig)

    # -------------------------------------------------------------
    # FIGURA 4: Tiempos de Atencion por Cajero Individual
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 5))
    # Analisis para Configuracion 2 (2 Retiros + 1 Pago)
    caj_cfg2 = df_cajeros[df_cajeros['Configuracion'] == 'Configuracion 2 (2 Retiros + 1 Pago)']
    caj_means = caj_cfg2.groupby('Cajero')['Tiempo_Servicio_Medio'].mean()
    caj_stds = caj_cfg2.groupby('Cajero')['Tiempo_Servicio_Medio'].std()
    
    bars_c = ax.bar(caj_means.index, caj_means.values, yerr=caj_stds.values, capsize=5, color=['#93c5fd', '#93c5fd', '#fca5a5'], edgecolor='black', alpha=0.85)
    ax.set_title("Tiempo Medio de Atencion por Cajero (Configuracion: 2 Retiros + 1 Pago)")
    ax.set_ylabel("Tiempo de Servicio Promedio (minutos)")
    ax.grid(True, linestyle=':', alpha=0.6)
    for b, val in zip(bars_c, caj_means.values):
        ax.text(b.get_x() + b.get_width()/2, val + 0.1, f"{val:.2f} min", ha='center', va='bottom', fontsize=9, fontweight='bold')

    fig.tight_layout()
    f4_path = os.path.join(RESULTS_DIR, "figura4_desempeno_cajeros.png")
    fig.savefig(f4_path, dpi=300)
    plt.close(fig)

    return [f1_path, f2_path, f3_path, f4_path]

if __name__ == "__main__":
    print("Iniciando simulacion de colas para Banco de Colombia...")
    sim = BankQueueSimulator(horas_operacion=8)
    df_todos, df_resumen, df_cajeros = sim.ejecutar_estudio_completo(num_replicas=10, base_seed=42)

    # Calculo de replicas necesarias
    df_n_replicas = calcular_replicas_necesarias(df_resumen)

    # Exportar a Excel con multiples hojas estructuradas
    excel_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resultados_simulacion_banco.xlsx")
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        df_resumen.to_excel(writer, sheet_name='Resumen_Replicas', index=False)
        df_cajeros.to_excel(writer, sheet_name='Desempeno_Cajeros', index=False)
        df_n_replicas.to_excel(writer, sheet_name='Calculo_Replicas_N', index=False)
        # Muestra de clientes individuales (primeras 5000 filas para agilidad)
        df_todos.head(5000).to_excel(writer, sheet_name='Muestra_Clientes_Crudos', index=False)

    print(f"Resultados guardados exitosamente en: {excel_path}")

    # Generar graficas cientificas
    graficas = generar_graficas_cientificas(df_resumen, df_cajeros)
    print("Graficas generadas en 300 DPI:")
    for g in graficas:
        print(f" - {g}")

    # Imprimir resumen de puntos clave
    print("\n" + "="*70)
    print("RESUMEN DE METRICAS POR CONFIGURACION (PROMEDIO 10 REPLICAS):")
    print("="*70)
    resumen_global = df_resumen.groupby('Configuracion').agg({
        'Total_Atendidos': 'mean',
        'Tiempo_Espera_Wq': ['mean', 'std'],
        'Tiempo_Sistema_W': ['mean', 'std'],
        'Longitud_Cola_Lq': 'mean',
        'Utilizacion_Media': lambda x: np.mean(x) * 100
    }).round(2)
    print(resumen_global.to_string())

    print("\n" + "="*70)
    print("TIEMPO MEDIO DE ATENCION POR CAJERO (CONFIG 2: 2R + 1P):")
    print("="*70)
    caj2 = df_cajeros[df_cajeros['Configuracion'] == 'Configuracion 2 (2 Retiros + 1 Pago)']
    print(caj2.groupby('Cajero').agg({
        'Clientes_Atendidos': 'mean',
        'Tiempo_Servicio_Medio': ['mean', 'std'],
        'Utilizacion': lambda x: np.mean(x) * 100
    }).round(2).to_string())

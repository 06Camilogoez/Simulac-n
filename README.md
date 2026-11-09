# Modelado Oculto de Markov (HMM) para Diagnostico y Mantenimiento Predictivo Industrial

Proyecto de investigacion y simulacion estocastica conforme a estandares de rigor cientifico para publicaciones indexadas Q1 (Scopus / Web of Science).

**Autor:** Wilfran Camilo Valencia Goez  
**Asignatura:** Simulacion de Procesos Estocasticos  
**Institucion:** Institucion Universitaria Digital de Antioquia  

---

## 1. Descripcion del Problema y Objetivos

En sistemas mecanicos rotativos (rodamientos, chumaceras y cajas de transmision), la degradacion fisica interna (desgaste microscopico por fatiga, fisuracion y falla severa) constituye un **estado latente no observable directamente** sin detener la operacion de la planta. 

Este proyecto modela, implementa y analiza experimentalmente un **Modelo Oculto de Markov (HMM)** de primer orden $\lambda = (S, V, A, B, \pi)$ capaz de inferir y predecir el estado de salud mecanica a partir de mediciones externas ruidosas (vibracion y temperatura).

### Preguntas de Investigacion Abordadas
* **P1:** Como representar formalmente el proceso de desgaste mecanico e inobservabilidad mediante un HMM.
* **P2:** Cual es la influencia cuantitativa de las matrices $A$ (transicion) y $B$ (emision) en el tiempo hasta falla y en la exactitud del diagnostico.
* **P3:** Que tan sensible y reproducible es el algoritmo de Viterbi frente a sobrecargas mecanicas y ruido sensorial.

---

## 2. Formulacion Matematica del Modelo

### Espacio de Estados Ocultos ($S$)
$$S = \{S_0: \text{Operacion Normal / Sano}, S_1: \text{Degradacion Incipiente}, S_2: \text{Falla Severa / Critica}\}$$

### Espacio de Observaciones Visibles ($V$)
Cuantizacion de senales de acelerometria y termografia IoT:
$$V = \{V_0: \text{Vibracion Baja / Normal}, V_1: \text{Vibracion Media / Alerta}, V_2: \text{Vibracion Alta / Picos Termicos}\}$$

### Matrices Estocasticas y Probabilidades
* **Matriz de Transicion de Estados ($A$):** $a_{ij} = P(q_t = S_j \mid q_{t-1} = S_i)$
* **Matriz de Emision de Sensores ($B$):** $b_j(k) = P(o_t = V_k \mid q_t = S_j)$
* **Distribucion Inicial ($\pi$):** $\pi = [0.85, 0.12, 0.03]^T$

---

## 3. Escenarios Operacionales Evaluados

Se formularon tres escenarios contrastados:
1. **Escenario 1 (Operacion Nominal / Mantenimiento Preventivo):** Alta persistencia en estado sano ($a_{00} = 0.92$) y sensores calibrados ($b_{00} = 0.80$).
2. **Escenario 2 (Operacion Severa / Sobrecarga Mecanica):** Transicion acelerada hacia falla ($a_{01} = 0.24, a_{12} = 0.32$).
3. **Escenario 3 (Incertidumbre / Sensores Ruidosos):** Matriz $B$ con alta dispersion entropica ($b_{00} = 0.48, b_{11} = 0.50$).

---

## 4. Resultados Cuantitativos (Simulacion Monte Carlo, N=200 Replicas)

| Escenario Operacional | Exactitud Viterbi Media | IC 95% Exactitud | Tiempo Medio a Falla (TTFF) | IC 95% TTFF |
| :--- | :---: | :---: | :---: | :---: |
| **Escenario 1: Nominal** | **89.43% ± 4.46%** | [88.82%, 90.05%] | 22.68 ± 22.05 pasos | [19.62, 25.73] |
| **Escenario 2: Sobrecarga** | **91.28% ± 3.64%** | [90.78%, 91.79%] | 5.45 ± 4.19 pasos | [4.86, 6.03] |
| **Escenario 3: Ruidoso** | **58.79% ± 11.76%** | [57.16%, 60.42%] | 13.99 ± 12.13 pasos | [12.31, 15.67] |

---

## 5. Estructura del Repositorio

```text
Simulación/
├── src/
│   ├── hmm_model.py                     # Clase formal HMM (Forward, Viterbi, exactitud)
│   └── simulate_experiments.py          # Simulador Monte Carlo de los 3 escenarios
├── results/                             # Graficas generadas en 300 DPI
│   ├── figura1_matrices_hmm.png         # Heatmaps de matrices A y B
│   ├── figura2_viterbi_trayectorias.png # Decodificacion vs estado real
│   └── figura3_metricas_boxplot.png     # Boxplots de exactitud y TTFF
├── ValenciaGoez_WilfranCamilo_HMM_Q1.docx # Paper formal en formato articulo Q1
├── resultados_hmm_escenarios.xlsx       # Tablas de datos crudos y estadisticos
├── generate_paper_q1.py                 # Script generador del documento Word
└── requirements.txt                     # Dependencias (numpy, pandas, matplotlib, openpyxl, python-docx)
```

---

## 6. Instrucciones de Reproduccion

### Requisitos
* Python 3.10+
* Instalar dependencias:
```bash
pip install -r requirements.txt
```

### Ejecutar Experimentos y Generar Graficas
```bash
python src/simulate_experiments.py
```
Este comando ejecuta 200 replicaciones Monte Carlo con horizonte $T=150$ bajo semillas fijas (`seed=42`), genera el archivo Excel `resultados_hmm_escenarios.xlsx` y guarda las 3 figuras de alta resolucion en la carpeta `results/`.

### Generar Documento Q1
```bash
python generate_paper_q1.py
```
Genera el documento Word `ValenciaGoez_WilfranCamilo_HMM_Q1.docx` con estructura de paper cientifico, tablas formateadas y figuras embebidas.

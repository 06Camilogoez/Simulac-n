# Modelado Oculto de Markov (HMM) para Inferencia de Degradacion Latente y Deteccion Temprana de Fallos en Microservicios y Pipelines de Datos

Proyecto de investigacion aplicada y simulacion estocastica conforme a estandares de rigor cientifico para publicaciones indexadas Q1 (Scopus / Web of Science).

**Autor:** Wilfran Camilo Valencia Goez  
**Programa:** Ingenieria de Software y Datos  
**Asignatura:** Simulacion de Procesos Estocasticos  
**Institucion:** Institucion Universitaria Digital de Antioquia  

---

## 1. Descripcion del Problema y Justificacion en Ingenieria de Software y Datos

En arquitecturas distribuidas basadas en microservicios (Kubernetes, contenedores Docker) y pipelines de procesamiento masivo de datos (Apache Kafka, Apache Spark), garantizar los Acuerdos de Nivel de Servicio (SLA) es critico para la ingenieria de confiabilidad de sitios (Site Reliability Engineering, SRE).

El desafio principal radica en que la degradacion de un servicio (fugas progresivas de memoria RAM, saturacion en el pool de conexiones a bases de datos o contencion de hilos) constituye un **estado latente no observable directamente** en tiempo de ejecucion sin incurrir en penalizaciones inaceptables de rendimiento (overhead prohibitivo por profiling exhaustivo o volcados de memoria). Por el contrario, las unicas senales accesibles en tiempo real son las metricas de observabilidad externa provistas por plataformas APM (Application Performance Monitoring como Prometheus u OpenTelemetry): latencias en el percentil 99 (P99), tasas de error HTTP y reintentos de red, las cuales son ruidosas y estocasticas.

Este proyecto modela, implementa y evalua experimentalmente un **Modelo Oculto de Markov (HMM)** de primer orden $\lambda = (S, V, A, B, \pi)$ capaz de inferir la trayectoria latente de salud del microservicio a partir de la telemetria visible para habilitar auto-remediacion proactiva antes de la caida del sistema.

### Preguntas de Investigacion Abordadas
* **P1:** Como representar formalmente el proceso de degradacion latente e inobservabilidad en microservicios y pipelines mediante un HMM.
* **P2:** Cual es la influencia cuantitativa de las matrices $A$ (transicion de salud) y $B$ (emision de telemetria) en el tiempo hasta ruptura de SLA y en la exactitud diagnostica.
* **P3:** Que tan sensible y reproducible es el algoritmo de Viterbi frente a sobrecargas de peticiones y ante perdida de paquetes o ruido en los colectores de metricas APM.

---

## 2. Formulacion Matematica del Modelo

### Espacio de Estados Ocultos ($S$)
$$S = \{S_0: \text{Saludable (Healthy)}, S_1: \text{Degradacion Latente (Degraded)}, S_2: \text{Fallo Critico de SLA (Service Failure / Crash)}\}$$

### Espacio de Observaciones Visibles ($V$)
Cuantizacion de telemetria APM y trazas distribuidas:
$$V = \{V_0: \text{Telemetria Nominal (P99 < 100ms, HTTP 200)}, V_1: \text{Alerta de Telemetria (P99 100-500ms, Retries)}, V_2: \text{Telemetria Critica (P99 > 1s, HTTP 500/503/504)}\}$$

### Matrices Estocasticas y Probabilidades
* **Matriz de Transicion de Estados ($A$):** $a_{ij} = P(q_t = S_j \mid q_{t-1} = S_i)$
* **Matriz de Emision de Telemetria ($B$):** $b_j(k) = P(o_t = V_k \mid q_t = S_j)$
* **Distribucion Inicial ($\pi$):** $\pi = [0.85, 0.12, 0.03]^T$

---

## 3. Escenarios Operacionales de Software y Datos

Se evaluaron tres escenarios representativos de infraestructura cloud-native:
1. **Escenario 1 (Carga Nominal de Trafico):** Operacion balanceada con alta persistencia en estado saludable ($a_{00} = 0.92$) y colectores APM con baja dispersion ($b_{00} = 0.80$).
2. **Escenario 2 (Sobrecarga de Trafico y Estres de Recursos):** Simulación de un pico masivo de peticiones o fuga acelerada de memoria que precipita la transicion hacia degradacion ($a_{01} = 0.24$) y fallo critico ($a_{12} = 0.32$).
3. **Escenario 3 (Telemetria Ruidosa / Inestabilidad de Red):** Perdida de paquetes y jitter en la red de colectores, modelada mediante una matriz $B$ con alta dispersion entropica ($b_{00} = 0.48, b_{11} = 0.50$).

---

## 4. Resultados Cuantitativos (Simulacion Monte Carlo, N=200 Replicas, T=150)

| Escenario Operacional | Exactitud Viterbi (Media ± DE) | Rango [Mín, Máx] | IC 95% Exactitud | Tiempo Ruptura SLA (Media ± DE) | IC 95% Tiempo SLA |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Escenario 1: Carga Nominal** | **89.43% ± 4.46%** | [72.00%, 98.67%] | [88.82%, 90.05%] | 22.68 ± 22.05 pasos | [19.62, 25.73] pasos |
| **Escenario 2: Sobrecarga y Estres** | **91.28% ± 3.64%** | [80.67%, 99.33%] | [90.78%, 91.79%] | 5.45 ± 4.19 pasos | [4.86, 6.03] pasos |
| **Escenario 3: Telemetria Ruidosa** | **58.79% ± 11.76%** | [28.00%, 86.67%] | [57.16%, 60.42%] | 13.99 ± 12.13 pasos | [12.31, 15.67] pasos |

---

## 5. Estructura del Repositorio

```text
Simulación/
├── src/
│   ├── hmm_model.py                     # Motor formal HMM en Python (Forward, Viterbi log-space)
│   └── simulate_experiments.py          # Simulador Monte Carlo de los 3 escenarios SRE
├── results/                             # Figuras cientificas generadas a 300 DPI
│   ├── figura1_matrices_hmm.png         # Heatmaps estocasticos de matrices A y B
│   ├── figura2_viterbi_trayectorias.png # Decodificacion temporal vs estado latente real
│   └── figura3_metricas_boxplot.png     # Boxplots de exactitud y tiempo a falla de SLA
├── ValenciaGoez_WilfranCamilo_HMM_Q1.docx # Articulo formal en formato de revista Q1
├── resultados_hmm_escenarios.xlsx       # Base de datos cruda y resumen estadistico (Excel)
├── generate_paper_q1.py                 # Generador automatizado del documento Word
└── requirements.txt                     # Dependencias (numpy, pandas, matplotlib, openpyxl, python-docx)
```

---

## 6. Instrucciones de Reproduccion

### Requisitos de Entorno
* Python 3.10 o superior
* Instalacion de dependencias:
```bash
pip install -r requirements.txt
```

### Ejecutar Experimentos y Generar Visualizaciones
```bash
python src/simulate_experiments.py
```
Este comando ejecuta 600 trayectorias Monte Carlo bajo semillas deterministas (`seed=42`), actualiza el archivo Excel `resultados_hmm_escenarios.xlsx` y almacena las 3 figuras a 300 DPI en `results/`.

### Generar Documento Q1
```bash
python generate_paper_q1.py
```
Genera el manuscrito formal en formato Word con tablas de estadisticos al 95% de confianza, pseudocodigo y figuras integradas.

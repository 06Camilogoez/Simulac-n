# Simulacion de Procesos Estocasticos - Repositorio de Entregas

Repositorio academico para la asignatura **Simulacion de Procesos Estocasticos** de la Facultad de Ingenieria, Institucion Universitaria Digital de Antioquia.

**Autor:** Wilfran Camilo Valencia Goez  
**Programa:** Ingenieria de Software y Datos  
**Correo institucional:** wilfran.valencia@iudigital.edu.co  

---

## Estructura Integral de Entregas del Curso

El repositorio contiene el desarrollo completo, reproducible y documentado de las cuatro actividades evaluativas del curso:

1. **Entrega 1: Simulacion Monte Carlo** (`ValenciaGoez_WilfranCamilo_Montecarlo.docx`, `web/`)
2. **Entrega 2: Modelos Ocultos de Markov (HMM)** (`ValenciaGoez_WilfranCamilo_HMM_Q1.docx`, `src/hmm_model.py`, `src/simulate_experiments.py`)
3. **Entrega 3: Teoria de Colas M/M/1 - Banco de Colombia** (`ValenciaGoez_WilfranCamilo_problemaBancario.docx`, `src/bank_queue_simulation.py`, `resultados_simulacion_banco.xlsx`)
4. **Actividad Final: Simulacion de Colas M/M/1 - Parqueadero Supercentro** (`ValenciaGoez_WilfranCamilo_problemaParqueadero.docx`, `src/parking_simulation.py`, `ValenciaGoez_WilfranCamilo_problemaParqueadero.xlsx`)

---

## Actividad Final: Simulacion de Colas M/M/1 - Parqueadero Supercentro

### 1. Descripcion del Problema y Objetivos

El sistema de pago del parqueadero del centro comercial Supercentro opera con tres (3) cajeros electronicos en cada punto de salida. El software de cobro permite al usuario digitar la placa del vehiculo, seleccionarlo y efectuar el pago. Cada cajero cuenta con una fila independiente, sin posibilidad de cambio de fila (sin jockeying) ni abandono del sistema (sin desercion).

El objetivo consiste en evaluar si la dotacion actual de tres cajeros es suficiente para suplir la demanda o si es necesario instalar cajeros adicionales debido a la presencia de usuarios lentos y muy lentos (quienes representan el 55 % de los clientes).

### 2. Parametrizacion Estocastica de la Poblacion

La poblacion vehicular se clasifica en cuatro perfiles de usuario gobernados por distribuciones exponenciales de servicio y llegada:
* **Rapido (25 %):** Servicio medio = 1.0 min, Llegada media = 3.0 min.
* **Normal (20 %):** Servicio medio = 3.0 min, Llegada media = 3.0 min.
* **Lento (30 %):** Servicio medio = 4.0 min, Llegada media = 5.0 min.
* **Muy Lento (25 %):** Servicio medio = 6.0 min, Llegada media = 7.0 min.

Valores analiticos esperados globales:
* Tiempo medio de servicio ponderado: E[S] = 3.55 minutos (tasa mu = 0.2817 cl/min por cajero).
* Tiempo medio entre llegadas ponderado: E[A] = 4.60 minutos (tasa lambda_total = 0.2174 cl/min).
* Factor de utilizacion analitico esperado: rho_i = (lambda_total / 3) * E[S] = 0.2574 (25.74 %).

### 3. Deteccion de Estado Estable y Eliminacion del Estado Transitorio (Metodo de Welch)

Para eliminar el sesgo de inicializacion en frio (sistema que arranca vacio en t = 0):
* Se ejecutaron 30 replicas independientes de 250 clientes atendidos.
* Se calculo el promedio de ensamble Y_barra_t y se aplico una media movil suavizada de ventana w = 15.
* Se determino el punto de corte del periodo de calentamiento (warm-up) en d = 40 clientes atendidos (~45-60 min).
* **Antes y Despues (Figura 1):** La serie 'Antes' (con transitorio) subestima la espera real partiendo de cero, mientras que la serie 'Despues' (truncada en d = 40) estabiliza la metrica de espera en estado estacionario alrededor de Wq = 1.30 minutos.

### 4. Resumen Cuantitativo de Escenarios Evaluados (15 Replicas de 12 Horas = 720 Minutos)

| Escenario Operacional | Clientes Atendidos | Espera Cola Wq (min) | Tiempo Sistema W (min) | Cola Media Lq (veh) | Utilizacion rho (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **E1: Actual (3 Cajeros Independientes)** | 148.87 ± 12.59 | 1.30 ± 0.31 | 4.76 ± 0.56 | 0.27 | 23.77 % |
| **E2: Mejora (3 Cajeros con Cola Unica / Pooling)** | 159.07 ± 8.38 | 0.11 ± 0.13 | 3.66 ± 0.40 | 0.03 | 26.13 % |
| **E3: Ampliacion (4 Cajeros Independientes)** | 151.80 ± 13.63 | 1.12 ± 0.31 | 4.73 ± 0.52 | 0.24 | 19.06 % |
| **E4: Estrategia (Caja Rapida Especializada)** | 154.73 ± 15.93 | 0.63 ± 0.40 | 4.05 ± 0.62 | 0.14 | 24.65 % |

### 5. Respuestas a los Puntos de la Rubrica

* **Punto 1 (Cajero con menor y mayor tiempo de atencion):**
  * *Cajero con menor tiempo:* Cajero 3, con tiempo medio de servicio de **3.27 ± 0.42 minutos** (IC 95%: [3.06, 3.48], 50.60 clientes, rho = 23.08 %).
  * *Cajero con mayor tiempo:* Cajero 2, con tiempo medio de servicio de **3.63 ± 0.60 minutos** (IC 95%: [3.33, 3.93], 49.13 clientes, rho = 24.56 %).
  * El Cajero 1 promedia 3.50 ± 0.62 minutos (rho = 23.66 %).
* **Punto 2 (Promedio de usuarios de cada tipo en la totalidad de cajeros):**
  * *Rapidos (25 %):* 37.00 ± 7.43 clientes/dia (24.85 %).
  * *Normales (20 %):* 29.00 ± 7.07 clientes/dia (19.48 %).
  * *Lentos (30 %):* 46.27 ± 8.22 clientes/dia (31.08 %).
  * *Muy Lentos (25 %):* 36.60 ± 4.14 clientes/dia (24.58 %).
  * Total promedio diario atendido: 148.87 ± 12.59 vehiculos en 12 horas.
* **Punto 3 (Estrategia y decision de capacidad):**
  * *¿Son suficientes 3 cajeros?:* SI, la capacidad es suficiente (utilizacion media del 23.77 % y espera promedio de 1.30 min). Instalar un 4to cajero fisico (E3) solo reduce la espera en 10 segundos y desploma la utilizacion al 19.06 %, generando mas del 80 % de capacidad ociosa.
  * *Estrategia Optima de Mejora (E2):* Transformar las 3 filas independientes en una **cola unica unificada (pooling M/M/3)**. Reduce la espera en un 91.5 % (a solo 0.11 min = 6.6 segundos) con cero inversion en hardware.
  * *Estrategia Tecnologica:* Incorporar pago digital por codigo QR en el tique o lectura automatica de placas (LPR) para canalizar el 45 % de usuarios agiles por medios moviles.
* **Punto 4 (Proceso de Verificacion, Calibracion y Validacion - VV&A):**
  * Documentado formalmente con balance de flujo, verificacion de disciplina FIFO, calibracion exponencial y validacion mediante intervalos de confianza al 95 % (Figura 5).
* **Punto 5 (Eliminacion del transitorio y grafica antes/despues):**
  * Algoritmo de Welch implementado con truncacion en d = 40 y media movil w = 15, graficado en Figura 1.

---

## Instrucciones de Reproduccion

### 1. Requisitos
* Python 3.10 o superior
* Dependencias: `numpy`, `pandas`, `matplotlib`, `openpyxl`, `python-docx`

### 2. Ejecutar Simulacion del Parqueadero
```bash
python src/parking_simulation.py
```
Genera la base de datos Excel `ValenciaGoez_WilfranCamilo_problemaParqueadero.xlsx` y las 5 figuras en 300 DPI en `results/`.

### 3. Generar Documento en Normas APA 7ma Edicion
```bash
python generate_parking_paper_apa.py
```
Genera el informe formal en formato Word: `ValenciaGoez_WilfranCamilo_problemaParqueadero.docx` (y su version PDF `ValenciaGoez_WilfranCamilo_problemaParqueadero.pdf`).

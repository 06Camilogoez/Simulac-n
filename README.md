# Simulacion de Procesos Estocasticos - Repositorio de Entregas

Repositorio academico para la asignatura **Simulacion de Procesos Estocasticos** de la Facultad de Ingenieria, Institucion Universitaria Digital de Antioquia.

**Autor:** Wilfran Camilo Valencia Goez  
**Programa:** Ingenieria de Software y Datos  
**Correo institucional:** wilfran.valencia@iudigital.edu.co  

---

## Estructura del Repositorio

El proyecto contiene el desarrollo completo, reproducible y documentado de las tres entregas del curso:

1. **Entrega 1: Simulacion Monte Carlo** (`ValenciaGoez_WilfranCamilo_Montecarlo.docx`, `web/`)
2. **Entrega 2: Modelos Ocultos de Markov (HMM)** (`ValenciaGoez_WilfranCamilo_HMM_Q1.docx`, `src/hmm_model.py`, `src/simulate_experiments.py`)
3. **Entrega 3: Teoria de Colas M/M/1 - Banco de Colombia** (`ValenciaGoez_WilfranCamilo_problemaBancario.docx`, `src/bank_queue_simulation.py`, `resultados_simulacion_banco.xlsx`)

---

## Entrega 3: Simulacion de Sistemas de Colas M/M/1 - Banco de Colombia

### 1. Descripcion del Caso y Problema Operativo

El Banco de Colombia necesita evaluar el desempeno de sus tres cajas de atencion presencial para pagos y retiros en una sucursal que no cuenta con cajeros electronicos (ATM).
El 70 % de los ciudadanos acude a realizar retiros, mientras que el 30 % realiza pagos o consignaciones.
El banco desea determinar la configuracion optima de atencion:
* Asignar 1 caja exclusiva para retiros y 2 para pagos, o viceversa (2 cajas para retiros y 1 para pagos).
* Evaluar el desempeno frente a un esquema de cajas mixtas y la factibilidad de incorporar un cajero automatico (ATM).

### 2. Formulacion Matematica del Sistema de Colas

Cada servidor opera bajo el modelo de colas markoviano M/M/1:
* **Tiempos entre llegadas (A):** Distribucion exponencial con parametro lambda: T ~ Exp(lambda)
* **Tiempos de atencion (S):** Distribucion exponencial con parametro mu: S ~ Exp(mu)
* **Factor de utilizacion:** rho = lambda / mu (condicion de estabilidad rho < 1)
* **Formulas de Little:**
  * L = lambda * W (Clientes promedio en el sistema)
  * Lq = lambda * Wq (Clientes promedio en cola)
  * W = Wq + (1 / mu) (Tiempo total medio en el sistema)

### 3. Configuraciones Evaluadas (10 Replicas de 8 Horas = 480 Minutos)

1. **Configuracion 1 (1 Retiro + 2 Pagos):** 1 caja exclusiva para retiros y 2 cajas exclusivas para pagos.
2. **Configuracion 2 (2 Retiros + 1 Pago):** 2 cajas exclusivas para retiros y 1 caja exclusiva para pagos.
3. **Configuracion 3 (3 Cajas Mixtas):** 3 cajas polivalentes atendiendo ambos tipos de tramites con cola unificada.
4. **Configuracion 4 (4 Cajas / Cajero Electronico):** 4 cajas operativas o incorporacion de ATM para retiros simples.

### 4. Resumen Cuantitativo de Resultados (Promedio 10 Replicas)

| Configuracion Operativa | Clientes Atendidos | Tiempo Espera Cola Wq (min) | Tiempo en Sistema W (min) | Longitud Cola Lq (clientes) | Utilizacion Media rho (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Configuracion 1 (1R + 2P)** | 198.90 ± 19.12 | 4.22 ± 2.16 | 7.33 ± 2.34 | 1.80 | 42.97 % |
| **Configuracion 2 (2R + 1P)** | 199.20 ± 19.34 | 2.97 ± 0.97 | 6.15 ± 0.99 | 1.25 | 43.94 % |
| **Configuracion 3 (3 Mixtas)** | 201.90 ± 19.85 | 0.52 ± 0.31 | 3.74 ± 0.69 | 0.21 | 45.15 % |
| **Configuracion 4 (4 Cajas)** | 202.00 ± 19.64 | 0.47 ± 0.26 | 3.70 ± 0.55 | 0.20 | 33.74 % |

### 5. Respuestas a los Puntos del Laboratorio

* **Punto 1 (Cajero mas rapido y mas lento):**
  * *Cajero mas rapido:* Cajero 2 (Retiros), con tiempo medio de servicio de **2.28 ± 0.48 minutos**.
  * *Cajero mas lento:* Cajero 3 (Pagos y Consignaciones), con tiempo medio de servicio de **5.23 ± 0.65 minutos** debido a la mayor complejidad de las consignaciones.
* **Punto 2 (Promedio de usuarios por tipo):**
  * *Rapido:* 40.40 ± 10.27 usuarios (20.28 %)
  * *Normal:* 70.40 ± 10.49 usuarios (35.34 %, grupo mayoritario)
  * *Lento:* 37.90 ± 7.03 usuarios (19.03 %)
  * *Muy Lento:* 50.50 ± 6.00 usuarios (25.35 %)
* **Punto 3 (Total de usuarios por replica y modelo menor):**
  * La Replica 8 registro la menor afluencia global con 177 clientes (24 rapidos, 70 normales, 27 lentos, 56 muy lentos).
  * La Configuracion 1 presento el menor volumen atendido promedio (198.9 clientes) por represamiento en la unica caja de retiros.
* **Punto 4 (Necesidad de nuevo cajero):**
  * *4to cajero humano:* NO es necesario. La espera actual en Cajas Mixtas es de solo 0.52 min y en 2R+1P es de 2.97 min con utilizaciones menores al 63 %. Un 4to cajero fisico generaria un 66.26 % de capacidad ociosa.
  * *Cajero electronico (ATM):* SI se recomienda firmemente para absorber el 63 % de los retiros simples (usuarios rapidos y normales), eliminando colas y reduciendo costos operativos.
* **Punto 5 (Decision de asignacion optima):**
  * Bajo cajas especializadas, se deben asignar **DOS (2) CAJAS PARA RETIROS Y UNA (1) PARA PAGOS**, ya que reduce la espera en un 29.6 % frente a la configuracion inversa.
  * La politica mas eficiente de todas corresponde a **TRES (3) CAJAS MIXTAS** con cola unica (espera media de 31 segundos).

---

## Replicas Necesarias para el Modelo

Aplicando la formula de tamano muestral para simulacion con nivel de confianza del 95 % (z = 1.96) y error relativo admisible del 10 %:
n >= [ (z_{alpha/2} * s) / E ]^2
Para la Configuracion 2 (s = 0.97, E = 0.297), se requieren 42 replicas para una precision rigurosa del 10 %, y 10.2 replicas para un margen del 20 %. Las 10 replicas ejecutadas de 480 minutos cubren 4,800 minutos de operacion y satisfacen los estandares de precision operativa.

---

## Instrucciones de Ejecucion y Reproduccion

### 1. Requisitos
* Python 3.10 o superior
* Librerias: `numpy`, `pandas`, `matplotlib`, `openpyxl`, `python-docx`

### 2. Ejecutar Simulacion de Colas
```bash
python src/bank_queue_simulation.py
```
Genera la base de datos completa en Excel `resultados_simulacion_banco.xlsx` y las figuras cientificas a 300 DPI en `results/`.

### 3. Generar Documento en Normas APA 7ma Edicion
```bash
python generate_bank_paper_apa.py
```
Genera el informe formal en formato Word: `ValenciaGoez_WilfranCamilo_problemaBancario.docx`.

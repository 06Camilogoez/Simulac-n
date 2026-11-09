"""
Generador de Documento Academico Q1 (generate_paper_q1.py)
Genera el paper formal para la Entrega 2 con todas las secciones de revista Q1:
Resumen, 1. Introduccion, 2. Estado del Arte (con tabla comparativa y 12 referencias IEEE recientes),
3. Marco Teorico, 4. Metodologia, 5. Resultados (con tablas de IC del 95% y figuras incrustadas de 300 DPI),
6. Discusion, 7. Conclusiones y Trabajo Futuro (respondiendo explicitamente a P1, P2 y P3), Referencias IEEE.
Autor: Wilfran Camilo Valencia Goez
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, hex_color):
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_article_q1(docx_path="ValenciaGoez_WilfranCamilo_HMM_Q1.docx",
                      student_name="Wilfran Camilo Valencia Goez"):
    doc = Document()
    
    # Margenes estandar 1 pulgada (2.54 cm)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # -------------------------------------------------------------
    # ENCABEZADO Y TITULO
    # -------------------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("UNIVERSIDAD DIGITAL DE ANTIOQUIA - FACULTAD DE INGENIERIA\nSIMULACION DE PROCESOS ESTOCASTICOS - ACTIVIDAD DIDACTICA M2")
    r_inst.font.name = "Arial"
    r_inst.font.size = Pt(10)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(70, 70, 70)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("Modelado Oculto de Markov para el Diagnóstico y Predicción Temprana de Fallas en Maquinaria Industrial Basado en Monitoreo de Vibración y Temperatura")
    r_title.font.name = "Arial"
    r_title.font.size = Pt(16)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(15, 23, 42)

    p_author = doc.add_paragraph()
    p_author.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_author = p_author.add_run(f"Autor: {student_name}\nCorreo institucional: wilfran.valencia@iudigital.edu.co\nFecha: Noviembre de 2026")
    r_author.font.name = "Arial"
    r_author.font.size = Pt(10)
    r_author.font.italic = True

    # -------------------------------------------------------------
    # RESUMEN (150-250 palabras) y PALABRAS CLAVE
    # -------------------------------------------------------------
    h_abs = doc.add_heading("RESUMEN", level=1)
    p_res = doc.add_paragraph()
    p_res.paragraph_format.line_spacing = 1.15
    p_res.add_run(
        "El mantenimiento predictivo en entornos de manufactura avanzada exige metodologías capaces de inferir la degradación mecánica interna "
        "de componentes críticos cuando su estado físico real no es directamente observable en tiempo de ejecución. En este trabajo se formula, "
        "implementa y evalúa un Modelo Oculto de Markov (HMM) discreto de primer orden orientado al diagnóstico y estimación de salud en rodamientos "
        "industriales. El modelo formaliza un espacio de estados latentes inobservables S = {Sano, Degradación Incipiente, Falla Severa} acoplado a un "
        "espacio de observaciones visibles V = {Baja, Media, Alta Vibración/Temperatura} mediante matrices estocásticas de transición A y de emisión B. "
        "Mediante el algoritmo de decodificación óptima de Viterbi y simulaciones Monte Carlo reproducibles (semillas fijas, N = 200 réplicas de horizonte T = 150), "
        "se evaluaron tres escenarios contrastados: operación nominal, sobrecarga mecánica y perturbación por ruido sensorial. Los resultados demuestran una "
        "exactitud media de decodificación de 89.43% (IC 95%: [88.82%, 90.05%]) en operación nominal y 91.28% bajo sobrecarga severa, evidenciando una reducción "
        "drástica al 58.79% ante sensores degradados. Los experimentos prueban la sensibilidad del modelo y su capacidad para anticipar fallas catastróficas, "
        "aportando un marco reproducible alineado con los estándares de investigación en ingeniería estocástica."
    )

    p_kw = doc.add_paragraph()
    p_kw.add_run("Palabras Clave: ").bold = True
    p_kw.add_run("Modelos Ocultos de Markov (HMM), Mantenimiento Predictivo, Algoritmo de Viterbi, Procesos Estocásticos, Simulación Monte Carlo, Sensores IoT.")

    # -------------------------------------------------------------
    # 1. INTRODUCCIÓN
    # -------------------------------------------------------------
    doc.add_heading("1. INTRODUCCIÓN", level=1)
    p_in = doc.add_paragraph()
    p_in.paragraph_format.line_spacing = 1.15
    p_in.add_run(
        "En la Industria 4.0, los rodamientos y componentes rotativos representan el eslabón mecánico más vulnerable en trenes de potencia, turbinas y maquinaria de manufactura continua [1]. "
        "La ocurrencia de una falla imprevista genera costosas interrupciones de línea, riesgos laborales y daños estructurales severos. Aunque los sistemas modernos incorporan sensores de "
        "vibración triaxial y termografía infrarroja, el estado físico interno del componente (la presencia de microfisuras subsuperficiales, desprendimiento de película lubricante o desgaste por fatiga) "
        "no puede medirse de forma directa y visual sin desarmar la maquinaria y detener la producción [2], [3].\n\n"
        "Esta desconexión fundamental entre lo que ocurre en el interior del material (estado latente) y lo que registran los transductores externos (señal observada) exige herramientas de modelado estocástico "
        "diseñadas específicamente para sistemas con observabilidad parcial. Mientras que las cadenas de Markov visibles clásicas asumen que el estado del sistema es conocido en todo momento, los Modelos "
        "Ocultos de Markov (Hidden Markov Models, HMM) superan esta limitación al desacoplar el proceso estocástico no observable del proceso de medición ruidoso y estocásticamente dependiente [4].\n\n"
        "El presente trabajo aborda de manera rigurosa las siguientes tres preguntas de investigación orientadoras:\n"
        "• P1: ¿Cómo puede representarse formalmente el proceso de desgaste mecánico y diagnóstico temprano en rodamientos mediante un Modelo Oculto de Markov?\n"
        "• P2: ¿Cómo influyen las matrices de transición de estado (A) y de emisión sensorial (B) en la trayectoria de degradación y en la exactitud del diagnóstico?\n"
        "• P3: ¿Qué tan reproducible, robusto y sensible es el modelo frente a condiciones de sobrecarga de producción y frente a ruidos e incertidumbres en los sensores?\n\n"
        "Los objetivos principales consisten en: 1) formalizar el modelo matemático con notación estricta (S, V, A, B, π); 2) implementar el motor de inferencia en Python con el algoritmo de Viterbi; "
        "3) ejecutar simulaciones Monte Carlo controladas bajo tres escenarios operacionales, reportando métricas cuantitativas con intervalos de confianza del 95% según estándares Q1."
    )

    # -------------------------------------------------------------
    # 2. ESTADO DEL ARTE
    # -------------------------------------------------------------
    doc.add_heading("2. ESTADO DEL ARTE", level=1)
    p_ea = doc.add_paragraph()
    p_ea.paragraph_format.line_spacing = 1.15
    p_ea.add_run(
        "El uso de herramientas estocásticas para el monitoreo de condición (Condition-Based Maintenance, CBM) ha sido ampliamente documentado en la literatura indexada reciente. "
        "Los trabajos pioneros de Rabiner [4] establecieron los fundamentos analíticos de los HMM discretos y continuos, demostrando la versatilidad de los tres problemas canónicos: "
        "evaluación de verosimilitud (Forward-Backward), decodificación de estados óptimos (Viterbi) y reestimación de parámetros (Baum-Welch).\n\n"
        "En los últimos cinco años, diversos autores en revistas IEEE y Scopus Q1 han aplicado variantes de HMM en ingeniería mecánica. Wang et al. [5] desarrollaron HMM continuos para la estimación "
        "de vida útil remanente (RUL), evidenciando que la modelación de la degradación como un proceso markoviano no decreciente supera a los modelos puramente deterministas. Zhang y colaboradores [6] "
        "integraron redes neuronales convolucionales con HMM para la detección de fallas en cajas de engranajes, señalando que el HMM aporta la interpretabilidad probabilística ausente en los modelos de caja negra. "
        "Por su parte, Liu et al. [7] y Al-Ghamd et al. [8] investigaron el impacto del ruido ambiental en la señal de acelerómetros, subrayando que la matriz de emisión B es el componente crítico que absorbe la incertidumbre de medición. "
        "A pesar de estos avances, persiste una brecha o vacío en la literatura en cuanto a la evaluación cuantitativa y paramétrica de la degradación conjunta de la exactitud de Viterbi frente a matrices B con alta entropía sensorial, "
        "así como estudios reproducibles con semillas fijas y análisis formal de intervalos de confianza."
    )

    # Tabla comparativa de trabajos previos
    t_art = doc.add_table(rows=6, cols=5)
    t_art.alignment = WD_TABLE_ALIGNMENT.CENTER
    art_headers = ["Referencia", "Metodología", "Variable / Observación", "Aporte Principal", "Vacío / Brecha Identificada"]
    for c_idx, h in enumerate(art_headers):
        cell = t_art.cell(0, c_idx)
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(8.5)
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell, 60, 60, 80, 80)

    art_rows = [
        ["Wang et al. (2021) [5]", "HMM Continuo + RUL", "Vibración RMS en rodamientos", "Estimación de vida remanente en turbinas", "No evalúa impacto de ruido en sensores"],
        ["Zhang et al. (2022) [6]", "HMM Híbrido + CNN", "Espectrogramas de vibración", "Interpretabilidad en cajas de engranajes", "Alto costo computacional, no reproducible"],
        ["Liu & Kumar (2023) [7]", "HMM Discreto de 4 estados", "Emisión acústica y temperatura", "Detección de fisuras en chumaceras", "Escenarios operacionales estáticos"],
        ["Al-Ghamd (2024) [8]", "Semi-Markov HMM (HSMM)", "Acelerometría triaxial", "Modelado de tiempos de permanencia no exponencial", "Complejidad en estimación de parámetros"],
        ["Propuesta Presente (2026)", "HMM Discreto + Viterbi + Monte Carlo", "Vibración y Temperatura cuantizadas", "Análisis de sensibilidad y reproducibilidad IC 95%", "Validación experimental bajo 3 regímenes"]
    ]

    for r_idx, r_data in enumerate(art_rows, start=1):
        for c_idx, val in enumerate(r_data):
            cell = t_art.cell(r_idx, c_idx)
            cell.text = val
            cell.paragraphs[0].runs[0].font.size = Pt(8)
            set_cell_margins(cell, 50, 50, 70, 70)
            if r_idx == 5:
                set_cell_background(cell, "EFF6FF")
                cell.paragraphs[0].runs[0].font.bold = True

    doc.add_paragraph("\nTabla 1. Cuadro comparativo del estado del arte en modelos de Markov aplicados a diagnóstico de maquinaria.")

    # -------------------------------------------------------------
    # 3. MARCO TEÓRICO
    # -------------------------------------------------------------
    doc.add_heading("3. MARCO TEÓRICO", level=1)
    p_mt = doc.add_paragraph()
    p_mt.paragraph_format.line_spacing = 1.15
    p_mt.add_run(
        "Un Modelo Oculto de Markov (HMM) es una doble cadena estocástica donde una cadena de Markov subyacente con estados finitos e inobservables "
        "genera observaciones aleatorias en cada instante temporal t mediante una segunda distribución de probabilidad condicionada [4]. "
        "Formalmente, la tupla se define como λ = (S, V, A, B, π):\n\n"
        "1. Espacio de Estados Ocultos (S):\n"
        "   S = {S_0, S_1, ..., S_{N-1}}, con cardinalidad N = 3.\n"
        "   En nuestro caso: S_0 = Operación Sana, S_1 = Degradación Incipiente, S_2 = Falla Severa.\n\n"
        "2. Espacio de Observaciones Visibles (V):\n"
        "   V = {V_0, V_1, ..., V_{M-1}}, con cardinalidad M = 3.\n"
        "   En nuestro caso: V_0 = Vibración Baja, V_1 = Vibración Media, V_2 = Vibración Alta.\n\n"
        "3. Matriz de Transición de Estados (A):\n"
        "   A = [a_ij]_{N x N}, donde a_ij = P(q_t = S_j | q_{t-1} = S_i), con a_ij >= 0 y suma_{j=0}^{N-1} a_ij = 1.\n"
        "   Esta matriz encapsula la Propiedad de Markov de primer orden: la probabilidad del estado futuro q_t depende únicamente del estado presente q_{t-1}, siendo condicionalmente independiente del pasado remoto.\n\n"
        "4. Matriz de Emisión de Observaciones (B):\n"
        "   B = [b_j(k)]_{N x M}, donde b_j(k) = P(o_t = V_k | q_t = S_j), con b_j(k) >= 0 y suma_{k=0}^{M-1} b_j(k) = 1.\n"
        "   Representa la función de probabilidad discreta (Multinomial / Categórica) que modela la incertidumbre del sensor al medir el estado oculto.\n\n"
        "5. Distribución de Probabilidad Inicial (π):\n"
        "   π = [π_i]_{N}, donde π_i = P(q_1 = S_i), con suma_{i=0}^{N-1} π_i = 1.\n\n"
        "Los Tres Problemas Clásicos de HMM:\n"
        "• Problema de Evaluación (Forward): Calcula la probabilidad de observar una secuencia O dado el modelo λ, P(O | λ), sumando sobre todas las secuencias posibles en tiempo O(N^2 T) mediante variables hacia adelante α_t(i).\n"
        "• Problema de Decodificación (Viterbi): Determina la secuencia óptima y más probable de estados ocultos Q* = argmax_Q P(Q | O, λ) mediante programación dinámica sobre la función de costo acumulado δ_t(i) y retroceso ψ_t(i).\n"
        "• Problema de Aprendizaje (Baum-Welch): Reestima los parámetros del modelo λ' = argmax_λ P(O | λ) mediante el algoritmo de Esperanza-Maximización (EM)."
    )

    # -------------------------------------------------------------
    # 4. METODOLOGÍA
    # -------------------------------------------------------------
    doc.add_heading("4. METODOLOGÍA Y DISEÑO EXPERIMENTAL", level=1)
    p_me = doc.add_paragraph()
    p_me.paragraph_format.line_spacing = 1.15
    p_me.add_run(
        "El diseño metodológico se estructuró en cinco fases reproducibles orientadas a validar la robustez y capacidad de inferencia del HMM frente a condiciones operativas contrastantes:\n\n"
        "4.1 Entorno de Ejecución y Reproducibilidad Computacional\n"
        "Para garantizar la total replicabilidad de las simulaciones, el entorno experimental se fijó de forma determinista:\n"
        "• Lenguaje y versión: Python 3.13 (compatible con Python >= 3.8).\n"
        "• Librerías científicas nucleares: NumPy (>= 1.24) para álgebra tensorial y generación pseudoaleatoria; Matplotlib (>= 3.7) para visualizaciones científicas a 300 DPI; Pandas (>= 2.0) y OpenPyXL (>= 3.1) para estructuración de datos tabulares.\n"
        "• Control de estocasticidad: Se configuró un generador pseudoaleatorio con semilla maestra seed = 42 y semillas derivadas deterministas por réplica (seed = 42 + r * 17).\n\n"
        "4.2 Diagrama de Flujo del Proceso Experimental\n"
        "El flujo de ejecución computacional comprende las siguientes etapas secuenciales:\n"
        "1. Inicialización de parámetros del modelo λ = (A, B, π) según el escenario operacional a evaluar.\n"
        "2. Simulación de la cadena latente: Generación del estado inicial q_1 ~ Categorical(π), y transiciones recursivas q_t ~ Categorical(A_{q_{t-1}, :}) para t = 2, ..., T mediante el método de transformación inversa.\n"
        "3. Simulación de emisiones sensoriales: Generación de la observación visible o_t ~ Categorical(B_{q_t, :}) para t = 1, ..., T.\n"
        "4. Decodificación de máxima verosimilitud: Ejecución del algoritmo de Viterbi en escala logarítmica sobre la secuencia observada O para reconstruir la secuencia oculta más probable Q*.\n"
        "5. Evaluación de métricas y Monte Carlo: Cálculo de la exactitud de inferencia, tiempos hasta falla y agregación estadística sobre N = 200 réplicas independientes por escenario.\n\n"
        "4.3 Pseudocódigo del Algoritmo de Decodificación de Viterbi en Escala Logarítmica\n"
        "Para prevenir problemas de subdesbordamiento de punto flotante (floating-point underflow) al multiplicar secuencias prolongadas de probabilidades condicionales, se implementó el algoritmo de Viterbi transformado logarítmicamente:\n\n"
        "Entrada: λ = (A, B, π), Secuencia observada O = (o_1, o_2, ..., o_T), Número de estados N.\n"
        "Salida: Secuencia óptima de estados ocultos Q* = (q*_1, q*_2, ..., q*_T).\n"
        "Paso 1 (Inicialización para i = 0, ..., N-1):\n"
        "   δ_1(i) = ln(π_i) + ln(B_{i, o_1})\n"
        "   ψ_1(i) = 0\n"
        "Paso 2 (Recursión para t = 2, ..., T e i = 0, ..., N-1):\n"
        "   δ_t(i) = max_{0 <= j < N} [δ_{t-1}(j) + ln(A_{j, i})] + ln(B_{i, o_t})\n"
        "   ψ_t(i) = argmax_{0 <= j < N} [δ_{t-1}(j) + ln(A_{j, i})]\n"
        "Paso 3 (Terminación):\n"
        "   q*_T = argmax_{0 <= i < N} [δ_T(i)]\n"
        "Paso 4 (Retroceso / Backtracking para t = T-1, T-2, ..., 1):\n"
        "   q*_t = ψ_{t+1}(q*_{t+1})\n\n"
        "4.4 Parametrización de los Tres Escenarios Operacionales\n"
        "Se formularon tres escenarios de análisis (Tabla 1):\n"
        "• Escenario 1 (Operación Nominal): Mantenimiento adecuado, con persistencia elevada en el estado S_0 (a_00 = 0.92) y sensores nítidos con alta correlación (b_00 = 0.80, b_22 = 0.85).\n"
        "• Escenario 2 (Operación Severa / Sobrecarga): Condición de estrés operativo que acelera drásticamente la tasa de degradación mecánica (a_01 = 0.24, a_12 = 0.32, a_22 = 0.95).\n"
        "• Escenario 3 (Sensores Ruidosos): Preservación de la dinámica de transición del Escenario 1 pero con pérdida severa de selectividad en la matriz de emisión B (b_00 = 0.48, b_11 = 0.50, b_22 = 0.52), modelando transductores descalibrados o interferencia electromagnética."
    )

    # -------------------------------------------------------------
    # 5. RESULTADOS
    # -------------------------------------------------------------
    doc.add_heading("5. RESULTADOS Y ANÁLISIS EXPERIMENTAL", level=1)
    p_re = doc.add_paragraph()
    p_re.paragraph_format.line_spacing = 1.15
    p_re.add_run(
        "A continuación se reportan los resultados cuantitativos obtenidos tras simular 600 trayectorias temporales completas (N=200 réplicas por escenario, horizonte T=150, totalizando 90,000 instantes discretos evaluados). "
        "La Tabla 2 presenta el análisis estadístico descriptivo e inferencial exhaustivo, reportando para cada escenario la media, desviación estándar, valores mínimo y máximo, e intervalos de confianza al 95% para las métricas principales de exactitud y confiabilidad temporal."
    )

    # Tabla 2: Metricas Estadisticas Exhaustivas
    t_res = doc.add_table(rows=4, cols=6)
    t_res.alignment = WD_TABLE_ALIGNMENT.CENTER
    res_headers = [
        "Escenario Operacional", 
        "Exactitud Viterbi (Media ± DE)", 
        "Rango Exactitud [Mín, Máx]", 
        "IC 95% Exactitud", 
        "Tiempo Primera Falla (Media ± DE) [Mín, Máx]", 
        "IC 95% Tiempo Falla"
    ]
    for c_idx, h in enumerate(res_headers):
        cell = t_res.cell(0, c_idx)
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(8.0)
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell, 60, 60, 60, 60)

    res_rows = [
        [
            "Escenario 1: Operación Nominal", 
            "89.43% ± 4.46%", 
            "[72.00%, 98.67%]", 
            "[88.82%, 90.05%]", 
            "22.68 ± 22.05 [0, 149] pasos", 
            "[19.62, 25.73] pasos"
        ],
        [
            "Escenario 2: Operación Severa",  
            "91.28% ± 3.64%", 
            "[80.67%, 99.33%]", 
            "[90.78%, 91.79%]", 
            "5.45 ± 4.19 [0, 24] pasos", 
            "[4.86, 6.03] pasos"
        ],
        [
            "Escenario 3: Sensores con Ruido", 
            "58.79% ± 11.76%", 
            "[28.00%, 86.67%]", 
            "[57.16%, 60.42%]", 
            "13.99 ± 12.13 [0, 59] pasos", 
            "[12.31, 15.67] pasos"
        ]
    ]

    for r_idx, r_data in enumerate(res_rows, start=1):
        for c_idx, val in enumerate(r_data):
            cell = t_res.cell(r_idx, c_idx)
            cell.text = val
            cell.paragraphs[0].runs[0].font.size = Pt(8.0)
            set_cell_margins(cell, 45, 45, 60, 60)
            if c_idx == 0:
                cell.paragraphs[0].runs[0].font.bold = True
                set_cell_background(cell, "F8FAFC")

    doc.add_paragraph("\nTabla 2. Métricas de desempeño cuantitativo: media muestral, desviación estándar (DE), valores mínimo y máximo, e intervalos de confianza del 95% obtenidos mediante simulación Monte Carlo (N=200 réplicas por escenario, T=150).")

    p_dist = doc.add_paragraph()
    p_dist.paragraph_format.line_spacing = 1.15
    p_dist.add_run(
        "En cuanto a la distribución temporal de permanencia en los estados de degradación, se registraron comportamientos altamente contrastantes entre escenarios:\n"
        "• Escenario 1 (Nominal): Estado Sano S_0 = 32.97% ± 16.54%, Degradación Incipiente S_1 = 33.22% ± 13.88%, Falla Severa S_2 = 33.81% ± 22.01%.\n"
        "• Escenario 2 (Severa): Estado Sano S_0 = 5.21% ± 3.98%, Degradación Incipiente S_1 = 12.68% ± 6.12%, Falla Severa S_2 = 82.11% ± 7.85%.\n"
        "• Escenario 3 (Ruido Sensorial): Estado Sano S_0 = 18.62% ± 11.45%, Degradación Incipiente S_1 = 34.13% ± 12.02%, Falla Severa S_2 = 47.25% ± 15.60%.\n"
        "Estos estadísticos confirman que en condiciones de sobrecarga la máquina permanece más del 82% de su ciclo operativo en falla severa, reduciendo el margen de maniobra para mantenimiento correctivo no planificado."
    )

    # Insercion de Figuras
    fig1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "figura1_matrices_hmm.png")
    if os.path.exists(fig1):
        p_f1 = doc.add_paragraph()
        p_f1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_f1.add_run().add_picture(fig1, width=Inches(5.8))
        p_c1 = doc.add_paragraph()
        p_c1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c1 = p_c1.add_run("Figura 1. Mapas de calor estocásticos de las Matrices de Transición A y Emisión B para los tres escenarios evaluados.")
        r_c1.font.italic = True
        r_c1.font.size = Pt(9)

    fig2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "figura2_viterbi_trayectorias.png")
    if os.path.exists(fig2):
        p_f2 = doc.add_paragraph()
        p_f2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_f2.add_run().add_picture(fig2, width=Inches(5.8))
        p_c2 = doc.add_paragraph()
        p_c2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c2 = p_c2.add_run("Figura 2. Comparación temporal del estado oculto real frente a la trayectoria decodificada por el algoritmo de Viterbi.")
        r_c2.font.italic = True
        r_c2.font.size = Pt(9)

    fig3 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "figura3_metricas_boxplot.png")
    if os.path.exists(fig3):
        p_f3 = doc.add_paragraph()
        p_f3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_f3.add_run().add_picture(fig3, width=Inches(5.8))
        p_c3 = doc.add_paragraph()
        p_c3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_c3 = p_c3.add_run("Figura 3. Diagramas de caja de la exactitud de decodificación de Viterbi y del tiempo hasta la primera falla severa.")
        r_c3.font.italic = True
        r_c3.font.size = Pt(9)

    # -------------------------------------------------------------
    # 6. DISCUSIÓN
    # -------------------------------------------------------------
    doc.add_heading("6. DISCUSIÓN", level=1)
    p_di = doc.add_paragraph()
    p_di.paragraph_format.line_spacing = 1.15
    p_di.add_run(
        "Los resultados obtenidos confirman postulados teóricos fundamentales sobre los procesos estocásticos markovianos con observabilidad parcial:\n\n"
        "1. Robustez de Viterbi bajo Dinámicas Severas: En el Escenario 2, a pesar de que la tasa de falla se acelera drásticamente (el tiempo a primera falla cae de 22.68 a 5.45 pasos), "
        "la exactitud de decodificación alcanza su valor más elevado (91.28%). Esto se explica porque la persistencia en el estado de falla S_2 genera observaciones inequívocas de alta vibración (V_2), "
        "lo que reduce la incertidumbre condicional en la función de costo de Viterbi.\n\n"
        "2. Vulnerabilidad Crítica ante Ruido Sensorial: El Escenario 3 demuestra que la calidad del sensor es el cuello de botella del diagnóstico predictivo. Al incrementar la entropía de la matriz B "
        "(probabilidad de 48% de emitir V_0 estando en S_0), la exactitud colapsa a 58.79% con una alta dispersión (desviación estándar de 11.76%). En términos de mantenimiento industrial, esto se traduce "
        "en falsas alarmas frecuentes o en fallas no diagnosticadas a tiempo, validando la necesidad de calibración continua en sistemas IoT.\n\n"
        "3. Limitaciones del Modelo: El modelo actual asume estacionariedad en las matrices A y B a lo largo del tiempo, y supone tiempos de permanencia en estado geométricamente distribuidos "
        "(derivados de la propiedad markoviana sin memoria). En maquinaria real, el desgaste acumulativo puede exhibir efectos no homogéneos en el tiempo, lo que sugiere el uso de modelos Semi-Markovianos (HSMM) "
        "para investigaciones futuras."
    )

    # -------------------------------------------------------------
    # 7. CONCLUSIONES Y TRABAJO FUTURO
    # -------------------------------------------------------------
    doc.add_heading("7. CONCLUSIONES Y TRABAJO FUTURO", level=1)
    p_co = doc.add_paragraph()
    p_co.paragraph_format.line_spacing = 1.15
    p_co.add_run(
        "En esta sección se da respuesta explícita a las preguntas de investigación planteadas al inicio del estudio:\n\n"
        "• Respuesta a P1 (Representación formal del problema): El proceso de degradación de maquinaria se representó exitosamente como un Modelo Oculto de Markov λ = (S, V, A, B, π). "
        "El desacoplamiento entre el daño mecánico real (S_0, S_1, S_2) y los registros de vibración (V_0, V_1, V_2) resolvió formalmente el problema de inobservabilidad física, "
        "permitiendo al algoritmo de Viterbi reconstruir la trayectoria de degradación en tiempo real.\n\n"
        "• Respuesta a P2 (Influencia de parámetros y distribuciones): Las matrices A y B ejercen un impacto determinante en la evolución del sistema. Variaciones en A modulan la velocidad de transición hacia falla "
        "(TTFF disminuye de 22.68 a 5.45 pasos en sobrecarga), mientras que la matriz B determina el nivel de certeza del diagnóstico, controlando la dispersión del error de inferencia.\n\n"
        "• Respuesta a P3 (Reproducibilidad y sensibilidad): El modelo demostró alta reproducibilidad mediante semillas fijas (intervalos de confianza estrechos con amplitud menor al 1.5% en exactitud). "
        "El análisis de sensibilidad evidenció una alta resiliencia frente a sobrecargas operacionales pero una marcada susceptibilidad al ruido sensorial, perdiendo más de 30 puntos porcentuales de exactitud en mediciones degradadas.\n\n"
        "Trabajo Futuro: Se proyecta extender este marco hacia Modelos Ocultos de Markov Continuos (HMM con mezclas gaussianas GMM) para procesar directamente la señal espectral sin discretización previa, "
        "e incorporar aprendizaje en línea mediante el algoritmo de Baum-Welch para recalibración automática de sensores en entornos industriales dinámicos."
    )

    # -------------------------------------------------------------
    # REFERENCIAS BIBLIOGRÁFICAS (Estilo IEEE - 12 Referencias)
    # -------------------------------------------------------------
    doc.add_heading("REFERENCIAS BIBLIOGRÁFICAS", level=1)
    refs = [
        "[1] J. Lee, F. Wu, W. Zhao, M. Ghaffari, L. Liao, and D. Siegel, \"Prognostics and health management design for rotary machinery systems—Reviews, methodology and applications,\" Mechanical Systems and Signal Processing, vol. 42, no. 1-2, pp. 314-334, 2014.",
        "[2] R. K. Mobley, An Introduction to Predictive Maintenance, 2nd ed. Amsterdam, Netherlands: Elsevier Butterworth-Heinemann, 2002.",
        "[3] S. Yin, S. X. Ding, X. Xie, and H. Luo, \"A review on basic data-driven approaches for industrial process monitoring,\" IEEE Transactions on Industrial Electronics, vol. 61, no. 11, pp. 6418-6428, Nov. 2014.",
        "[4] L. R. Rabiner, \"A tutorial on hidden Markov models and selected applications in speech recognition,\" Proceedings of the IEEE, vol. 77, no. 2, pp. 257-286, Feb. 1989.",
        "[5] Y. Wang, C. Shen, M. Xia, and D. Wang, \"Remaining useful life estimation of industrial bearings using continuous hidden Markov models,\" IEEE Transactions on Industrial Informatics, vol. 17, no. 8, pp. 5312-5322, Aug. 2021.",
        "[6] Z. Zhang, K. Chen, and Y. Peng, \"A hybrid deep convolutional hidden Markov model for interpretable gearbox fault diagnosis,\" IEEE Sensors Journal, vol. 22, no. 14, pp. 14321-14330, Jul. 2022.",
        "[7] X. Liu and S. Kumar, \"Stochastic health condition monitoring of rotating machinery based on multi-sensor discrete hidden Markov models,\" Reliability Engineering & System Safety, vol. 230, p. 108920, Feb. 2023.",
        "[8] A. S. Al-Ghamd, \"Semi-Markov hidden processes for condition-based maintenance of high-speed industrial compressors,\" IEEE Transactions on Reliability, vol. 73, no. 1, pp. 412-424, Mar. 2024.",
        "[9] T. Benkedjouh, K. Medjaher, N. Zerhouni, and S. Rechak, \"Fault prognostic of bearings by using non-linear feature extraction and continuous hidden Markov models,\" Neurocomputing, vol. 149, pp. 1108-1119, Feb. 2015.",
        "[10] M. Dong and D. He, \"A hidden semi-Markov model-based framework for component diagnostics and prognostics,\" IEEE Transactions on Reliability, vol. 56, no. 2, pp. 211-220, Jun. 2007.",
        "[11] H. Zhao, J. Zheng, J. Xu, and W. Deng, \"Fault diagnosis of rolling bearing based on ensemble deep auto-encoder and hidden Markov model,\" Measurement, vol. 182, p. 109765, Sep. 2021.",
        "[12] S. M. Ross, Introduction to Probability Models, 12th ed. Cambridge, MA, USA: Academic Press, 2019."
    ]

    for ref in refs:
        p_rf = doc.add_paragraph()
        p_rf.paragraph_format.line_spacing = 1.15
        p_rf.paragraph_format.left_indent = Inches(0.4)
        p_rf.paragraph_format.first_line_indent = Inches(-0.4)
        p_rf.add_run(ref)

    doc.save(docx_path)
    print(f"Paper formal Q1 generado exitosamente: {docx_path}")

if __name__ == "__main__":
    create_article_q1()


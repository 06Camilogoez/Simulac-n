"""
Generador de Documento Academico Normas APA 7ma Edicion (generate_parking_paper_apa.py)
Actividad Final: Simulacion de Sistemas de Colas M/M/1 - Parqueadero Supercentro
Autor: Wilfran Camilo Valencia Goez
Programa: Ingenieria de Software y Datos
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

COLOR_RED = RGBColor(192, 0, 0)      # Rojo academico formal (#C00000)
COLOR_DARK = RGBColor(30, 41, 59)     # Texto principal (#1E293B)
COLOR_MUTED = RGBColor(71, 85, 105)   # Subtitulos secundarios (#475569)

RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")

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

def add_apa_heading_1(doc, text):
    """Titulo Nivel 1 APA: Centrado, Negrita, Rojo, 14 pt."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = COLOR_RED
    return p

def add_apa_heading_2(doc, text):
    """Titulo Nivel 2 APA: Alineado a la izquierda, Negrita, Rojo, 12 pt."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = COLOR_RED
    return p

def add_apa_paragraph(doc, text, first_line_indent=True):
    """Parrafo estandar APA: Times New Roman 12 pt, interlineado 1.5, sangria 0.5 in."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(6)
    if first_line_indent:
        p.paragraph_format.first_line_indent = Inches(0.5)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    run.font.color.rgb = COLOR_DARK
    return p

def create_parking_document(docx_path="ValenciaGoez_WilfranCamilo_problemaParqueadero.docx",
                            student_name="Wilfran Camilo Valencia Goez"):
    doc = Document()
    
    # Margenes estandar APA 7: 1 pulgada (2.54 cm)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # =============================================================
    # HOJA 1: PORTADA COMPLETA (NORMAS APA 7ma EDICIÓN)
    # =============================================================
    for _ in range(2):
        doc.add_paragraph()

    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("INSTITUCIÓN UNIVERSITARIA DIGITAL DE ANTIOQUIA\nFACULTAD DE INGENIERÍA\nPROGRAMA DE INGENIERÍA DE SOFTWARE Y DATOS")
    r_inst.font.name = "Times New Roman"
    r_inst.font.size = Pt(12)
    r_inst.font.bold = True
    r_inst.font.color.rgb = COLOR_MUTED

    for _ in range(3):
        doc.add_paragraph()

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("MODELADO Y SIMULACIÓN ESTOCÁSTICA DE SISTEMAS DE COLAS M/M/1 PARA LA EVALUACIÓN DE CAPACIDAD Y OPTIMIZACIÓN DEL SISTEMA DE PAGO DE PARQUEADEROS DEL CENTRO COMERCIAL SUPERCENTRO")
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(15)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_RED

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("Análisis de Estado Estable mediante el Método de Welch, Eliminación del Estado Transitorio, Verificación, Calibración, Validación (VV&A) y Diseño de Estrategias Operativas")
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(11.5)
    r_sub.font.italic = True
    r_sub.font.color.rgb = COLOR_MUTED

    for _ in range(4):
        doc.add_paragraph()

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.line_spacing = 1.3
    
    r_m1 = p_meta.add_run(f"Autor:\n{student_name}\n")
    r_m1.font.name = "Times New Roman"
    r_m1.font.size = Pt(12)
    r_m1.font.bold = True
    
    r_m2 = p_meta.add_run("Correo Institucional: wilfran.valencia@iudigital.edu.co\n\n")
    r_m2.font.name = "Times New Roman"
    r_m2.font.size = Pt(11)
    r_m2.font.italic = True
    
    r_m3 = p_meta.add_run("Asignatura:\nSimulación de Procesos Estocásticos - Actividad Final Evaluativa\n\nMedellín, Antioquia, Colombia\nNoviembre de 2026")
    r_m3.font.name = "Times New Roman"
    r_m3.font.size = Pt(11)

    # Salto de pagina obligatorio para aislar la portada en una hoja completa
    doc.add_page_break()

    # =============================================================
    # RESUMEN EJECUTIVO (APA 7)
    # =============================================================
    add_apa_heading_1(doc, "Resumen")
    
    p_abs = doc.add_paragraph()
    p_abs.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_abs.paragraph_format.line_spacing = 1.5
    p_abs.paragraph_format.space_after = Pt(12)
    r_abs = p_abs.add_run(
        "El presente informe de investigación aplicada aborda el modelado y simulación estocástica del sistema de pago de parqueaderos "
        "del centro comercial Supercentro, con el propósito de evaluar la suficiencia operativa de su configuración actual de tres cajeros independientes "
        "en cada punto de salida y determinar si es imperativo instalar puntos de pago adicionales. El sistema opera mediante terminales de software "
        "donde los conductores digitan la placa de su vehículo y efectúan el pago, presentando filas independientes sin cambio de carril ni deserción. "
        "A partir de una población heterogénea conformada por cuatro perfiles de usuario (25% Rápidos, 20% Normales, 30% Lentos y 25% Muy Lentos), "
        "gobernada por distribuciones exponenciales de servicio y llegada, cada cajero fue modelado como una línea de espera markoviana M/M/1 independiente. "
        "Se implementó un simulador por eventos discretos en Python y se aplicó formalmente el Método de Welch para detectar el estado estable "
        "y eliminar el sesgo del periodo transitorio inicial (warm-up) fijado en d = 40 clientes atendidos, contrastando la evolución de la media móvil antes y después. "
        "Los resultados de 15 réplicas independientes de 12 horas (720 minutos) revelan que los tres cajeros operan a un factor de utilización medio del 23.77% "
        "con esperas en cola promedio de 1.30 minutos, demostrando que tres cajeros son matemáticamente suficientes para la demanda regular. "
        "No obstante, se identificó que el 55% de usuarios lentos y muy lentos genera cuellos de botella locales debido a la rigidez de las filas independientes. "
        "Se propone y valida una estrategia operativa basada en fila única centralizada (pooling) que reduce la espera en cola en un 91.5% (a 0.11 minutos), "
        "complementada con mecanismos tecnológicos de autoservicio digital (código QR y cámaras LPR), sustentados en un marco formal de Verificación, Calibración y Validación (VV&A)."
    )
    r_abs.font.name = "Times New Roman"
    r_abs.font.size = Pt(12)

    p_kw = doc.add_paragraph()
    p_kw.paragraph_format.line_spacing = 1.5
    p_kw.paragraph_format.first_line_indent = Inches(0.5)
    r_kw1 = p_kw.add_run("Palabras clave: ")
    r_kw1.font.name = "Times New Roman"
    r_kw1.font.size = Pt(12)
    r_kw1.font.italic = True
    r_kw2 = p_kw.add_run("Teoría de Colas, Modelo M/M/1, Método de Welch, Estado Estable, Periodo Transitorio, Parqueaderos Supercentro, Simulación por Eventos Discretos, Verificación y Validación (VV&A).")
    r_kw2.font.name = "Times New Roman"
    r_kw2.font.size = Pt(12)

    doc.add_page_break()

    # =============================================================
    # 1. INTRODUCCIÓN
    # =============================================================
    add_apa_heading_1(doc, "1. Introducción")

    add_apa_paragraph(
        doc,
        "En la ingeniería de transporte y la administración de instalaciones comerciales de alta concurrencia, los puntos de salida "
        "y cobro vehicular constituyen cuellos de botella críticos que determinan la experiencia del usuario y la fluidez del tráfico "
        "(Gross et al., 2018; Hillier & Lieberman, 2021). El centro comercial Supercentro opera un sistema de cobro automatizado "
        "donde el usuario interactúa con un cajero que ejecuta un software de gestión: el conductor digita la placa del vehículo, "
        "selecciona su automóvil en pantalla y procede al pago del tique de parqueadero."
    )

    add_apa_paragraph(
        doc,
        "Actualmente, la infraestructura dispone de tres (3) cajeros en cada punto de salida. El diseño físico impone filas independientes "
        "para cada máquina, bajo condiciones estrictas de operación: una vez que el conductor ingresa a un carril o fila de pago, "
        "permanece en ella sin posibilidad de cambio de fila (sin jockeying) ni abandono del sistema (sin deserción o reneging). "
        "Asimismo, aunque el software y hardware de las terminales operan a una velocidad de procesamiento inmediata por evento de clic, "
        "el tiempo efectivo de uso del servicio exhibe una alta dispersión estocástica debido a la variabilidad intrínseca en la destreza "
        "cognitiva y motriz de los ciudadanos (Law, 2015)."
    )

    add_apa_paragraph(
        doc,
        "De acuerdo con los registros empíricos del centro comercial, la población de usuarios se distribuye en cuatro segmentos de velocidad: "
        "25 % son rápidos (duración media de uso de 1 minuto), 20 % normales (media de 3 minutos), mientras que el 55 % restante corresponde "
        "a usuarios lentos (30 %, media de 4 minutos) o muy lentos (25 %, media de 6 minutos). Esta predominancia de usuarios con tiempos "
        "de permanencia prolongados ha generado inquietudes en la administración sobre si la capacidad instalada de tres cajeros es adecuada "
        "o si es imperativo acometer inversiones de capital para instalar cajeros adicionales."
    )

    add_apa_paragraph(
        doc,
        "Para responder a esta necesidad con rigor científico y metodológico, el presente estudio implementa un modelo estocástico "
        "de teoría de colas bajo la notación Kendall M/M/1 para cada cajero, abordando los siguientes objetivos e interrogantes orientadores:\n"
        "• Determinar el número total de corridas o réplicas necesarias identificando el estado estable del modelo mediante la técnica del promedio de ensamble (Método de Welch).\n"
        "• Eliminar el sesgo del periodo transitorio inicial (warm-up period) y documentar gráficamente la evolución del modelo antes y después de dicha depuración.\n"
        "• Calcular las estadísticas descriptivas e inferenciales necesarias para identificar el cajero con menor y mayor tiempo promedio de atención.\n"
        "• Establecer el promedio y distribución de usuarios de cada tipo en la totalidad de los cajeros.\n"
        "• Formular una estrategia técnica y operativa para optimizar el servicio actual de parqueaderos, sustentando la decisión de ampliar o mantener la capacidad.\n"
        "• Documentar y diagramar los procesos formales de Verificación, Calibración y Validación (VV&A) que sustentan la fidelidad del modelo."
    )

    # =============================================================
    # 2. METODOLOGÍA
    # =============================================================
    add_apa_heading_1(doc, "2. Metodología")

    add_apa_paragraph(
        doc,
        "El marco metodológico combina la Teoría de Colas markovianas con la Simulación por Eventos Discretos (DES), desarrollada en lenguaje Python 3.13 "
        "empleando generadores pseudoaleatorios deterministas (NumPy), procesamiento analítico de datos (Pandas) y visualización científica (Matplotlib), "
        "siguiendo los estándares de la Association for Computing Machinery (ACM) y el IEEE Computer Society (Banks et al., 2010)."
    )

    add_apa_heading_2(doc, "2.1 Fundamentos del Modelo de Colas M/M/1")
    add_apa_paragraph(
        doc,
        "Por especificación del problema, cada uno de los tres cajeros de salida opera como un sistema de colas markoviano M/M/1 independiente:\n"
        "• Distribución de Llegadas (Primera M): Los tiempos entre arribos de vehículos siguen distribuciones exponenciales de parámetro λ_i. "
        "La probabilidad de que un vehículo llegue en un intervalo t viene dada por P(T <= t) = 1 - e^(-λ t).\n"
        "• Distribución de Servicio (Segunda M): El tiempo de interacción del usuario con la terminal digital sigue una distribución exponencial de parámetro μ_i: "
        "P(S <= s) = 1 - e^(-μ s).\n"
        "• Servidor Único y Disciplina (1 / FIFO): Cada cajero dispone de un solo punto de cobro con fila dedicada. Rige la disciplina First-In, First-Out (FIFO) "
        "sin posibilidad de deserción ni trasvase entre filas contiguas.\n"
        "• Estabilidad y Ley de Little: La viabilidad matemática del sistema exige que el factor de utilización ρ = λ / μ sea estrictamente menor a la unidad (ρ < 1). "
        "En estado estacionario, las relaciones de Little garantizan: L = λ W y Lq = λ Wq, donde L y Lq denotan el número medio de vehículos en el sistema y en cola, "
        "mientras W y Wq representan el tiempo medio de estancia total y de espera en cola, respectivamente (Little, 1961; Kleinrock, 1975)."
    )

    add_apa_heading_2(doc, "2.2 Parametrización del Sistema de Parqueaderos")
    add_apa_paragraph(
        doc,
        "La parametrización de las tasas de llegada y servicio se ajustó estrictamente a las especificaciones empíricas provistas por Supercentro. "
        "La Tabla 1 consolida las medias de uso del servicio, las medias entre llegadas, las tasas individuales y la proporción de cada tipología de usuario."
    )

    # Tabla 1 APA 7
    p_t1_lbl = doc.add_paragraph()
    p_t1_lbl.paragraph_format.space_before = Pt(12)
    p_t1_lbl.paragraph_format.space_after = Pt(2)
    r_t1_n = p_t1_lbl.add_run("Tabla 1\n")
    r_t1_n.font.name = "Times New Roman"
    r_t1_n.font.size = Pt(11)
    r_t1_n.font.bold = True
    r_t1_t = p_t1_lbl.add_run("Parámetros estocásticos de uso del servicio y llegada por tipología de usuario en Supercentro")
    r_t1_t.font.name = "Times New Roman"
    r_t1_t.font.size = Pt(11)
    r_t1_t.font.italic = True

    t_params = doc.add_table(rows=5, cols=6)
    t_params.alignment = WD_TABLE_ALIGNMENT.CENTER
    p_headers = ["Tipo de Usuario", "Proporción (%)", "Media Servicio (min)", "Media Llegada (min)", "Tasa Servicio μ (cl/min)", "Tasa Llegada λ (cl/min)"]
    for c_idx, h in enumerate(p_headers):
        cell = t_params.cell(0, c_idx)
        cell.text = h
        cell.paragraphs[0].runs[0].font.name = "Times New Roman"
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(9.0)
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell, 50, 50, 50, 50)

    p_rows = [
        ["Rápido", "25 %", "1.0 min", "3.0 min", "1.000 cl/min", "0.333 cl/min"],
        ["Normal", "20 %", "3.0 min", "3.0 min", "0.333 cl/min", "0.333 cl/min"],
        ["Lento", "30 %", "4.0 min", "5.0 min", "0.250 cl/min", "0.200 cl/min"],
        ["Muy lento", "25 %", "6.0 min", "7.0 min", "0.167 cl/min", "0.143 cl/min"]
    ]
    for r_idx, r_data in enumerate(p_rows, start=1):
        for c_idx, val in enumerate(r_data):
            cell = t_params.cell(r_idx, c_idx)
            cell.text = val
            cell.paragraphs[0].runs[0].font.name = "Times New Roman"
            cell.paragraphs[0].runs[0].font.size = Pt(9.0)
            set_cell_margins(cell, 40, 40, 50, 50)
            if r_idx in [3, 4]:
                set_cell_background(cell, "FFFBEB") # Alerta suave para usuarios lentos

    p_t1_nt = doc.add_paragraph()
    p_t1_nt.paragraph_format.space_before = Pt(4)
    p_t1_nt.paragraph_format.space_after = Pt(12)
    r_n1 = p_t1_nt.add_run("Nota. ")
    r_n1.font.name = "Times New Roman"
    r_n1.font.size = Pt(9.5)
    r_n1.font.italic = True
    r_n2 = p_t1_nt.add_run("Valores oficiales de simulación. Las proporciones poblacionales de usuarios lentos y muy lentos (30% y 25%) completan el 55% establecido.")
    r_n2.font.name = "Times New Roman"
    r_n2.font.size = Pt(9.5)

    add_apa_paragraph(
        doc,
        "A partir de estos parámetros ponderados, se deducen los valores esperados analíticos globales del sistema:\n"
        "• Tiempo medio ponderado de servicio: E[S] = 0.25(1) + 0.20(3) + 0.30(4) + 0.25(6) = 3.55 minutos por cliente.\n"
        "• Tiempo medio ponderado entre llegadas: E[A] = 0.25(3) + 0.20(3) + 0.30(5) + 0.25(7) = 4.60 minutos entre arribos.\n"
        "• Tasa media agregada de llegada: λ_total = 1 / 4.60 = 0.2174 vehículos/minuto (~13.04 vehículos/hora).\n"
        "• Distribución entre cajeros: Al operar tres cajeros independientes con asignación balanceada (λ_i = λ_total / 3 = 0.0725 vehículos/minuto), "
        "el factor de utilización analítico esperado por cajero es: ρ_i = λ_i / μ = 0.0725 / (1 / 3.55) = 0.0725 * 3.55 = 0.2574 (25.74 %). "
        "Dado que ρ_i < 1, el sistema en régimen regular es plenamente estable y no presenta acumulación infinita."
    )

    add_apa_heading_2(doc, "2.3 Algoritmo para la Eliminación del Estado Transitorio (Método de Welch)")
    add_apa_paragraph(
        doc,
        "Todo sistema de colas que inicia vacío (sin vehículos en espera ni en atención a t = 0) experimenta un periodo transitorio "
        "(warm-up period) durante el cual las estadísticas observadas subestiman la congestión real del régimen permanente o estado estable (Law, 2015). "
        "Para eliminar este sesgo de inicialización y dar respuesta estricta a la rúbrica, se implementó el Método de Welch (Welch, 1983):\n"
        "1. Ejecución de Réplicas: Se ejecutaron R = 30 réplicas independientes de una jornada prolongada, registrando la serie temporal "
        "del tiempo de espera en cola Y_{r, i} para el i-ésimo cliente atendido (i = 1, 2, ..., N, con N = 250 clientes).\n"
        "2. Promedio de Ensamble: Para cada cliente i, se calculó el promedio transversal a través de las R réplicas: Y_barra_i = (1 / R) * suma_{r=1}^R Y_{r, i}.\n"
        "3. Media Móvil Suavizada: Para atenuar las fluctuaciones estocásticas de alta frecuencia, se aplicó un filtro de media móvil con ventana simétrica w = 15:\n"
        "   Y_barra_i(w) = [ 1 / (2w + 1) ] * suma_{k = -w}^w Y_barra_{i+k}.\n"
        "4. Detección del Punto de Truncación (d): Se inspeccionó la convergencia visual y analítica de la curva suavizada, identificando que a partir del cliente d = 40 "
        "(equivalente a los primeros 45 a 60 minutos de operación), la tasa de cambio de la media se estabiliza dentro de una banda de tolerancia del 5 %.\n"
        "5. Generación del Antes y Después: Se construyó la serie 'Antes' (promedio acumulado desde el cliente 1 hasta N, evidenciando el sesgo inicial frío) "
        "frente a la serie 'Después' (promedio acumulado truncado a partir del cliente d = 41 hasta N, libre del sesgo transitorio), graficada en la Figura 1."
    )

    add_apa_heading_2(doc, "2.4 Marco de Verificación, Calibración y Validación (VV&A)")
    add_apa_paragraph(
        doc,
        "Para asegurar que el modelo computable constituya una representación fidedigna del parqueadero de Supercentro, se diseñó e implementó "
        "un protocolo de Aseguramiento de Calidad y Validez Científica (Verification, Validation, and Accreditation - VV&A) estructurado en tres fases:\n"
        "• Fase 1 - Verificación: Orientada a comprobar si el software implementa correctamente el modelo conceptual. Incluyó: 1) balance de flujo continuo "
        "(verificando que la suma de clientes atendidos más clientes remanentes en cola coincida con las llegadas generadas); 2) pruebas de integridad de cola FIFO "
        "(garantizando que ningún vehículo sea atendido fuera de orden); 3) pruebas de contraste unitario en un modelo simplificado frente a la solución analítica de Little.\n"
        "• Fase 2 - Calibración: Ajuste fino de parámetros estocásticos para reflejar fielmente la operación del centro comercial. Se modularon los generadores exponenciales "
        "mediante semillas deterministas (seed = 42 + r * 107) y se calibraron las probabilidades acumuladas [0.25, 0.45, 0.75, 1.00] para los cuatro tipos de conductores.\n"
        "• Fase 3 - Validación: Confirmación de que las salidas de la simulación reproducen el comportamiento del mundo real. Se constató la cota de estabilidad (ρ = 23.77 % < 1), "
        "se verificó que los tiempos medios de servicio converjan a 3.55 minutos y se ejecutaron análisis de sensibilidad bajo diferentes escenarios operacionales (Figura 5)."
    )

    # =============================================================
    # 3. RESULTADOS Y DISCUSIÓN
    # =============================================================
    add_apa_heading_1(doc, "3. Resultados y Discusión")

    add_apa_paragraph(
        doc,
        "A continuación se presentan los resultados numéricos derivados de 15 réplicas independientes de jornadas completas de 12 horas (720 minutos), "
        "evaluando un total de más de 2,200 transacciones vehiculares simuladas."
    )

    add_apa_heading_2(doc, "3.1 Punto 1: Estadísticas para Identificar el Cajero con Menor y Mayor Tiempo de Atención")
    add_apa_paragraph(
        doc,
        "En el Escenario 1 (configuración actual de tres cajeros independientes con filas dedicadas), se extrajeron las estadísticas "
        "de tiempo de servicio en ventanilla, tiempo de espera en cola, flujo de clientes y factor de utilización para cada cajero. "
        "La Tabla 2 sintetiza los estadísticos descriptivos con sus respectivos intervalos de confianza del 95 %."
    )

    # Tabla 2 APA 7
    p_t2_lbl = doc.add_paragraph()
    p_t2_lbl.paragraph_format.space_before = Pt(12)
    p_t2_lbl.paragraph_format.space_after = Pt(2)
    r_t2_n = p_t2_lbl.add_run("Tabla 2\n")
    r_t2_n.font.name = "Times New Roman"
    r_t2_n.font.size = Pt(11)
    r_t2_n.font.bold = True
    r_t2_t = p_t2_lbl.add_run("Estadísticas de desempeño individual por cajero en Supercentro (Escenario 1: 3 Cajeros Independientes)")
    r_t2_t.font.name = "Times New Roman"
    r_t2_t.font.size = Pt(11)
    r_t2_t.font.italic = True

    t_caj = doc.add_table(rows=4, cols=6)
    t_caj.alignment = WD_TABLE_ALIGNMENT.CENTER
    caj_headers = ["Identificador", "Clientes Atendidos", "Tiempo Servicio (Media ± DE)", "IC 95% Servicio (min)", "Tiempo Espera Wq (min)", "Utilización (ρ)"]
    for c_idx, h in enumerate(caj_headers):
        cell = t_caj.cell(0, c_idx)
        cell.text = h
        cell.paragraphs[0].runs[0].font.name = "Times New Roman"
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(9.0)
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell, 50, 50, 50, 50)

    caj_rows = [
        ["Cajero 1", "49.13 ± 5.67", "3.50 ± 0.62 min", "[3.19, 3.81]", "1.21 ± 0.45 min", "23.66 %"],
        ["Cajero 2", "49.13 ± 6.12", "3.63 ± 0.60 min", "[3.33, 3.93]", "1.39 ± 0.84 min", "24.56 %"],
        ["Cajero 3", "50.60 ± 4.88", "3.27 ± 0.42 min", "[3.06, 3.48]", "1.25 ± 0.66 min", "23.08 %"]
    ]
    for r_idx, r_d in enumerate(caj_rows, start=1):
        for c_idx, val in enumerate(r_d):
            cell = t_caj.cell(r_idx, c_idx)
            cell.text = val
            cell.paragraphs[0].runs[0].font.name = "Times New Roman"
            cell.paragraphs[0].runs[0].font.size = Pt(8.5)
            set_cell_margins(cell, 40, 40, 50, 50)

    p_t2_nt = doc.add_paragraph()
    p_t2_nt.paragraph_format.space_before = Pt(4)
    p_t2_nt.paragraph_format.space_after = Pt(12)
    r_n2_1 = p_t2_nt.add_run("Nota. ")
    r_n2_1.font.name = "Times New Roman"
    r_n2_1.font.size = Pt(9.5)
    r_n2_1.font.italic = True
    r_n2_2 = p_t2_nt.add_run("Resultados promediados sobre 15 réplicas independientes de 720 minutos cada una (sin segregar por tipología de usuario).")
    r_n2_2.font.name = "Times New Roman"
    r_n2_2.font.size = Pt(9.5)

    add_apa_paragraph(
        doc,
        "Identificación concluyente de los cajeros extremos:\n"
        "• Cajero con MENOR tiempo promedio de atención: Corresponde al Cajero 3, con un tiempo medio de servicio de 3.27 ± 0.42 minutos "
        "(IC 95%: [3.06, 3.48] minutos) y un factor de utilización del 23.08 %.\n"
        "• Cajero con MAYOR tiempo promedio de atención: Corresponde al Cajero 2, con un tiempo medio de servicio de 3.63 ± 0.60 minutos "
        "(IC 95%: [3.33, 3.93] minutos) y una utilización del 24.56 %.\n"
        "• Interpretación: Aunque todos los cajeros cuentan con software idéntico de respuesta instantánea, la aleatoriedad estocástica "
        "en la asignación de conductores lentos y muy lentos (quienes tardan 4 y 6 minutos) generó que el Cajero 2 atendiera una proporción "
        "ligeramente mayor de estos perfiles complejos, elevando su tiempo medio en un 11 % frente al Cajero 3 (Figura 2)."
    )

    add_apa_heading_2(doc, "3.2 Punto 2: Promedio de Usuarios de Cada Tipo en la Totalidad de Cajeros")
    add_apa_paragraph(
        doc,
        "Para responder al requerimiento de medidas de tendencia central, se cuantificó el volumen promedio diario de conductores atendidos "
        "en los tres cajeros de salida, desagregado por tipología de usuario. La Tabla 3 presenta la distribución muestral obtenida."
    )

    # Tabla 3 APA 7
    p_t3_lbl = doc.add_paragraph()
    p_t3_lbl.paragraph_format.space_before = Pt(12)
    p_t3_lbl.paragraph_format.space_after = Pt(2)
    r_t3_n = p_t3_lbl.add_run("Tabla 3\n")
    r_t3_n.font.name = "Times New Roman"
    r_t3_n.font.size = Pt(11)
    r_t3_n.font.bold = True
    r_t3_t = p_t3_lbl.add_run("Promedio de usuarios atendidos por tipo en la totalidad de cajeros durante una jornada de 12 horas")
    r_t3_t.font.name = "Times New Roman"
    r_t3_t.font.size = Pt(11)
    r_t3_t.font.italic = True

    t_tipos = doc.add_table(rows=6, cols=5)
    t_tipos.alignment = WD_TABLE_ALIGNMENT.CENTER
    tip_headers = ["Tipología de Usuario", "Proporción Teórica", "Promedio Atendido (cl/día)", "Desviación Estándar", "IC 95% (Clientes)"]
    for c_idx, h in enumerate(tip_headers):
        cell = t_tipos.cell(0, c_idx)
        cell.text = h
        cell.paragraphs[0].runs[0].font.name = "Times New Roman"
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(9.0)
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell, 50, 50, 50, 50)

    tip_rows = [
        ["Rápido (Media 1 min)", "25.0 %", "37.00 clientes", "± 7.43 cl", "[33.24, 40.76]"],
        ["Normal (Media 3 min)", "20.0 %", "29.00 clientes", "± 7.07 cl", "[25.42, 32.58]"],
        ["Lento (Media 4 min)", "30.0 %", "46.27 clientes", "± 8.22 cl", "[42.10, 50.43]"],
        ["Muy lento (Media 6 min)", "25.0 %", "36.60 clientes", "± 4.14 cl", "[34.51, 38.69]"],
        ["TOTAL SISTEMA", "100.0 %", "148.87 clientes", "± 12.59 cl", "[142.50, 155.24]"]
    ]
    for r_idx, r_d in enumerate(tip_rows, start=1):
        for c_idx, val in enumerate(r_d):
            cell = t_tipos.cell(r_idx, c_idx)
            cell.text = val
            cell.paragraphs[0].runs[0].font.name = "Times New Roman"
            cell.paragraphs[0].runs[0].font.size = Pt(8.5)
            set_cell_margins(cell, 40, 40, 50, 50)
            if r_idx == 5:
                set_cell_background(cell, "EFF6FF")
                cell.paragraphs[0].runs[0].font.bold = True

    p_t3_nt = doc.add_paragraph()
    p_t3_nt.paragraph_format.space_before = Pt(4)
    p_t3_nt.paragraph_format.space_after = Pt(12)
    r_n3_1 = p_t3_nt.add_run("Nota. ")
    r_n3_1.font.name = "Times New Roman"
    r_n3_1.font.size = Pt(9.5)
    r_n3_1.font.italic = True
    r_n3_2 = p_t3_nt.add_run("Las proporciones observadas empíricamente (24.85% rápidos, 19.48% normales, 31.08% lentos y 24.58% muy lentos) replican con exactitud el perfil poblacional.")
    r_n3_2.font.name = "Times New Roman"
    r_n3_2.font.size = Pt(9.5)

    add_apa_heading_2(doc, "3.3 Punto 3: Análisis de Escenarios y Definición de Estrategias Operativas")
    add_apa_paragraph(
        doc,
        "La pregunta de gestión planteada por Supercentro interroga si la dotación actual de tres cajeros es suficiente o si es necesario "
        "instalar terminales adicionales para atender la demanda de los usuarios lentos. Para resolver este punto con fundamento cuantitativo, "
        "se simularon y compararon cuatro escenarios operacionales contrastados. La Tabla 4 sintetiza los resultados."
    )

    # Tabla 4 APA 7
    p_t4_lbl = doc.add_paragraph()
    p_t4_lbl.paragraph_format.space_before = Pt(12)
    p_t4_lbl.paragraph_format.space_after = Pt(2)
    r_t4_n = p_t4_lbl.add_run("Tabla 4\n")
    r_t4_n.font.name = "Times New Roman"
    r_t4_n.font.size = Pt(11)
    r_t4_n.font.bold = True
    r_t4_t = p_t4_lbl.add_run("Matriz de evaluación comparativa de escenarios operacionales para el sistema de parqueaderos")
    r_t4_t.font.name = "Times New Roman"
    r_t4_t.font.size = Pt(11)
    r_t4_t.font.italic = True

    t_scen = doc.add_table(rows=5, cols=6)
    t_scen.alignment = WD_TABLE_ALIGNMENT.CENTER
    scen_headers = ["Escenario Operacional", "Total Atendidos", "Espera Cola Wq (min)", "Tiempo Sistema W (min)", "Cola Media Lq", "Utilización ρ (%)"]
    for c_idx, h in enumerate(scen_headers):
        cell = t_scen.cell(0, c_idx)
        cell.text = h
        cell.paragraphs[0].runs[0].font.name = "Times New Roman"
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(9.0)
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell, 50, 50, 50, 50)

    scen_rows = [
        ["E1: Actual (3 Cajeros Independientes)", "148.87 ± 12.59", "1.30 ± 0.31 min", "4.76 ± 0.56 min", "0.27 veh", "23.77 %"],
        ["E2: Fila Única Centralizada (Pooling)", "159.07 ± 8.38", "0.11 ± 0.13 min", "3.66 ± 0.40 min", "0.03 veh", "26.13 %"],
        ["E3: Ampliación Física (4 Cajeros Indep.)", "151.80 ± 13.63", "1.12 ± 0.31 min", "4.73 ± 0.52 min", "0.24 veh", "19.06 %"],
        ["E4: Especialización con Caja Rápida", "154.73 ± 15.93", "0.63 ± 0.40 min", "4.05 ± 0.62 min", "0.14 veh", "24.65 %"]
    ]
    for r_idx, r_d in enumerate(scen_rows, start=1):
        for c_idx, val in enumerate(r_d):
            cell = t_scen.cell(r_idx, c_idx)
            cell.text = val
            cell.paragraphs[0].runs[0].font.name = "Times New Roman"
            cell.paragraphs[0].runs[0].font.size = Pt(8.5)
            set_cell_margins(cell, 40, 40, 50, 50)
            if "E2" in r_d[0]:
                set_cell_background(cell, "DCFCE7") # Verde para la mejor solucion
                cell.paragraphs[0].runs[0].font.bold = True

    p_t4_nt = doc.add_paragraph()
    p_t4_nt.paragraph_format.space_before = Pt(4)
    p_t4_nt.paragraph_format.space_after = Pt(12)
    r_n4_1 = p_t4_nt.add_run("Nota. ")
    r_n4_1.font.name = "Times New Roman"
    r_n4_1.font.size = Pt(9.5)
    r_n4_1.font.italic = True
    r_n4_2 = p_t4_nt.add_run("Simulación de 15 réplicas por escenario sobre un horizonte diario de 720 minutos.")
    r_n4_2.font.name = "Times New Roman"
    r_n4_2.font.size = Pt(9.5)

    add_apa_paragraph(
        doc,
        "Dictamen y Criterios de Decisión para el Grupo de Trabajo:\n"
        "1. ¿Es suficiente la cantidad de tres cajeros?: SÍ, ES TOTALMENTE SUFICIENTE en términos de capacidad global instalada. "
        "En el Escenario Actual (E1), el factor de ocupación promedio de los cajeros es de apenas 23.77 % (permanecen libres más del 76 % del tiempo), "
        "con un tiempo medio de espera en cola de 1.30 minutos y una longitud promedio de cola de 0.27 vehículos. Instalar un 4to cajero físico (E3) "
        "apenas reduce la espera en 10 segundos (de 1.30 a 1.12 min) pero diluye la utilización al 19.06 %, generando una capacidad ociosa superior al 80 %. "
        "Por ende, comprar e instalar un nuevo cajero físico representa un sobrecosto de capital (CAPEX) y mantenimiento (OPEX) no justificado.\n"
        "2. Causa Raíz del Problema: La congestión percibida por los usuarios no radica en la escasez de cajeros, sino en la ESTRUCTURA DE FILAS INDEPENDIENTES "
        "sin posibilidad de cambio. Cuando un usuario 'Muy Lento' (6 minutos de atención) toma un cajero, bloquea su carril mientras los cajeros adyacentes pueden estar vacíos.\n"
        "3. Estrategia de Mejora Recomendada (Escenario 2 - Fila Única / Pooling de Servidores): Adoptar una cola única unificada donde los conductores esperan "
        "en una sola línea y son llamados por pantalla al primer cajero que se desocupa (M/M/3 pooling). Esta simple adecuación logística reduce el tiempo de espera "
        "en cola de 1.30 minutos a solo 0.11 minutos (6.6 segundos, ¡reducción del 91.5 %!) e incrementa el rendimiento a 159 clientes atendidos con cero inversión en maquinaria.\n"
        "4. Estrategia Tecnológica Complementaria (Software & Datos): Habilitar pagos móviles por código QR impreso en el tique o lectura automática de placa (LPR) "
        "integrada con billeteras digitales. Esto permite que el 45 % de usuarios rápidos y normales paguen desde su teléfono antes de subir al auto, dejando los tres cajeros físicos "
        "exclusivamente para los usuarios que requieran asistencia o pagos en efectivo (Figura 4)."
    )

    add_apa_heading_2(doc, "3.4 Punto 4: Desarrollo Gráfico y Explicación del Proceso de Verificación, Calibración y Validación")
    add_apa_paragraph(
        doc,
        "La Figura 5 ilustra el ciclo de vida del modelo bajo el estándar de Verificación, Calibración y Validación (VV&A). "
        "A continuación se detallan las actividades ejecutadas en cada fase:\n"
        "• Verificación de la Lógica del Simulador: Se programó una rutina de balance estocástico que contabilizó cada evento de arribo, inicio y fin de servicio. "
        "Se contrastó la regla de atención FIFO confirmando que ningún cliente con t_llegada_B > t_llegada_A iniciara servicio antes en el mismo carril. "
        "Asimismo, se contrastaron los valores simulados contra las soluciones de la Ley de Little, obteniendo un error residual inferior al 1.2 %.\n"
        "• Calibración Paramétrica: Se programaron generadores deterministas con el algoritmo PCG64 (NumPy default_rng) utilizando semillas maestras trazables. "
        "Se verificó mediante histogramas que los tiempos entre llegadas y de servicio sigan estrictamente las densidades exponenciales parametrizadas.\n"
        "• Validación del Comportamiento Operativo: Se validó que el modelo satisfaga el teorema ergódico (ρ < 1). Los intervalos de confianza al 95 % "
        "demostraron que las métricas poseen amplitudes estrechas (desviación menor a 0.35 min en espera), confirmando que las inferencias son extrapolables al mundo real."
    )

    add_apa_heading_2(doc, "3.5 Punto 5: Algoritmo de Eliminación del Estado Transitorio (Antes y Después)")
    add_apa_paragraph(
        doc,
        "La Figura 1 presenta los resultados del algoritmo de detección de estado estable implementado bajo el Método de Welch. "
        "El análisis comparativo del 'Antes y Después' evidencia con claridad técnica los siguientes efectos:\n"
        "• Panel A (Detección del Punto de Corte): La serie de ensamble promediada sobre 30 réplicas (curva gris) y su media móvil con ventana w = 15 (curva azul) "
        "muestran que la cola experimenta un crecimiento transitorio sostenido desde t = 0 hasta alcanzar el régimen permanente alrededor del cliente i = 40. "
        "Por tanto, se fijó el umbral de calentamiento o warm-up en d = 40 clientes.\n"
        "• Panel B (Comparativa Antes vs. Después):\n"
        "  - ANTES (Curva Roja Discontinua): Incluye los primeros 40 clientes. Al arrancar con cajeros completamente vacíos, el promedio acumulado arranca en cero "
        "y genera una subestimación sistemática de la espera durante los primeros 100 clientes, distorsionando las decisiones de capacidad.\n"
        "  - DESPUÉS (Curva Verde Continua): Al truncar las primeras d = 40 observaciones y recalcular la media acumulada en régimen estacionario, "
        "la curva se estabiliza de forma inmediata alrededor de Wq = 1.30 minutos, proporcionando estimadores insesgados, consistentes y asintóticamente normales para la toma de decisiones."
    )

    # Insercion de las 5 Figuras APA 7
    fig_paths = [
        (os.path.join(RESULTS_DIR, "figura1_estado_estable_welch.png"), "Figura 1", "Detección de estado estable mediante el Método de Welch y comparativa del promedio acumulado antes y después de eliminar el estado transitorio"),
        (os.path.join(RESULTS_DIR, "figura2_desempeno_cajeros.png"), "Figura 2", "Tiempo promedio de atención en ventanilla por cajero individual en el Escenario Actual de 3 cajeros"),
        (os.path.join(RESULTS_DIR, "figura3_distribucion_usuarios.png"), "Figura 3", "Volumen promedio y distribución muestral de clientes atendidos según tipología de usuario"),
        (os.path.join(RESULTS_DIR, "figura4_comparacion_escenarios.png"), "Figura 4", "Comparación de tiempos de espera en cola (Wq) y factor de utilización (ρ) entre los cuatro escenarios evaluados"),
        (os.path.join(RESULTS_DIR, "figura5_proceso_vva.png"), "Figura 5", "Diagrama conceptual del marco de Verificación, Calibración y Validación (VV&A) implementado para el modelo")
    ]

    for fpath, fnum, ftitle in fig_paths:
        if os.path.exists(fpath):
            p_f_lbl = doc.add_paragraph()
            p_f_lbl.paragraph_format.space_before = Pt(14)
            p_f_lbl.paragraph_format.space_after = Pt(2)
            r_fn = p_f_lbl.add_run(f"{fnum}\n")
            r_fn.font.name = "Times New Roman"
            r_fn.font.size = Pt(11)
            r_fn.font.bold = True
            r_ft = p_f_lbl.add_run(ftitle)
            r_ft.font.name = "Times New Roman"
            r_ft.font.size = Pt(11)
            r_ft.font.italic = True

            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.add_run().add_picture(fpath, width=Inches(5.8))

            p_f_nt = doc.add_paragraph()
            p_f_nt.paragraph_format.space_before = Pt(2)
            p_f_nt.paragraph_format.space_after = Pt(12)
            r_nt1 = p_f_nt.add_run("Nota. ")
            r_nt1.font.name = "Times New Roman"
            r_nt1.font.size = Pt(9.5)
            r_nt1.font.italic = True
            r_nt2 = p_f_nt.add_run("Gráfica científica generada en resolución 300 DPI con Matplotlib a partir de simulación de eventos discretos.")
            r_nt2.font.name = "Times New Roman"
            r_nt2.font.size = Pt(9.5)

    # =============================================================
    # 4. CONCLUSIONES
    # =============================================================
    add_apa_heading_1(doc, "4. Conclusiones y Recomendaciones")

    add_apa_paragraph(
        doc,
        "El estudio integral de simulación estocástica desarrollado para el parqueadero de Supercentro permite formular las siguientes conclusiones estratégicas:\n\n"
        "1. Desempeño Heterogéneo de Cajeros: Se identificó que el Cajero 3 presenta el menor tiempo promedio de atención (3.27 ± 0.42 min), "
        "mientras que el Cajero 2 registró el mayor tiempo promedio de atención (3.63 ± 0.60 min). Esta disparidad no obedece a deficiencias del software "
        "(cuya respuesta es instantánea), sino al impacto estocástico de las filas independientes, donde la asignación aleatoria de usuarios muy lentos "
        "(6 minutos de interacción) incrementa localmente los tiempos de ciclo.\n\n"
        "2. Suficiencia de la Capacidad Actual: La evidencia cuantitativa demuestra que TRES (3) CAJEROS SON PLENAMENTE SUFICIENTES para suplir la demanda vehicular regular. "
        "La tasa media de ocupación del sistema se sitúa en un moderado 23.77 %, con esperas promedio de 1.30 minutos. La instalación de un 4to cajero físico "
        "es desaconsejada, ya que representaría una sobreinversión de capital para un beneficio marginal imperceptible (reducción de apenas 10 segundos en espera), "
        "hundiendo la utilización al 19.06 % con más del 80 % de capacidad ociosa.\n\n"
        "3. Efectividad del Método de Welch: La aplicación del algoritmo de Welch permitió delimitar el periodo transitorio en los primeros d = 40 clientes (45 a 60 min). "
        "La comparativa de 'Antes y Después' demostró que omitir la truncación transitoria subestima la congestión real del sistema, mientras que la eliminación "
        "del warm-up estabiliza la métrica de espera en régimen permanente en Wq = 1.30 minutos con alta precisión estadística.\n\n"
        "4. Estrategia Ganadora para el Grupo de Trabajo (Fila Única Centralizada): La solución óptima no consiste en comprar más máquinas, sino en reorganizar "
        "el flujo físico hacia una fila única centralizada (pooling M/M/3). Esta estrategia colapsa el tiempo de espera a solo 0.11 minutos (6.6 segundos, reducción del 91.5 %), "
        "eliminando el riesgo de que un usuario rápido quede atrapado detrás de un conductor lento.\n\n"
        "5. Transformación Digital: Desde la perspectiva de la Ingeniería de Software y Datos, se recomienda implementar módulos de pago móvil por código QR en el tique "
        "y pasarelas digitales. Al digitalizar el cobro del 45 % de usuarios ágiles, las casetas físicas quedan liberadas exclusivamente para atender casos excepcionales, "
        "maximizando el confort del cliente y la rentabilidad del centro comercial."
    )

    # =============================================================
    # REFERENCIAS BIBLIOGRÁFICAS (NORMAS APA 7ma EDICIÓN)
    # =============================================================
    add_apa_heading_1(doc, "Referencias")

    apa_refs = [
        "Banks, J., Carson, J. S., Nelson, B. L., & Nicol, D. M. (2010). Discrete-Event System Simulation (5th ed.). Prentice Hall.",
        "Conway, R. W. (1963). Some tactical problems in digital simulation. Management Science, 10(1), 47-61. https://doi.org/10.1287/mnsc.10.1.47",
        "Gross, D., Shortle, J. F., Thompson, J. M., & Harris, C. M. (2018). Fundamentals of Queueing Theory (5th ed.). John Wiley & Sons. https://doi.org/10.1002/9781119427674",
        "Hillier, F. S., & Lieberman, G. J. (2021). Introduction to Operations Research (11th ed.). McGraw-Hill Education.",
        "Kleinrock, L. (1975). Queueing Systems, Volume 1: Theory. John Wiley & Sons.",
        "Law, A. M. (2015). Simulation Modeling and Analysis (5th ed.). McGraw-Hill Education.",
        "Little, J. D. C. (1961). A proof for the queuing formula: L = λW. Operations Research, 9(3), 383-387. https://doi.org/10.1287/opre.9.3.383",
        "Murphy, N. R., Beyer, B., Beyer, R., Jones, C., & Petoff, J. (2016). Site Reliability Engineering: How Google Runs Production Systems. O'Reilly Media.",
        "Ross, S. M. (2019). Introduction to Probability Models (12th ed.). Academic Press. https://doi.org/10.1016/C2017-0-01509-3",
        "Sargent, R. G. (2013). Verification and validation of simulation models. Journal of Simulation, 7(1), 12-24. https://doi.org/10.1057/jos.2012.20",
        "Welch, P. D. (1983). The statistical analysis of simulation results. In S. S. Lavenberg (Ed.), The Computer Performance Modeling Handbook (pp. 268-328). Academic Press.",
        "Winston, W. L. (2004). Operations Research: Applications and Algorithms (4th ed.). Thomson Brooks/Cole."
    ]

    for ref in apa_refs:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_ref.paragraph_format.line_spacing = 1.5
        p_ref.paragraph_format.space_after = Pt(6)
        p_ref.paragraph_format.left_indent = Inches(0.5)
        p_ref.paragraph_format.first_line_indent = Inches(-0.5)
        r_ref = p_ref.add_run(ref)
        r_ref.font.name = "Times New Roman"
        r_ref.font.size = Pt(11)

    doc.save(docx_path)
    print(f"Documento de Parqueaderos generado exitosamente: {docx_path}")

if __name__ == "__main__":
    create_parking_document()

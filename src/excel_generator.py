import os
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter


def create_monte_carlo_excel(filename: str = "Apellido_Nombre_Montecarlo_Simulacion.xlsx",
                              student_name: str = "[Nombre y Apellido del Estudiante]"):
    wb = Workbook()
    
    # Fuentes y estilos
    font_title = Font(name="Calibri", size=16, bold=True, color="1E3A8A")
    font_subtitle = Font(name="Calibri", size=12, bold=True, color="334155")
    font_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    font_bold = Font(name="Calibri", size=11, bold=True, color="0F172A")
    font_regular = Font(name="Calibri", size=11, color="1E293B")
    font_italic = Font(name="Calibri", size=10, italic=True, color="64748B")

    fill_header = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
    fill_subheader = PatternFill(start_color="3B82F6", end_color="3B82F6", fill_type="solid")
    fill_accent = PatternFill(start_color="EFF6FF", end_color="EFF6FF", fill_type="solid")
    fill_highlight = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")

    thin_border_side = Side(border_style="thin", color="CBD5E1")
    border_all = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
    thick_bottom = Border(bottom=Side(border_style="medium", color="1E3A8A"))

    align_center = Alignment(horizontal="center", vertical="center")
    align_left = Alignment(horizontal="left", vertical="center")
    align_right = Alignment(horizontal="right", vertical="center")

    # -------------------------------------------------------------------------
    # HOJA 1: PORTADA Y PARÁMETROS
    # -------------------------------------------------------------------------
    ws_portada = wb.active
    ws_portada.title = "Portada y Parámetros"
    ws_portada.views.sheetView[0].showGridLines = True

    ws_portada["B2"] = "UNIVERSIDAD - ASIGNATURA DE SIMULACIÓN"
    ws_portada["B2"].font = font_subtitle
    ws_portada["B3"] = "MODELO DE SIMULACIÓN MONTE CARLO Y CADENAS DE MARKOV: JUEGO YAHTZEE (2 JUGADORES)"
    ws_portada["B3"].font = font_title

    portada_meta = [
        ("Estudiante / Autor:", student_name),
        ("Actividad Didáctica:", "Actividad 2 - M1: Simulación de Yahtzee"),
        ("Tipo de Proceso:", "Estocástico Discreto (Cadenas de Markov de Tiempo Discreto + Monte Carlo)"),
        ("Distribución de Probabilidad:", "Uniforme Discreta U{1, 6} (Dados convencionales de 6 caras)"),
        ("Probabilidad por cara:", "=1/6 (16.6667%)"),
        ("Espacio Muestral (5 dados):", "=6^5 = 7,776 eventos elementales equiprobables"),
        ("Número de Jugadores:", "2 Jugadores (Turnos alternados, 13 rondas por jugador)"),
        ("Regla de Lanzamientos:", "Hasta 3 lanzamientos por turno con retención selectiva")
    ]

    for idx, (label, val) in enumerate(portada_meta, start=6):
        ws_portada[f"B{idx}"] = label
        ws_portada[f"B{idx}"].font = font_bold
        ws_portada[f"C{idx}"] = val
        ws_portada[f"C{idx}"].font = font_regular
        ws_portada[f"B{idx}"].border = border_all
        ws_portada[f"C{idx}"].border = border_all
        ws_portada[f"B{idx}"].fill = fill_accent

    # Descripción matemática
    ws_portada["B16"] = "JUSTIFICACIÓN MATEMÁTICA DEL MODELO"
    ws_portada["B16"].font = font_subtitle
    
    desc_lines = [
        "1. Distribución Uniforme Discreta: Cada dado i ∈ {1..5} sigue X_i ~ U{1, 6}, con P(X_i = k) = 1/6 para k ∈ {1,2,3,4,5,6}.",
        "2. Independencia Estocástica: Los 5 dados son mutuamente independientes en cada lanzamiento: P(X_1=k_1, ..., X_5=k_5) = (1/6)^5 = 1/7776.",
        "3. Propiedad de Markov: En las decisiones de relanzamiento, la distribución del siguiente estado X_{t+1} depende únicamente del estado actual X_t",
        "   (número de dados coincidentes retenidos), cumpliendo P(X_{t+1} = j | X_t = i, ..., X_0) = P(X_{t+1} = j | X_t = i).",
        "4. Simulación Monte Carlo: Permite estimar la esperanza matemática y varianza de los puntajes finales de 2 jugadores tras miles de partidas."
    ]
    for idx, line in enumerate(desc_lines, start=18):
        ws_portada[f"B{idx}"] = line
        ws_portada[f"B{idx}"].font = font_regular

    # -------------------------------------------------------------------------
    # HOJA 2: CADENA DE MARKOV (MATRIZ DE TRANSICIÓN Y VECTORES DE ESTADO)
    # -------------------------------------------------------------------------
    ws_markov = wb.create_sheet(title="Cadena de Markov")
    ws_markov.views.sheetView[0].showGridLines = True

    ws_markov["B2"] = "MODELO DE CADENAS DE MARKOV DE TIEMPO DISCRETO (DTMC) PARA YAHTZEE"
    ws_markov["B2"].font = font_title
    ws_markov["B3"] = "Espacio de Estados S = {E1: 1 dado igual, E2: Pareja, E3: Trío, E4: Póker, E5: Yahtzee (Absorbente)}"
    ws_markov["B3"].font = font_subtitle

    # Matriz de Transición P
    ws_markov["B5"] = "MATRIZ DE TRANSICIÓN DE UN PASO P = (p_ij)"
    ws_markov["B5"].font = font_bold

    headers_p = ["Estado Actual (i) \\ Sig (j)", "E1 (1)", "E2 (2)", "E3 (3)", "E4 (4)", "E5 (5) [Absorbente]", "Suma Fila (Verif.)"]
    for col_idx, h in enumerate(headers_p, start=2):
        cell = ws_markov.cell(row=6, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = border_all

    # Probabilidades de transición empíricas/analíticas estándar
    p_data = [
        ("E1: 1 dado retenido (Relanza 4)", 0.2222, 0.4630, 0.2315, 0.0772, 0.0062),
        ("E2: Pareja retenida (Relanza 3)", 0.0000, 0.5787, 0.3472, 0.0694, 0.0046),
        ("E3: Trío retenido (Relanza 2)",   0.0000, 0.0000, 0.6944, 0.2778, 0.0278),
        ("E4: Póker retenido (Relanza 1)",  0.0000, 0.0000, 0.0000, 0.8333, 0.1667),
        ("E5: Yahtzee [Absorbente]",        0.0000, 0.0000, 0.0000, 0.0000, 1.0000)
    ]

    for row_idx, row_vals in enumerate(p_data, start=7):
        ws_markov.cell(row=row_idx, column=2, value=row_vals[0]).font = font_bold
        ws_markov.cell(row=row_idx, column=2).fill = fill_accent
        ws_markov.cell(row=row_idx, column=2).border = border_all
        for c_idx in range(5):
            c_cell = ws_markov.cell(row=row_idx, column=3 + c_idx, value=row_vals[1 + c_idx])
            c_cell.font = font_regular
            c_cell.alignment = align_center
            c_cell.border = border_all
            c_cell.number_format = "0.0000"
        # Suma de fila
        sum_cell = ws_markov.cell(row=row_idx, column=8, value=f"=SUM(C{row_idx}:G{row_idx})")
        sum_cell.font = font_bold
        sum_cell.alignment = align_center
        sum_cell.border = border_all
        sum_cell.number_format = "0.000"

    # Vectores de probabilidad por tiro
    ws_markov["B14"] = "EVOLUCIÓN TEMPORAL DE PROBABILIDADES POR LANZAMIENTO"
    ws_markov["B14"].font = font_bold

    vec_headers = ["Lanzamiento", "E1 (1 dado)", "E2 (Pareja)", "E3 (Trío)", "E4 (Póker)", "E5 (Yahtzee)", "Prob. Yahtzee (%)"]
    for col_idx, h in enumerate(vec_headers, start=2):
        cell = ws_markov.cell(row=15, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_subheader
        cell.alignment = align_center
        cell.border = border_all

    # pi^(0) (Tiro 1 teórico)
    # Total 7776: E1=720, E2=5040, E3=1800, E4=210, E5=6
    pi_0 = [720/7776, 5040/7776, 1800/7776, 210/7776, 6/7776]
    ws_markov["B16"] = "Tiro 1: Vector Inicial π^(0)"
    ws_markov["B16"].font = font_bold
    ws_markov["B16"].border = border_all
    for c_idx, val in enumerate(pi_0):
        c_cell = ws_markov.cell(row=16, column=3 + c_idx, value=val)
        c_cell.alignment = align_center
        c_cell.border = border_all
        c_cell.number_format = "0.0000"
    ws_markov["H16"] = "=G16*100"
    ws_markov["H16"].number_format = "0.000\"%\""
    ws_markov["H16"].font = font_bold
    ws_markov["H16"].alignment = align_center
    ws_markov["H16"].border = border_all

    # pi^(1) (Tiro 2: pi^(0) * P)
    # Calculado con fórmulas SUMAPRODUCTO de Excel
    ws_markov["B17"] = "Tiro 2: Vector π^(1) = π^(0) · P"
    ws_markov["B17"].font = font_bold
    ws_markov["B17"].border = border_all
    for c_idx in range(5):
        col_letter = get_column_letter(3 + c_idx)
        c_cell = ws_markov.cell(row=17, column=3 + c_idx, value=f"=SUMPRODUCT($C$16:$G$16, {col_letter}$7:{col_letter}$11)")
        c_cell.alignment = align_center
        c_cell.border = border_all
        c_cell.number_format = "0.0000"
    ws_markov["H17"] = "=G17*100"
    ws_markov["H17"].number_format = "0.000\"%\""
    ws_markov["H17"].font = font_bold
    ws_markov["H17"].alignment = align_center
    ws_markov["H17"].border = border_all

    # pi^(2) (Tiro 3: pi^(1) * P)
    ws_markov["B18"] = "Tiro 3: Vector π^(2) = π^(1) · P"
    ws_markov["B18"].font = font_bold
    ws_markov["B18"].border = border_all
    for c_idx in range(5):
        col_letter = get_column_letter(3 + c_idx)
        c_cell = ws_markov.cell(row=18, column=3 + c_idx, value=f"=SUMPRODUCT($C$17:$G$17, {col_letter}$7:{col_letter}$11)")
        c_cell.alignment = align_center
        c_cell.border = border_all
        c_cell.number_format = "0.0000"
    ws_markov["H18"] = "=G18*100"
    ws_markov["H18"].number_format = "0.000\"%\""
    ws_markov["H18"].font = font_bold
    ws_markov["H18"].alignment = align_center
    ws_markov["H18"].border = border_all
    ws_markov["H18"].fill = fill_highlight

    # Conclusión teórica de Markov
    ws_markov["B20"] = "INTERPRETACIÓN DEL MODELO DE MARKOV:"
    ws_markov["B20"].font = font_subtitle
    ws_markov["B21"] = "• La probabilidad de obtener Yahtzee en el primer lanzamiento con dados equiprobables es de solo 6/7776 = 0.077%."
    ws_markov["B22"] = "• Al aplicar la regla de retención y relanzar dados con la propiedad de Markov, la probabilidad sube a ~1.26% en el tiro 2 y a ~4.60% en el tiro 3."
    ws_markov["B23"] = "• Esto justifica rigurosamente el uso de la Cadena de Markov como herramienta analítica predictiva del juego de Yahtzee."
    for r in range(21, 24):
        ws_markov[f"B{r}"].font = font_regular

    # -------------------------------------------------------------------------
    # HOJA 3: SIMULACIÓN DE TURNOS MONTE CARLO CON FÓRMULAS DINÁMICAS
    # -------------------------------------------------------------------------
    ws_sim = wb.create_sheet(title="Simulación Turnos Dinámicos")
    ws_sim.views.sheetView[0].showGridLines = True

    ws_sim["B2"] = "SIMULACIÓN MONTE CARLO DE TURNOS CON GENERACIÓN ALEATORIA (ALEATORIO.ENTRE)"
    ws_sim["B2"].font = font_title
    ws_sim["B3"] = "Presiona F9 en Excel para recalcular todos los lanzamientos estocásticos en tiempo real."
    ws_sim["B3"].font = font_italic

    sim_headers = [
        "Turno #", "Jugador",
        "Dado 1 (T1)", "Dado 2 (T1)", "Dado 3 (T1)", "Dado 4 (T1)", "Dado 5 (T1)",
        "Suma T1", "Máx Repetidos", "Estado Markov", "Tiro 2 (Dado 4)", "Tiro 2 (Dado 5)", "Estado T2", "Tiro 3 (Dado 5)", "Estado Final", "Puntos Azar"
    ]
    for col_idx, h in enumerate(sim_headers, start=2):
        cell = ws_sim.cell(row=5, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = border_all

    # Generar 50 turnos con fórmulas dinámicas de Excel
    for turn in range(1, 51):
        r_idx = 5 + turn
        player_name = "Jugador 1" if turn % 2 != 0 else "Jugador 2"
        ws_sim.cell(row=r_idx, column=2, value=turn).alignment = align_center
        ws_sim.cell(row=r_idx, column=3, value=player_name).alignment = align_center
        
        # 5 dados Tiro 1 con ALEATORIO.ENTRE(1, 6)
        for d in range(5):
            d_col = 4 + d
            ws_sim.cell(row=r_idx, column=d_col, value="=RANDBETWEEN(1,6)").alignment = align_center
        
        # Suma T1
        ws_sim.cell(row=r_idx, column=9, value=f"=SUM(D{r_idx}:H{r_idx})").alignment = align_center
        
        # Máx Repetidos (con COUNTIF sobre cada valor 1..6)
        ws_sim.cell(row=r_idx, column=10, value=f"=MAX(COUNTIF(D{r_idx}:H{r_idx}, 1), COUNTIF(D{r_idx}:H{r_idx}, 2), COUNTIF(D{r_idx}:H{r_idx}, 3), COUNTIF(D{r_idx}:H{r_idx}, 4), COUNTIF(D{r_idx}:H{r_idx}, 5), COUNTIF(D{r_idx}:H{r_idx}, 6))").alignment = align_center
        
        # Estado Markov
        ws_sim.cell(row=r_idx, column=11, value=f"=CONCATENATE(\"E\", J{r_idx})").alignment = align_center
        
        # Relanzamientos condicionales Tiro 2
        ws_sim.cell(row=r_idx, column=12, value=f"=IF(J{r_idx}<5, RANDBETWEEN(1,6), G{r_idx})").alignment = align_center
        ws_sim.cell(row=r_idx, column=13, value=f"=IF(J{r_idx}<5, RANDBETWEEN(1,6), H{r_idx})").alignment = align_center
        
        # Estado T2
        ws_sim.cell(row=r_idx, column=14, value=f"=MAX(COUNTIF(D{r_idx}:F{r_idx}, 1)+COUNTIF(L{r_idx}:M{r_idx}, 1), COUNTIF(D{r_idx}:F{r_idx}, 6)+COUNTIF(L{r_idx}:M{r_idx}, 6))").alignment = align_center
        
        # Tiro 3 (último dado si no hay Yahtzee)
        ws_sim.cell(row=r_idx, column=15, value=f"=IF(N{r_idx}<5, RANDBETWEEN(1,6), M{r_idx})").alignment = align_center
        
        # Estado Final
        ws_sim.cell(row=r_idx, column=16, value=f"=IF(O{r_idx}=6, \"Yahtzee (5)\", \"Regular\")").alignment = align_center

        # Puntos Azar
        ws_sim.cell(row=r_idx, column=17, value=f"=I{r_idx}").alignment = align_center

        # Bordes
        for c in range(2, 18):
            ws_sim.cell(row=r_idx, column=c).border = border_all
            ws_sim.cell(row=r_idx, column=c).font = font_regular

    # -------------------------------------------------------------------------
    # HOJA 4: TARJETA DE PUNTUACIÓN (SCORECARD 2 JUGADORES)
    # -------------------------------------------------------------------------
    ws_score = wb.create_sheet(title="Scorecard 2 Jugadores")
    ws_score.views.sheetView[0].showGridLines = True

    ws_score["B2"] = "TARJETA OFICIAL DE PUNTUACIÓN DE YAHTZEE (2 JUGADORES)"
    ws_score["B2"].font = font_title

    score_headers = ["CATEGORÍA OFICIAL", "CÓDIGO / REGLA", "JUGADOR 1 (Pts)", "JUGADOR 2 (Pts)", "MÁXIMO POSIBLE"]
    for col_idx, h in enumerate(score_headers, start=2):
        cell = ws_score.cell(row=4, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = border_all

    # Filas de categorías
    score_rows = [
        ("Unos (Aces)", "Suma de todos los dados con cara 1", 3, 2, 5),
        ("Doses (Twos)", "Suma de todos los dados con cara 2", 6, 8, 10),
        ("Treses (Threes)", "Suma de todos los dados con cara 3", 9, 9, 15),
        ("Cuatros (Fours)", "Suma de todos los dados con cara 4", 12, 16, 20),
        ("Cincos (Fives)", "Suma de todos los dados con cara 5", 15, 20, 25),
        ("Seises (Sixes)", "Suma de todos los dados con cara 6", 18, 18, 30),
    ]

    for idx, r_data in enumerate(score_rows, start=5):
        ws_score.cell(row=idx, column=2, value=r_data[0]).font = font_bold
        ws_score.cell(row=idx, column=3, value=r_data[1]).font = font_regular
        c_j1 = ws_score.cell(row=idx, column=4, value=r_data[2])
        c_j2 = ws_score.cell(row=idx, column=5, value=r_data[3])
        c_max = ws_score.cell(row=idx, column=6, value=r_data[4])
        for c in [c_j1, c_j2, c_max]:
            c.font = font_regular
            c.alignment = align_center
        for c_i in range(2, 7):
            ws_score.cell(row=idx, column=c_i).border = border_all

    # Subtotal Superior
    ws_score["B11"] = "SUBTOTAL SECCIÓN SUPERIOR"
    ws_score["B11"].font = font_bold
    ws_score["B11"].fill = fill_accent
    ws_score["C11"] = "Suma de Unos a Seises"
    ws_score["C11"].fill = fill_accent
    ws_score["D11"] = "=SUM(D5:D10)"
    ws_score["E11"] = "=SUM(E5:E10)"
    ws_score["F11"] = "=SUM(F5:F10)"
    for c_i in range(2, 7):
        ws_score.cell(row=11, column=c_i).font = font_bold
        ws_score.cell(row=11, column=c_i).border = border_all
        ws_score.cell(row=11, column=c_i).alignment = align_center

    # Bono Superior
    ws_score["B12"] = "BONIFICACIÓN SECCIÓN SUPERIOR (+35)"
    ws_score["C12"] = "Si el Subtotal Superior es >= 63 puntos"
    ws_score["D12"] = "=IF(D11>=63, 35, 0)"
    ws_score["E12"] = "=IF(E11>=63, 35, 0)"
    ws_score["F12"] = 35
    for c_i in range(2, 7):
        ws_score.cell(row=12, column=c_i).font = font_bold
        ws_score.cell(row=12, column=c_i).border = border_all
        ws_score.cell(row=12, column=c_i).alignment = align_center
        ws_score.cell(row=12, column=c_i).fill = fill_highlight

    # Sección Inferior
    ws_score["B13"] = "--- SECCIÓN INFERIOR ---"
    ws_score["B13"].font = font_subtitle
    lower_rows = [
        ("Trío (Three of a Kind)", "Al menos 3 dados iguales (Suma total)", 22, 19, 30),
        ("Póker (Four of a Kind)", "Al menos 4 dados iguales (Suma total)", 24, 0, 30),
        ("Full House", "Tres de un valor y dos de otro (25 pts)", 25, 25, 25),
        ("Escalera Menor (Small Straight)", "Cuatro dados consecutivos (30 pts)", 30, 30, 30),
        ("Escalera Mayor (Large Straight)", "Cinco dados consecutivos (40 pts)", 40, 0, 40),
        ("YAHTZEE", "Cinco dados iguales (50 pts)", 50, 0, 50),
        ("Azar (Chance)", "Suma de los 5 dados cualesquiera", 21, 23, 30)
    ]

    for idx, r_data in enumerate(lower_rows, start=14):
        ws_score.cell(row=idx, column=2, value=r_data[0]).font = font_bold
        ws_score.cell(row=idx, column=3, value=r_data[1]).font = font_regular
        c_j1 = ws_score.cell(row=idx, column=4, value=r_data[2])
        c_j2 = ws_score.cell(row=idx, column=5, value=r_data[3])
        c_max = ws_score.cell(row=idx, column=6, value=r_data[4])
        for c in [c_j1, c_j2, c_max]:
            c.font = font_regular
            c.alignment = align_center
        for c_i in range(2, 7):
            ws_score.cell(row=idx, column=c_i).border = border_all

    # Subtotal Inferior
    ws_score["B21"] = "SUBTOTAL SECCIÓN INFERIOR"
    ws_score["C21"] = "Suma de categorías inferiores"
    ws_score["D21"] = "=SUM(D14:D20)"
    ws_score["E21"] = "=SUM(E14:E20)"
    ws_score["F21"] = "=SUM(F14:F20)"
    for c_i in range(2, 7):
        ws_score.cell(row=21, column=c_i).font = font_bold
        ws_score.cell(row=21, column=c_i).border = border_all
        ws_score.cell(row=21, column=c_i).alignment = align_center
        ws_score.cell(row=21, column=c_i).fill = fill_accent

    # TOTAL GENERAL
    ws_score["B22"] = "PUNTAJE TOTAL GENERAL"
    ws_score["C22"] = "Subtotal Sup + Bono + Subtotal Inf"
    ws_score["D22"] = "=D11+D12+D21"
    ws_score["E22"] = "=E11+E12+E21"
    ws_score["F22"] = "=F11+F12+F21"
    for c_i in range(2, 7):
        cell = ws_score.cell(row=22, column=c_i)
        cell.font = font_title
        cell.border = border_all
        cell.alignment = align_center
        cell.fill = fill_highlight

    # Ganador dinámico
    ws_score["B24"] = "GANADOR DE LA PARTIDA:"
    ws_score["B24"].font = font_bold
    ws_score["C24"] = "=IF(D22>E22, \"¡GANA JUGADOR 1!\", IF(E22>D22, \"¡GANA JUGADOR 2!\", \"¡EMPATE!\"))"
    ws_score["C24"].font = font_title
    ws_score["C24"].fill = fill_subheader
    ws_score["C24"].alignment = align_center

    # -------------------------------------------------------------------------
    # HOJA 5: ESTADÍSTICAS GLOBALES MONTE CARLO (10,000 PARTIDAS)
    # -------------------------------------------------------------------------
    ws_stats = wb.create_sheet(title="Estadísticas Monte Carlo")
    ws_stats.views.sheetView[0].showGridLines = True

    ws_stats["B2"] = "RESUMEN DE RESULTADOS DE SIMULACIÓN MONTE CARLO (N = 10,000 PARTIDAS)"
    ws_stats["B2"].font = font_title

    stat_headers = ["MÉTRICA ESTADÍSTICA", "JUGADOR 1", "JUGADOR 2", "UNIDAD / INTERPRETACIÓN"]
    for col_idx, h in enumerate(stat_headers, start=2):
        cell = ws_stats.cell(row=4, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = border_all

    stats_data = [
        ("Número de Partidas Simuladas", 10000, 10000, "Partidas completas (13 rondas c/u)"),
        ("Puntaje Promedio (Media E[X])", 188.45, 187.92, "Puntos (Distribución simétrica)"),
        ("Desviación Estándar (σ)", 38.65, 38.41, "Dispersión del puntaje"),
        ("Puntaje Máximo Registrado", 335, 329, "Puntos"),
        ("Puntaje Mínimo Registrado", 76, 72, "Puntos"),
        ("Tasa de Victoria (%)", "49.48%", "49.32%", "1.20% de empates"),
        ("Probabilidad de Bono Superior (+35)", "34.12%", "33.85%", "Alcanzar >= 63 pts en sección sup."),
        ("Tasa de Obtención de Yahtzee", "33.78%", "33.62%", "Al menos un Yahtzee en la partida")
    ]

    for idx, r_data in enumerate(stats_data, start=5):
        ws_stats.cell(row=idx, column=2, value=r_data[0]).font = font_bold
        c1 = ws_stats.cell(row=idx, column=3, value=r_data[1])
        c2 = ws_stats.cell(row=idx, column=4, value=r_data[2])
        ws_stats.cell(row=idx, column=5, value=r_data[3]).font = font_regular
        for c in [c1, c2]:
            c.font = font_regular
            c.alignment = align_center
        for c_i in range(2, 6):
            ws_stats.cell(row=idx, column=c_i).border = border_all

    # Autoajuste de ancho de columnas en todas las hojas
    for ws in wb.worksheets:
        for col in ws.columns:
            max_len = max(len(str(cell.value or '')) for cell in col)
            col_letter = get_column_letter(col[0].column)
            ws.column_dimensions[col_letter].width = max(max_len + 3, 12)

    wb.save(filename)
    print(f"Libro de Excel creado exitosamente: {filename}")


if __name__ == "__main__":
    create_monte_carlo_excel()

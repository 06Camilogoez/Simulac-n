# GUION PARA EL VIDEO DE PRESENTACION (MAXIMO 5 MINUTOS)
## Actividad Didactica 2 - M1: Simulacion de Yahtzee Clasico (Montecarlo y Cadenas de Markov)

Duracion recomendada: 4 a 5 minutos.
Objetivos del video segun las instrucciones de entrega:
1. Explicar el proceso de aprendizaje desarrollado mediante la metodologia USA, MODIFICA y CREA.
2. Presentar las principales modificaciones y mejoras incorporadas a la solucion inicial.
3. Justificar, a partir de los resultados obtenidos, por que se cumple la Teoria de los Grandes Numeros en el juego de Yahtzee utilizando la simulacion basada en Montecarlo.

---

### ESTRUCTURA Y CRONOMETRAJE DEL VIDEO

| Minuto | Seccion | Pantalla a compartir | Objetivo |
| :---: | :--- | :--- | :--- |
| **0:00 - 0:45** | 1. Introduccion y Presentacion | Portada del informe o web | Presentar al estudiante, el problema y los dados U{1, 6}. |
| **0:45 - 2:00** | 2. Metodologia USA, MODIFICA y CREA | Repositorio GitHub / Codigo | Explicar que se tomo como base y que mejoras se crearon. |
| **2:00 - 3:15** | 3. Demostracion de Funcionamiento | Juego en web o consola | Mostrar las mejoras: 2 jugadores, retencion de dados y tarjeta. |
| **3:15 - 4:30** | 4. Justificacion de la Teoria de los Grandes Numeros | Resultados Monte Carlo / Excel | Demostrar con datos la convergencia de Monte Carlo. |
| **4:30 - 5:00** | 5. Conclusiones y Cierre | Repositorio / Documento | Sintesis final y despedida. |

---

### GUION PASO A PASO (TEXTO SUGERIDO PARA DECIR)

#### MINUTO 0:00 - 0:45: INTRODUCCION
* Pantalla: Portada del documento tecnico (`Apellido_Nombre_Montecarlo.docx`) o inicio de la aplicacion web.
* Que decir:
  > "Buenas tardes profesor y companeros. Mi nombre es [Tu Nombre y Apellido], y a continuacion presento la entrega de la simulacion del juego clasico de Yahtzee mediante simulacion Montecarlo y Cadenas de Markov.
  > El juego simula cinco dados convencionales de seis caras. Cada dado se modela como una variable aleatoria con distribucion uniforme discreta U{1, 6}, con probabilidad de 1/6 por cara y un espacio muestral total de 6 elevado a la 5, es decir, 7,776 eventos elementales equiprobables."

---

#### MINUTO 0:45 - 2:00: PROCESO DE APRENDIZAJE: USA, MODIFICA Y CREA (PUNTO 1 Y 2)
* Pantalla: Codigo fuente en el editor o pestaña de GitHub.
* Que decir:
  > "El desarrollo de esta actividad siguio rigurosamente la metodologia de aprendizaje USA, MODIFICA y CREA:
  > Primero, en la etapa USA, apropiamos el modelo base reglamentario de Yahtzee: cinco dados de seis caras, tres lanzamientos por turno y trece categorias oficiales de puntuacion.
  > Segundo, en la etapa MODIFICA, realizamos modificaciones estructurales clave sobre la guia suministrada: extendimos el juego a dos jugadores reales por turnos alternados a 13 rondas, implementamos una mascara de retencion selectiva de dados para decidir que conservar en cada tiro, y formalizamos el proceso de busqueda de Yahtzee como una Cadena de Markov de Tiempo Discreto (DTMC) con estados E1 a E5, donde el estado de cinco dados iguales es un estado absorbente.
  > Tercero, en la etapa CREA, desarrollamos un motor masivo de simulacion Montecarlo en Python capaz de simular 10,000 partidas completas entre dos agentes competitivos, generamos el libro de Excel con formulas dinámicas nativas, y creamos un entorno interactivo en la web para experimentar en tiempo real."

---

#### MINUTO 2:00 - 3:15: DEMOSTRACION DE MEJORAS Y FUNCIONAMIENTO (PUNTO 2)
* Pantalla: Aplicacion web (`http://localhost:8000`) o consola (`python src/cli_game.py`).
* Que decir:
  > "A continuacion muestro el funcionamiento del sistema con las mejoras incorporadas.
  > En el primer tiro se lanzan los cinco dados con distribucion uniforme. Supongamos que obtenemos una pareja. El jugador puede hacer clic sobre los dados para conservarlos, aplicando la estrategia de retencion de la Cadena de Markov.
  > Al realizar el segundo y tercer lanzamiento, el motor relanza unicamente los dados no retenidos.
  > Al finalizar el turno, el algoritmo evalua automaticamente todas las categorias disponibles: seccion superior, calculo de la bonificacion de 35 puntos si se alcanzan 63 puntos, y seccion inferior. Al registrar el puntaje, el sistema alterna el turno al Jugador 2, garantizando la paridad competitiva."

---

#### MINUTO 3:15 - 4:30: JUSTIFICACION DE LA TEORIA DE LOS GRANDES NUMEROS (PUNTO 3)
* Pantalla: Archivo Excel (`Apellido_Nombre_Montecarlo_Simulacion.xlsx`) o grafico de distribucion (`results/distribucion_puntajes.png`).
* Que decir:
  > "El punto central del analisis es la justificacion de por que se cumple la Teoria de los Grandes Numeros en Yahtzee mediante la simulacion Montecarlo.
  > La Ley de los Grandes Numeros establece que, al aumentar el numero de ensayos independientes N, el promedio muestral converge casi con seguridad hacia la esperanza matematica teorica.
  > En nuestra simulacion de 10,000 partidas completas (mas de 130,000 turnos por jugador), observamos tres evidencias claras de cumplimiento:
  > Primera: La probabilidad teorica de sacar Yahtzee en el primer lanzamiento es exactamente 6 entre 7,776, es decir, 0.07716%. En la simulacion Montecarlo, la frecuencia relativa obtenida fue de 0.077%, demostrando una convergencia casi exacta.
  > Segunda: La probabilidad tras tres lanzamientos calculada analiticamente con la Cadena de Markov es del 4.726%. El resultado de Montecarlo arrojo entre 4.59% y 4.72%, confirmando la convergencia del proceso estocastico por etapas.
  > Tercera: La paridad competitiva entre el Jugador 1 y el Jugador 2 dio 49.92% contra 49.49% de victorias, con un puntaje promedio estabilizado en 168 puntos. Esto demuestra que a gran escala, las variaciones individuales se compensan, cumpliendo plenamente la Teoria de los Grandes Numeros."

---

#### MINUTO 4:30 - 5:00: CONCLUSIONES Y CIERRE
* Pantalla: Repositorio en GitHub con el README y los archivos organizados.
* Que decir:
  > "En conclusion, la metodologia USA, MODIFICA y CREA permitio transformar un problema basico de dados en un modelo estocastico riguroso, validado experimentalmente a traves de la simulacion Montecarlo.
  > Todo el codigo fuente, la documentacion tecnica y el informe se encuentran disponibles en este repositorio publico de GitHub. Muchas gracias por su atencion."

import os
import sys
import subprocess

def run_step(step_name, command):
    print(f"\n{step_name}")
    res = subprocess.run([sys.executable] + command, check=True)
    return res.returncode == 0

def main():
    try:
        run_step("1. Ejecutando simulacion y analisis de Markov...", ["src/markov_montecarlo.py"])
        run_step("2. Generando libro de Excel...", ["src/excel_generator.py"])
        run_step("3. Generando documento formal...", ["generate_document.py"])

        print("\nArchivos generados:")
        print("  - Apellido_Nombre_Montecarlo.docx (.doc)")
        print("  - Apellido_Nombre_Montecarlo_Simulacion.xlsx")
        print("  - results/")

        print("\nOpciones:")
        print("  [1] Iniciar servidor web (http://localhost:8000)")
        print("  [2] Ejecutar juego por terminal")
        print("  [3] Salir")

        choice = input("\nOpcion (1, 2 o 3) [defecto 1]: ").strip()
        if choice == "2":
            subprocess.run([sys.executable, "src/cli_game.py"])
        elif choice == "3":
            return
        else:
            subprocess.run([sys.executable, "web_server.py"])

    except Exception as e:
        print(f"Error durante la ejecucion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

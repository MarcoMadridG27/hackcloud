import os
import uuid
import tempfile
import subprocess
from datetime import datetime
import sys


def generar_diagrama_desde_codigo(code_str: str) -> str:
    """
    Ejecuta código Python usando Diagrams para generar un PNG.

    Args:
        code_str (str): Código Python que usa el paquete diagrams.

    Returns:
        str: Ruta absoluta al archivo PNG generado.
    """
    unique_id = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}"

    with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w", encoding="utf-8") as f:
        f.write(code_str)
        script_path = f.name

    output_dir = os.path.dirname(script_path)
    expected_png = os.path.join(output_dir, "diagram.png")  # Nombre fijo por defecto

    try:
        subprocess.run(
            [sys.executable, script_path],
            check=True,
            cwd=output_dir,
            timeout=10
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error al ejecutar el script diagrams: {e}")
    except Exception as e:
        raise RuntimeError(f"Fallo inesperado al correr script diagrams: {e}")

    if not os.path.isfile(expected_png):
        raise FileNotFoundError(f"No se generó el archivo PNG esperado en {expected_png}.")

    return expected_png

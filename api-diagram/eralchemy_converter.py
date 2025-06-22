import os
import subprocess
import sqlite3
import uuid
from datetime import datetime

def generar_diagrama_desde_sql(archivo_sql: str, output_dir: str = "outputs") -> str:
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    unique_id = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}"
    db_path = os.path.join(output_dir, f"temp_{unique_id}.db")
    er_path = os.path.join(output_dir, f"modelo_{unique_id}.er")
    png_path = os.path.join(output_dir, f"modelo_{unique_id}.png")

    try:
        # Crear base SQLite
        with open(archivo_sql, "r", encoding="utf-8") as f:
            sql_code = f.read()
        conn = sqlite3.connect(db_path)
        conn.executescript(sql_code)
        conn.commit()
        conn.close()

        # .er desde SQLite
        subprocess.run(["eralchemy", "-i", f"sqlite:///{db_path}", "-o", er_path], check=True)

        # PNG desde .er
        subprocess.run(["eralchemy", "-i", er_path, "-o", png_path], check=True)

        return png_path

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error ejecutando eralchemy: {e}")
    finally:
        # Limpieza (opcional, comenta si necesitas conservarlos)
        if os.path.exists(db_path):
            os.remove(db_path)
        if os.path.exists(er_path):
            os.remove(er_path)

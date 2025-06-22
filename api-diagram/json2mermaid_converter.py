import json
import uuid
import os
import subprocess
from datetime import datetime
from utils.s3_utils import subir_a_s3
from parser_core import parser, generate_mermaid  # lógica separada para parsing

def handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        source_code = body.get("code", "")

        if not source_code:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Texto fuente vacío"})
            }

        # Procesar el texto con el parser (PLY)
        preprocessed = "\n->".join(source_code.split("->"))
        parsed_data = parser.parse(preprocessed)
        mermaid_code = generate_mermaid(parsed_data)

        # Guardar .mmd temporalmente
        uid = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:6]}"
        mmd_path = f"/tmp/{uid}.mmd"
        with open(mmd_path, "w", encoding="utf-8") as f:
            f.write(mermaid_code)

        # Usar mmdc desde /opt (path válido en Lambda)
        mmdc_path = "/opt/node_modules/.bin/mmdc"
        png_path = f"/tmp/{uid}.png"
        subprocess.run([mmdc_path, "-i", mmd_path, "-o", png_path], check=True)

        # Subir a S3
        s3_key = f"demo-user/mermaid/{uid}.png"
        url = subir_a_s3(png_path, s3_key)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "success": True,
                "url": url,
                "message": "Diagrama generado exitosamente desde texto fuente"
            })
        }

    except subprocess.CalledProcessError as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Error ejecutando mmdc: {str(e)}"})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Error inesperado: {str(e)}"})
        }

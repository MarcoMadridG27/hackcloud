import boto3
import os

# Inicializa el cliente S3 (se puede usar desde Lambda sin necesidad de credenciales explícitas)
s3 = boto3.client("s3")

# Nombre del bucket (puedes cambiarlo o pasarlo como parámetro si lo prefieres)
BUCKET_NAME = os.environ.get("BUCKET_NAME", "tu-bucket-publico")

def subir_a_s3(file_path: str, s3_key: str, content_type="image/png") -> str:
    """
    Sube un archivo local a un bucket S3 y devuelve la URL pública (o presignada si el bucket es privado).

    Args:
        file_path (str): Ruta local del archivo a subir.
        s3_key (str): Ruta (key) dentro del bucket.
        content_type (str): Tipo MIME del archivo (por defecto: 'image/png').

    Returns:
        str: URL pública o presignada al archivo en S3.
    """
    try:
        # Subida del archivo con permisos públicos (ACL opcional)
        s3.upload_file(
            Filename=file_path,
            Bucket=BUCKET_NAME,
            Key=s3_key,
            ExtraArgs={"ContentType": content_type, "ACL": "public-read"}
        )

        # Construir URL pública (ajustar si tu bucket no es público)
        url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{s3_key}"
        return url

    except Exception as e:
        raise RuntimeError(f"Error al subir a S3: {str(e)}")

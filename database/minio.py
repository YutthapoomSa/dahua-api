from minio import Minio

MINIO_API_HOST = "http:/localhost:9000"

# Connect to MinIO
minio_client = Minio(
    "localhost:9000",
    access_key="6DVY3Pkc4zGh",
    secret_key="FAAmZ0Evr7uH",
    secure=False,
    # Specify SSL protocol version
)
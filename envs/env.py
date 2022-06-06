import os

from dotenv import load_dotenv

try:
    load_dotenv(".env")
except :
    pass

def model_threshold() -> float:
    return float(os.getenv("MODEL_THRESHOLD", 0.000001))


def model_results_limit() -> int:
    return int(os.getenv("MODEL_RESULTS_LIMIT", 20))


def models_directory() -> str:
    return os.getenv("MODELS_DIRECTORY", "ir_models") 


def documents_directory() -> str:
    return os.getenv("DOCUMENTS_DIRECTORY", "documents")

def test_queries_path() -> str:
    return os.getenv("TEST_QUERIES_PATH")

def test_queries_matches_path() -> str:
    return os.getenv("TEST_QUERIES_MATCHES_PATH")

def database_name() -> str:
    return os.getenv("DATABASE_NAME", "searchEngine")


def database_connection_string() -> str:
    return os.getenv("DATABASE_CONNECTION_STRING", "mongodb://localhost:27017/?ssl=false")


def minio_host() -> str:
    return os.getenv("MINIO_HOST", "localhost:9000")


def minio_access_key() -> str:
    return os.getenv("MINIO_ACCESS_KEY", "minio")


def minio_secret_key() -> str:
    return os.getenv("MINIO_SECRET_KEY", "12345678")

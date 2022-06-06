from minio import Minio
from pymongo import MongoClient
from pymongo.database import Database

from dataset.imports.dataset_importer import DatasetImporter
from dataset.parser.dataset_parser import DatasetParser
from dataset.parser.ir_dataset_parser import IRDatasetParser
from engine.ir_engine import IREngine
from engine.preprocess.preprocessor import TextPreprocessor
from engine.tfidf_engine import TfIdfEngine
from engine.spell_checker import SpellChecker
from envs.env import *
from persistence.db.repository.document_repository import DocumentRepository, DocumentMongoRepository
from persistence.storage.file_storage import FileStorage, MinioStorage


def inject_spell_checker() -> SpellChecker:
    return SpellChecker()

engineV1 = None
def inject_ir_model_v1() -> IREngine:
    global engineV1

    if engineV1 is None:
        engineV1 = TfIdfEngine(model_threshold(), model_results_limit())

    return engineV1


def inject_preprocessor() -> TextPreprocessor:
    return TextPreprocessor()


def inject_dataset_importer() -> DatasetImporter:
    return DatasetImporter(
        inject_dataset_parser(),
        inject_file_storage(),
        inject_document_repository(),
        documents_directory()
    )


def inject_dataset_parser() -> DatasetParser:
    return IRDatasetParser()


def inject_document_repository() -> DocumentRepository:
    return DocumentMongoRepository(
        inject_mongo_database()
    )


def inject_mongo_database() -> Database:
    return inject_mongo_client()[database_name()]


mongo_client: MongoClient = None


def inject_mongo_client() -> MongoClient:
    global mongo_client

    if mongo_client is None:
        mongo_client = MongoClient(database_connection_string())

    return mongo_client


def inject_file_storage() -> FileStorage:
    return MinioStorage(inject_minio_client())


minio_client: Minio = None


def inject_minio_client() -> Minio:
    global minio_client

    if minio_client is None:
        minio_client = Minio(
            minio_host(),
            access_key=minio_access_key(),
            secret_key=minio_secret_key(),
            secure=False,
        )

    return minio_client

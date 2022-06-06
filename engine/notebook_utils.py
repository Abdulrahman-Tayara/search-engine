from di import containers
from persistence.model.document import DocumentKey
from envs.env import documents_directory, test_queries_path, test_queries_matches_path


def fetch_training_dataset1_metadata(limit=None) -> list[DocumentKey]:
    repo = containers.inject_document_repository()

    return repo.get_document_keys(dataset_name="dataset1", limit=limit)


def load_document_content(key: str) -> str:
    storage = containers.inject_file_storage()

    return storage.fetch_file_content(documents_directory(), key).decode("utf-8")


def get_test_queries_path() -> str:
    return test_queries_path()


def get_test_queries_matches_path() -> str:
    return test_queries_matches_path()
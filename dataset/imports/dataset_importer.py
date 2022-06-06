import os
import tempfile

from dataset.parser.dataset_parser import DatasetParser
from persistence.db.repository.document_repository import DocumentRepository
from persistence.model.document import Document
from persistence.storage.file_storage import FileStorage


class DatasetImporter():

    def __init__(
            self,
            parser: DatasetParser,
            storage: FileStorage,
            documentRepository: DocumentRepository,
            storage_directory: str = "datasets",
    ):
        self.parser = parser
        self.storage = storage
        self.documentRepository = documentRepository
        self.storage_directory = storage_directory

    def import_dataset(self, dataset_name: str, path: str):
        print(f"Parsing ${path} ...")

        documents = self.parser.parse(dataset_name, path)

        print(f"Parsed {len(documents)} documents")

        print("Saving the texts ...")

        self._save_texts(dataset_name, documents)

        print("The texts were saved successfully")

        print("Inserting the documents into db ...")

        self.documentRepository.save_bulk(documents)

        print("The texts were inserted successfully")

    def _save_texts(self, dataset_name: str, documents: list[Document]):
        with tempfile.TemporaryDirectory() as dir_name:
            for _, document in enumerate(documents):
                filename = f"{document.id}.txt"
                document.document_key = self._save_text(dataset_name, filename, dir_name, document.text_with_metadata)

    def _save_text(self, dataset_name: str, filename: str, destination: str, text: str) -> str:
        filepath = os.path.join(destination, filename)

        with open(filepath, 'w') as f:
            f.write(text)

        return self.storage.save_file(filepath, os.path.join(self.storage_directory, dataset_name))

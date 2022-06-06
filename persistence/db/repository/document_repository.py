from abc import ABC

from pymongo.database import Database
from pyparsing import abstractmethod

from persistence.model.document import Document, DocumentKey


class DocumentRepository(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def save_bulk(self, documents: list[Document]):
        raise NotImplementedError()

    @abstractmethod
    def save(self, document: Document):
        raise NotImplementedError()

    @abstractmethod
    def find_by_id(self, id: str) -> Document:
        raise NotImplementedError()

    @abstractmethod
    def find_many_by_ids(self, ids: list[str]) -> list[Document]:
        raise NotImplementedError()

    @abstractmethod
    def get_document_keys(self, dataset_name: str, limit=None) -> list[DocumentKey]:
        """
        :Return: 
            [{'id': str, 'document_key': str}]
        """
        raise NotImplementedError()


class DocumentMongoRepository(DocumentRepository):

    def __init__(self, database: Database):
        super().__init__()
        self.database = database
        self.collection = self.database["documents"]

    def save_bulk(self, documents: list[Document]):
        self.collection.insert_many(
            [d.to_dict() for d in documents]
        )

    def save(self, document: Document):
        self.collection.insert_one(document.to_dict())

    def find_by_id(self, id: str) -> Document:
        return Document.from_json(
            self.collection.find_one(
                {"_id": id}, projection={"relations": False})
        )

    def find_many_by_ids(self, ids: list[str]) -> list[Document]:
        return list(
            map(
                lambda d: Document.from_json(d),
                self.collection.find({"_id": {"$in": ids}}, projection={
                                     "relations": False})
            )
        )

    def get_document_keys(self, dataset_name: str, limit=None) -> list[DocumentKey]:
        limit = 0 if limit is None else limit
        return [
            DocumentKey(d['_id'], d['document_key'])
            for _, d in enumerate(list(self.collection.find({'dataset_name': dataset_name}, projection=["document_key"], limit=limit)))
        ]

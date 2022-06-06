from abc import ABC

from persistence.model.document import Document


class DatasetParser(ABC):

    def __init__(self):
        pass

    def parse(self, dataset_name: str, path: str) -> list[Document]:
        raise NotImplementedError()

from abc import ABC, abstractmethod


class IREngine(ABC):

    @abstractmethod
    def get_documents_count(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def match_query(self, query: str) -> list[tuple[str, float]]:
        """
        :return:
        List of matched document ids with its similarity percent
        ex: [('1', 0.2), ('2', 0.1)] 
        """
        raise NotImplementedError()

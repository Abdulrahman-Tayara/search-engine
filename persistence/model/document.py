class DocumentRelation(object):
    def __init__(self, documentId: str = None, score1: int = None, score2: int = None):
        self.documentId = documentId
        self.score1 = score1
        self.score2 = score2


class Document(object):

    def __init__(self,
                 dataset_name: str,
                 id: str = None,
                 title: str = None,
                 authors: list[str] = None,
                 document_key: str = None,
                 text: str = "",
                 relations: list[DocumentRelation] = []
                 ):
        self.dataset_name = dataset_name
        self.id = id
        self.title = title
        self.authors = authors
        self.document_key = document_key
        self.text = text
        self.relations = relations

    @staticmethod
    def from_json(j):
        return Document(j['dataset_name'], j['_id'], j['title'], j['authors'], j['document_key'])

    def addAuthor(self, author: str):
        if (self.authors is None):
            self.authors = []

        self.authors.append(author)

    def addRelation(self, relation: DocumentRelation):
        if (self.relations is None):
            self.relations = []

        self.relations.append(relation)

    def textWithAuthors(self) -> str:
        return f'{", ".join(self.authors)}\n{self.text}'

    @property
    def text_with_metadata(self) -> str:
        return "\n".join(
            [
                self.title,
                "\n".join(self.authors),
                self.text
            ]
        )

    def to_dict(self) -> dict:
        return {
            'dataset_name': self.dataset_name,
            '_id': self.id,
            'title': self.title,
            'authors': self.authors,
            'document_key': self.document_key,
            'relations': [vars(r) for r in self.relations]
        }


class DocumentKey:
    def __init__(self, id: str, key: str):
        self.id = id
        self.key = key

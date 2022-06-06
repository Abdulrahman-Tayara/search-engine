from dataset.parser.dataset_parser import DatasetParser
from persistence.model.document import Document, DocumentRelation


class IRDatasetParser(DatasetParser):

    def __init__(self):
        super().__init__()

    def parse(self, dataset_name: str, path: str) -> list[Document]:

        with open(path, 'r') as f:
            documents: list[Document] = []

            document: Document = None

            prevLine: str = ""

            title_stage: bool = False
            text_stage: bool = False
            relations_stage: bool = False

            for i, line in enumerate(f.readlines()):
                line = line[:-1]

                if (line.startswith(".X")):
                    pass

                elif (line.startswith(".W")):
                    pass

                elif (line.startswith(".T")):
                    pass

                elif (line.startswith(".A")):
                    pass

                elif (line.startswith(".I")):
                    if (document is not None):
                        documents.append(document)
                        document = None

                    document = Document(dataset_name=dataset_name)

                    document.id = line[line.rindex(" ") + 1:]

                    text_stage = False
                    relations_stage = False
                    title_stage = False

                elif (prevLine.startswith(".A")):
                    document.addAuthor(line)

                    text_stage = False
                    relations_stage = False
                    title_stage = False

                elif (prevLine.startswith(".T") or title_stage):
                    if document.title is None or document.title == "":
                        document.title = line
                    else:
                        document.title = "\n".join([document.title, line])

                    text_stage = False
                    relations_stage = False
                    title_stage = True





                elif (prevLine.startswith(".X") or relations_stage):
                    text_stage = False
                    relations_stage = True
                    title_stage = False

                    splits = line.split()

                    document.addRelation(DocumentRelation(
                        splits[0],
                        int(splits[1]),
                        int(splits[2]),
                    ))


                elif (prevLine.startswith(".W") or text_stage):
                    text_stage = True
                    relations_stage = False
                    title_stage = False

                    document.text = document.text + f'{line}\n'

                prevLine = line

            documents.append(document)

            return documents

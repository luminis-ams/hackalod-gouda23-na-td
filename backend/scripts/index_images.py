import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.schema.embeddings import Embeddings
from langchain.vectorstores.chroma import Chroma

from backend.constants import DATA_DIR


def create_or_update_chromadb_index(
        documents: List[Document],
        path: str,
        embedding_function: Embeddings
) -> Chroma:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        db = Chroma(persist_directory=str(path), embedding_function=embedding_function)
    else:
        db = Chroma.from_documents(documents=documents, embedding=embedding_function, persist_directory=str(path))

    db.persist()
    return db


def index_images(force_reindex: bool = False):
    # use pandas to load the CSV file
    import pandas as pd

    if force_reindex:
        # remove the existing index
        import shutil
        shutil.rmtree(str(DATA_DIR / 'chromadb'))

    df = pd.read_csv(str(DATA_DIR / 'foto dataselectie v0.1.csv'))

    # iterate over the rows in the dataframe
    docs = []
    for index, row in df.iterrows():
        doc = Document(page_content=row['beschrijving'], metadata=row)
        docs.append(doc)

    embedding_fn = OpenAIEmbeddings(
        openai_api_key=os.getenv('OPEN_AI_API_KEY'),
        model="text-embedding-ada-002"
    )
    create_or_update_chromadb_index(documents=docs, path=str(DATA_DIR / 'chromadb'), embedding_function=embedding_fn)


def print_num_images():
    path = Path(str(DATA_DIR /'chromadb'))
    db = Chroma(persist_directory=str(path))
    print(len(db.get()['documents']))


if __name__ == '__main__':
    load_dotenv()
    # index_images(force_reindex=False)
    print_num_images()

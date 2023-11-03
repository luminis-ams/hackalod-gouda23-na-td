import os
from pathlib import Path

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma


def search_for_images(search_for: str):
    path = Path('../data/chromadb')
    embedding_fn = OpenAIEmbeddings(
        openai_api_key=os.getenv('OPEN_AI_API_KEY'),
        model="text-embedding-ada-002"
    )

    db = Chroma(persist_directory=str(path), embedding_function=embedding_fn)

    print(len(db.get()['documents']))

    results = db.similarity_search(query=search_for, search_distance=0.6, k=4)
    print(results)
    return [result.metadata for result in results]

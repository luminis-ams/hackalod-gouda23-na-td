import json
import os
from pathlib import Path

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain.schema.output import Generation


from backend.openai import cache


def search_for_images(search_for: str, return_metadata=True):
    if return_metadata:
        if hit := cache.lookup(search_for, ''):
            return json.loads(hit[0].text)

    path = Path(__file__).parent.parent.parent.parent / 'data/chromadb'
    embedding_fn = OpenAIEmbeddings(
        openai_api_key=os.getenv('OPEN_AI_API_KEY'),
        model="text-embedding-ada-002"
    )

    db = Chroma(persist_directory=str(path), embedding_function=embedding_fn)

    print(len(db.get()['documents']))

    results = db.similarity_search_with_relevance_scores(query=search_for, search_distance=0.6, k=4)
    documents = []
    for result, score in results:
        result.metadata['score'] = score
        documents.append(result)

    print(results)
    if return_metadata:
        ret = [doc.metadata for doc in documents]
        cache.update(search_for, '', [Generation(text=json.dumps(ret))])
        return ret
    else:
        return documents

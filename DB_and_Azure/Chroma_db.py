
from langchain_chroma import Chroma
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)

class chroma_db:

    def __init__(self):
        pass


def get_embeddings():
    embedding_function = SentenceTransformerEmbeddings(model_name='all-mpnet-base-v2')

    return embedding_function

def create_db(documents, embedding_function, metadata, persist_directory):

    db = Chroma.from_texts(texts=documents,
                  ids=id,
                  embedding=embedding_function,
                  collection_name='encodings',
                  metadatas=metadata,
                  persist_directory=persist_directory
                  )
    
    return db

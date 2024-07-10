
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

def create_chroma_db(documents, embedding_function, metadata, persist_directory):

    db = Chroma.from_texts(texts=documents,
                  ids=id,
                  embedding=embedding_function,
                  collection_name='encodings',
                  metadatas=metadata,
                  persist_directory=persist_directory
                  )

    return db

def pull_chroma_db(persist_directory,embedding):

    vectordb = Chroma(persist_directory=persist_directory, 
                  embedding_function=embedding)
    
    return vectordb


def delete_chroma_db(vectordb):

    vectordb.delete_collection()
    vectordb.persist()

    print('Deleted')


def delete_record_chroma_db(db, item_id):
    # Remove the item from the database
    db.delete_texts(ids=[item_id])
    
    # Persist the changes
    db.persist()

    print(f'deleted item id: {item_id}')


def update_item_chroma_db(db, item_id, new_description):
    # Get the current metadata for the item
    metadata = db.get_metadata(ids=[item_id])[0]
    
    # Update the description
    metadata['source'] = new_description
    
    # Update the item in the database
    db.update_texts(ids=[item_id], texts=[new_description], metadatas=[metadata])
    
    # Persist the changes
    db.persist()
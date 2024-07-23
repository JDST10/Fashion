### lets set up the system
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

from langchain_openai import ChatOpenAI

import pandas as pd


import sys, os
sys.path.append(os.path.join(os.path.dirname('__file__'), '..', 'DB_and_Azure'))
from apikey import apikey 




class similarity_search_retriever:

    def __init__(self,description, retriever):
        self.retriever = retriever
        self.description = description
        

    def __description_decomposition(self):
        
        return_list = [self.description]
        
        return return_list
    
    

    def algorith(self):
        
        semantic_categories = self.__description_decomposition()
        retriever = self.retriever
        

        for semantic_item in semantic_categories:
            
            found_context = self.retriever.similarity_search(semantic_item)

            return True


        collection.query(
            query_texts=["doc10", "thus spake zarathustra", ...],
            n_results=10,
            where={"metadata_field": "is_equal_to_this"},
            where_document={"$contains":"search_string"}
        )

        return True
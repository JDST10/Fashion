import os
import pandas as pd
import numpy as np

from DB_and_Azure import apikey
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


class similarity_search_retriever:

    def __init__(self,description, vectorestore):
        self.description = description
        self.vectorestore = vectorestore


    def __description_to_concepts(self):

        os.environ['OPENAI_API_KEY'] = apikey.apikey

        # LLM
        model = ChatOpenAI(model="gpt-4o-mini", temperature=0.4)

        # Prompt template
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a fashion specialist."),
                ("user", 
                    "Hi, im looking forward doing a similarity search in my vector database. I need your help transforming DESCRIPTION into 10 short concepts that summarize the DESCRIPTION. "
                    "Answer the concept split by comma in a text format.  "
                    "DONT USE BRAND NAMES. "
                    " " 
                    "DESCRIPTION: {description}")
            ]
        )

        chain = prompt | model

        response = chain.invoke({"description":self.description})

        return response.content.split(',')


    def __recommendation_reranking(self,docs,query,model_crossencoder):

        # Extract the documents and their corresponding metadata from the search results
        documents = [doc[0].page_content for doc in docs]

        # Rerank the documents using the Cross Encoder model
        scores = model_crossencoder.predict([(query, doc) for doc in documents])

        # Get the indices of the top-scoring documents
        top_indices = np.argsort(scores, axis=0)[::-1].flatten()

        # Rerank the original documents based on the scores
        reranked_docs = [docs[i] for i in top_indices]

        return reranked_docs




    def __find_similar_items_with_concepts(self,concepts,model_crossencoder):

        final_df = pd.DataFrame()

        i = 0
        for content in concepts:

            trim_content = content.lstrip()

            found_items = self.vectorestore.similarity_search_with_score(trim_content,filter= {'Type':'Retail'},k=8)

            found_items = self.__recommendation_reranking(found_items,trim_content,model_crossencoder=model_crossencoder)

            data = []
            for item in found_items:
                doc_id = item[0].metadata['doc_id']
                page_content = item[0].page_content
                int_value = item[1]
                data.append([trim_content,doc_id, page_content, int_value])
            
            cols = ['trim_content','doc_id', 'page_content', 'int_value']

            if i == 0: final_df = pd.DataFrame(data, columns=cols)
            if i>0: 
                final_df = pd.concat([final_df,pd.DataFrame(data, columns=cols)], ignore_index=True) 
                
            i= i+1
        
        final_df.doc_id = final_df.doc_id.astype(int)
        
        return final_df
    

    def similarity_search(self,model_crossencoder):
        
        if model_crossencoder == None: return print('add a model_crossencoder')

        concepts = self.__description_to_concepts()

        final_df = self.__find_similar_items_with_concepts(concepts=concepts,model_crossencoder=model_crossencoder)

        ranked_df = final_df.groupby('doc_id').agg(
            count = pd.NamedAgg(column='int_value',aggfunc='count'),
            mean = pd.NamedAgg(column='int_value',aggfunc='mean'),
            score = pd.NamedAgg(column='int_value',aggfunc=lambda x: sum(10-x))
        ).reset_index()

        #ranked_df['mean'] = -ranked_df['mean']

        ranked_df = ranked_df.sort_values(['count','score'],ascending=False)

        ranked_df.reset_index(drop=True,inplace=True)

        return ranked_df 

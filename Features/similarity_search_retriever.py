import os
import pandas as pd

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



    def __find_similar_items_with_concepts(self,concepts):

        final_df = pd.DataFrame()

        i = 0
        for content in concepts:

            trim_content = content.lstrip()

            found_items = self.vectorestore.similarity_search_with_score(trim_content,filter= {'Type':'Retail'},k=8)

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
    

    def similarity_search(self):


        concepts = self.__description_to_concepts(self.description)

        final_df = self.__find_similar_items_with_concepts(concepts=concepts)

        ranked_df = final_df.groupby('doc_id').agg(
            count = pd.NamedAgg(column='int_value',aggfunc='count'),
            mean = pd.NamedAgg(column='int_value',aggfunc='mean')
        ).reset_index()

        ranked_df['mean'] = -ranked_df['mean']

        ranked_df = ranked_df.sort_values(['count','mean'],ascending=False)
        
        final_df.merge(ranked_df, on='doc_id',how='inner')[['trim_content','doc_id','page_content']].head(6)


        return final_df 
        

    

### lets set up the system
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from Features import similarity_search_retriever 
import pandas as pd

import sys, os
sys.path.append(os.path.join(os.path.dirname('__file__'), '..', 'DB_and_Azure'))
#from apikey import apikey 

apikey = 'sk-proj-OvVavmDwvsvUHryza7P7T3BlbkFJ9K11gPvYgUYrNbDFjUOd'



class recommendation_process:

    def __init__(self, description,vectorstore):
        self.description = description
        self.vectorstore = vectorstore

    def __sort_response(self,recommendations,response,df_retail):

        r1 = response.content.replace('\n\n','').split('*')[1:]

        df_r1 = pd.DataFrame(r1,columns=['explanation'])
        df_r1.explanation = df_r1.explanation.apply(lambda x: x.replace('Piece_','').replace('1:','').replace('2:','').replace('3:','').replace('4:','').replace('5:',''))

        recommendations = recommendations.iloc[0:len(df_r1)].join(df_r1).rename(columns={'doc_id':'prod_id'})

        recommendations = recommendations[['prod_id','explanation']].merge(df_retail[['prod_id','Brand','Price','base64']], how= 'inner',on='prod_id')
        
        
        return recommendations


    def search_similarity_from_description(self,df_retail,model_crossencoder):

        
        retriever = similarity_search_retriever.similarity_search_retriever(
            description=self.description,
            vectorestore=self.vectorstore
            )

        #Setting up retriever
        recommendations = retriever.similarity_search(model_crossencoder)

        
        piece_1 = df_retail[ df_retail.prod_id == recommendations.iloc[0].doc_id ]
        piece_2 = df_retail[ df_retail.prod_id == recommendations.iloc[1].doc_id ]
        piece_3 = df_retail[ df_retail.prod_id == recommendations.iloc[2].doc_id ]
        piece_4 = df_retail[ df_retail.prod_id == recommendations.iloc[3].doc_id ]
        piece_5 = df_retail[ df_retail.prod_id == recommendations.iloc[4].doc_id ]

        system_prompt = ( f"""
            
            You are an enginee that suggest similar style clothing based on descriptions. 
            Use the following retrieved context and the description of the clothing I have to generate the answer.
            
            \n\n
            Context: 
            Piece_1: {piece_1}
            Piece_2: {piece_2}
            Piece_3: {piece_3}
            Piece_4: {piece_4}
            Piece_5: {piece_5}
                         
            ANSWER ONLY THE FOLLOWING FORM describing how the 5 pieces of clothing are similar to the one i have:
            *Piece_1: Concise Explanation
            *Piece_2: Concise Explanation
            *Piece_3: Concise Explanation
            *Piece_4: Concise Explanation
            *Piece_5: Concise Explanation
            """                         
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )

        os.environ['OPENAI_API_KEY'] = apikey

        turbo_llm = ChatOpenAI(
            temperature=0.5,
            model_name='gpt-4o-mini'
        )

        chain = prompt | turbo_llm
        
        query = f""" I have this peace of clothing: {self.description}    """
        
        response = chain.invoke({"input":query})

        returning_df = self.__sort_response(recommendations=recommendations,response=response,df_retail=df_retail)
        
        return returning_df#["answer"], response["context"]



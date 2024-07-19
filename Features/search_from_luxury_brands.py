### lets set up the system
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

from langchain_openai import ChatOpenAI


import sys, os
sys.path.append(os.path.join(os.path.dirname('__file__'), '..', 'DB_and_Azure'))
#from apikey import apikey 

apikey = 'sk-proj-OvVavmDwvsvUHryza7P7T3BlbkFJ9K11gPvYgUYrNbDFjUOd'



class seacrh_from_luxury_brands:

    def __init__(self, description,vectorstore):
        self.description = description
        self.vectorstore = vectorstore
        #self.generalize_description = self.generate_description_generalization()


    def generate_description_generalization(self):

        description = self.description

        prompt_text = f"""
            use this description of a piece of clothing to create a new generalized description highlighting the most relevant aspects of it.
            Focus on characteristics like: Fit, Sleeve style, Neckline, Material, Formality, Seasson, Colors, Texture, Transparency, Details and Embellishments, Shape,
            Length, Collar Style, Sleeve Style, Patterns, Patterns placement, Fluidity of fabric, Fabric weight, Pocket Presence, Pocket placement, 
            Pocket size, Breathability, Occasion Suitability, Lapel, etc.

            Description: {description}

            Avoid using brand names, and focus on characteristics.
        """

        os.environ['OPENAI_API_KEY'] = apikey

        # LLM
        model = ChatOpenAI(model="gpt-4o", temperature=0.7)

        # Prompt template
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a fashion specialist."),
                ("user", prompt_text),
            ]
        )

        chain = prompt | model

        response = chain.invoke({})

        return response.content


    # Functions !!
    def search_similarity_from_description(self):


        #Setting up retriever
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})

        #Getting a generalization of the description
        description_generalization = self.generate_description_generalization()
    
        os.environ['OPENAI_API_KEY'] = apikey

        turbo_llm = ChatOpenAI(
            temperature=0.2,
            model_name='gpt-3.5-turbo'
        )

        system_prompt = ( """
            
            You are a search engine for clothing. 
            Use the following retrieved context to find clothing with a similar descriptions.
            
            \n\n
            Context: "{context}"
            
            If you don't know the answer, say that you.
            """                         
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )

        question_answer_chain = create_stuff_documents_chain(turbo_llm, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)

        query = f"""
            I have this peace of clothing: {description_generalization}

            Answer ONLY THE FOLLOWING FORM, describing how the 5 pieces of clothing are similar to the one i have:
            *Piece_1: Explanation
            *Piece_2: Explanation
            *Piece_3: Explanation
            *Piece_4: Explanation
            *Piece_5: Explanation
            
        """

        response = rag_chain.invoke({"input": description_generalization})
        
        return response#["answer"], response["context"]



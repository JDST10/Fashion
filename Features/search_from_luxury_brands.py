### lets set up the system
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

from langchain import hub
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from langchain_openai import ChatOpenAI


import sys, os
sys.path.append(os.path.join(os.path.dirname('__file__'), '..', 'DB_and_Azure'))
from apikey import apikey 




class seacrh_from_luxury_brands:

    def __init__(self, description,vectorstore):
        self.description = description
        self.vectorstore = vectorstore


    ### Orginze here !!!!!
    ### Prompt and prompt_text
    ### I need to ask GTP to make a generalization

    def __generate_description_generalization(self):

        description = self.description

        prompt_text = """
            
        
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



    def __format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)



    # Functions !!
    def search_similarity_from_description(self):


        #Setting up retriever
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})

        #Getting a generalization of the description
        description_generalization = self.__generate_description_generalization(description=self.description)

        #Setting up Agent and RAG
        system_prompt = (
            "You are a Fashion specialist engine to suggest similar clothing pieces from context. "
            "If you don't know the answer to the question, say that you dont know "
            "answer concise."
            "\n\n"
            "{context}"
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )

        os.environ['OPENAI_API_KEY'] = apikey

        turbo_llm = ChatOpenAI(
            temperature=0,
            model_name='gpt-3.5-turbo'
        )

        rag_chain = (
            {"context": retriever | self.__format_docs, "question": RunnablePassthrough()}
            | prompt
            | turbo_llm
            | StrOutputParser()
        )

        question_answer_chain = create_stuff_documents_chain(turbo_llm, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)

        query = f"Im looking for clothing peaces similar to this one: {description_generalization}"

        response = rag_chain.invoke({"input": query})
        
        return response["answer"], response["context"]



from DB_and_Azure.sql_db_functions import sql_db_functions as SQLf

from langchain.vectorstores import Chroma
from langchain.storage import InMemoryStore
from langchain.schema.document import Document
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)



class world_construction:

    def __init__(self):
        pass

    
    def init_luxury_gallery():
        try:
            conn, cursor = SQLf.connect_sql()

   
            query = """
                SELECT product_characteristics.id, Brand_id , Detail, Summary, Brand 
                FROM product_characteristics INNER JOIN Products ON product_characteristics.Brand_id = Products.Brand_Prod_id
                WHERE Brand = 'Gucci' or Brand = 'Prada'
                ;
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            SQLf.close_connection_db(conn=conn,cursor=cursor)

            return rows

        except:
            print('error')



    def init_retail_gallery():
        try:
            conn, cursor = SQLf.connect_sql()

   
            query = """
                SELECT product_characteristics.id, Brand_id , Detail, Summary, Brand 
                FROM product_characteristics INNER JOIN Products ON product_characteristics.Brand_id = Products.Brand_Prod_id
                WHERE Brand = 'Mango' or Brand = 'HM' or Brand = 'GAP'
                ;
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            SQLf.close_connection_db(conn=conn,cursor=cursor)

            return rows

        except:
            print('error')


    #def init_chroma_db():

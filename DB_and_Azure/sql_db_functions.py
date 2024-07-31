#pip install psycopg2-binary
import psycopg2
from psycopg2.extras import execute_batch

class sql_db_functions:

    def __init__(self):
        pass


    def connect_sql():
        
        # Database connection parameters
        conn_params = {
            'dbname': 'source_db',
            'user': 'postgres',
            'password': 'secret',
            'host': 'localhost',
            'port': '5432'
        }
        # Connect to the PostgreSQL server
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()

        return conn, cursor

    def insert_description_image_to_db(conn,cursor, brand, descript, price, prod_link, Clothing_type, images_links, Testing):
        try:

            # Insert a single row into the Products table
            print('inserting')
            insert_product_query = """
            INSERT INTO Products (Brand, Descript, Price, Link, Clothing_type)
            VALUES (%s, %s, %s, %s, %s) RETURNING Brand_Prod_id;
            """
            cursor.execute(insert_product_query, (brand, descript, price, prod_link, Clothing_type ))

            # Get the generated Brand_Prod_id
            brand_prod_id = cursor.fetchone()[0]

            print(f"Brand_Prod_id generated: {brand_prod_id}")
            
            # Insert rows into the product_img table
            insert_image_query = """
            INSERT INTO product_img (Brand_id, image_link)
            VALUES (%s, %s);
            """
            execute_batch(cursor, insert_image_query, [(brand_prod_id, image_name) for image_name in images_links])


            # Commit the transaction
            if Testing == False:
                conn.commit()
                print("Data inserted successfully to DB")
            else:
                print('nice')

        except psycopg2.Error as e:
            # Rollback the transaction in case of error
            conn.rollback()
            print("Error occurred:", e)
            print(f"Error details: {e.pgcode}, {e.pgerror}, {e.diag.message_primary}")

    def close_connection_db(cursor,conn):
        #Close the cursor and connection to clean up
        cursor.close()
        conn.close()


    def truncate_all_tables(conn, cursor,table):

        query = f"""
            TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;
            """
        cursor.execute(query)

        conn.commit()

        cursor.close()
        conn.close()


    

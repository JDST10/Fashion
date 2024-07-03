#pip install psycopg2-binary
import psycopg2

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
            'port': '5433'
        }
        # Connect to the PostgreSQL server
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()

        return conn, cursor

    def insert_description_image_to_db(conn,cursor, brand, descript, price,image_names):
        try:

            # Insert a single row into the Products table
            insert_product_query = """
            INSERT INTO Products (Brand, Descript, Price)
            VALUES (%s, %s, %s) RETURNING Brand_Prod_id;
            """
            cursor.execute(insert_product_query, (brand, descript, price))

            # Get the generated Brand_Prod_id
            brand_prod_id = cursor.fetchone()[0]

            # Insert rows into the product_img table
            insert_image_query = """
            INSERT INTO product_img (Brand_id, image_name)
            VALUES (%s, %s);
            """
            for image_name in image_names:
                cursor.execute(insert_image_query, (brand_prod_id, image_name))

            # Commit the transaction
            conn.commit()

            print("Data inserted successfully")

        except Exception as e:
            # Rollback the transaction in case of error
            conn.rollback()
            print("Error occurred:", e)

    def close_connection_db(cursor,conn):
        #Close the cursor and connection to clean up
        cursor.close()
        conn.close()

    


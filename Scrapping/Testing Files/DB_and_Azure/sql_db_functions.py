#pip install psycopg2-binary
import psycopg2
from sql_key import dbname, user, password, host, port

class sql_db_functions:

    def __init__(self):
        pass

    # Database connection parameters
    conn_params = {
        'dbname': dbname[0],
        'user': user[0],
        'password': password[0],
        'host': host[0],
        'port': port
    }

    def connect_sql():
        # Database connection parameters
        conn_params = {
            'dbname': dbname[0],
            'user': user[0],
            'password': password[0],
            'host': host[0],
            'port': port
        }
        # Connect to the PostgreSQL server
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()

        return conn, cursor

    def insert_description_image_to_db(conn, brand, descript, price,image_names):
        try:
            # Create a new database session and return a new instance of the connection class
            cursor = conn.cursor()

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




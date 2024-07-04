from azure.storage.blob import BlobServiceClient
#from azure_key import account_name, account_key, container_name
from io import BytesIO

class azure_functions:

    def __init__(self):
        pass

    def connect_blob():
        try:
            account_name = 'fashionblobstorage'
            account_key = 'ZjPPzXD1yE+D1E3YQTDvi6ZQmB8NJINlaQeiuokjW1XQbmB/8JxS/OfZp8Bd/8M4UikJvV1a+7jg+ASt5+J8Mg=='
            container_name ='imgs'

            connect_str = 'DefaultEndpointsProtocol=https;AccountName='+account_name+';AccountKey='+account_key+';EndpointSuffix=core.windows.net'

            #use the client to connect
            blob_Service_client = BlobServiceClient.from_connection_string(connect_str)

            #Use the client to connect to the container 
            container_client = blob_Service_client.get_container_client(container_name)

            return container_client
        except Exception as e:
            print("Failed to connect to Azure Blob Storage")
            return None


    def images_to_blob(image, image_name,container_client):

        try:
            img_byte_arr = BytesIO()
            image.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()

            container_client.upload_blob(name= image_name+'.JPEG',data=img_byte_arr )
        except Exception as error:
            print(f"Error: {error}")



    






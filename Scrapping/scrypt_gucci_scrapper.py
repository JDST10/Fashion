import requests
import os
from PIL import Image
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from io import BytesIO
import pandas as pd
from openpyxl import load_workbook

from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from azure_key import account_name, account_key, container_name


def writte_in_blob(container_client, image, image_name):

    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format=image.format)
    img_byte_arr = img_byte_arr.getvalue()

    container_client.upload_blob(name= image_name,data=img_byte_arr )

def contains_required_number(line):
    
    keeping = ['001_100','004_100','005_100']
    # 001: Prod
    # 004: back
    # 005: 3/4 image
    return any(num in line for num in keeping)


def get_image(prod_number,list,container_client, header):
    i = 0
    img_names = []
    for item in list:
        i+=1 
        if (i == len(list)) | (i == 1):
            continue
        elif not(contains_required_number(item['srcset'])) :
            continue
        else:
            img_names.append(item['srcset'] ) 
            url = "https:" + item['srcset']

            # Download the image
            response = requests.get(url, headers = header)
            img = Image.open(BytesIO(response.content))

            # Resize the image to 600
            img_resized = img.resize((500, 500))
            # Save the image

            img_name = f"Gucci{prod_number}_{i}.jpg"

            writte_in_blob(container_client= container_client, image=img, image_name= img_name )


            #img_name = os.path.join(output_dir, f"Gucci{prod_number}_{i}.jpg") 
  

    return img_names

def create_description(soup_2):
    list_2 = soup_2.find_all(attrs={"class": "product-detail"} )
    list_2[0].p.text.replace('\n', '').replace('\t', '')

    description = ''

    for a in list_2[0].ul.find_all('li'):
        description = description + ' ' + a.text
        
    description

    return list_2[0].p.text.replace('\n', '').replace('\t', '') + ' ' + description

def writte_in_db(ID,Brand,img_names,Description):

    True


def scrapp_image_description(product_n, link, header, container_client):
    # Send an HTTP request to the URL
    response_1 = requests.get(link, headers = header)
    soup_1 = BeautifulSoup(response_1.content, 'html.parser')

    list_1 = soup_1.find_all(attrs={"data-image-size": "small-retina"})
    
    
    img_names = get_image(product_n,list_1,container_client, header)
    d = create_description(soup_1)

    #writte_in_db(product_n,'Gucci',img_names,d)

def connect_azure_blob(account_name,account_key):
    
    connect_str = 'DefaultEndpointsProtocol=https;AccountName='+account_name+';AccountKey='+account_key+';EndpointSuffix=core.windows.net'

    #use the client to connect
    blob_Service_client = BlobServiceClient.from_connection_string(connect_str)

    #Use the client to connect to the container 
    container_client = blob_Service_client.get_container_client(container_name)

    return container_client

def gucci(category_url,n_products):
    

    ua = UserAgent()
    header = {'User-Agent':str(ua.chrome)}

    url = category_url

    # Send an HTTP request to the URL
    response = requests.get(url, headers = header)
    soup = BeautifulSoup(response.content, 'html.parser')

    item_list = soup.select('article a')

    # Connect to azure:
    container_client = connect_azure_blob(account_name=account_name,account_key=account_key)

    br = 0
    for item in item_list: 
        
        if br == n_products:
            break
        else:
            link = 'https://www.gucci.com' + item['href']
            scrapp_image_description(product_n=br,link=link, header=header, container_client=container_client)

        br += 1


# Define the URL you want to scrape
#EXECUTE !!!!!
url = 'https://www.gucci.com/it/it/ca/women/ready-to-wear-for-women-c-women-readytowear'



gucci(url,3)
import requests
import os
from PIL import Image
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from io import BytesIO
import pandas as pd
from openpyxl import load_workbook

def contains_required_number(line):
    
    keeping = ['001_100','004_100','005_100']
    # 001: Prod
    # 004: back
    # 005: 3/4 image
    return any(num in line for num in keeping)


def get_image(prod_number,list,output_dir, header):
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
            img_name = os.path.join(output_dir, f"Gucci{prod_number}_{i}.jpg") 
            img_resized.save(img_name)
            print(f"Saved {img_name}")

    return img_names

def create_description(soup_2):
    list_2 = soup_2.find_all(attrs={"class": "product-detail"} )
    list_2[0].p.text.replace('\n', '').replace('\t', '')

    description = ''

    for a in list_2[0].ul.find_all('li'):
        description = description + ' ' + a.text
        
    description

    return list_2[0].p.text.replace('\n', '').replace('\t', '') + ' ' + description


def writte_in_excel(ID,Brand,img_names,Description):

    #NO LETS DO IT IN DOCKER WITH SQL

    #Create a row for each product
    for image_row in img_names:
        row = []
        row.append([ID, Brand, image_row, Description])

        df = pd.DataFrame(row)

        


def scrapp_image_description(product_n, link, header):
    # Send an HTTP request to the URL
    response_1 = requests.get(link, headers = header)
    soup_1 = BeautifulSoup(response_1.content, 'html.parser')

    list_1 = soup_1.find_all(attrs={"data-image-size": "small-retina"})
    
    output_dir = "Img"
    os.makedirs(output_dir, exist_ok=True)
    
    img_names = get_image(product_n,list_1,output_dir, header)
    d = create_description(soup_1)

    writte_in_excel(product_n,'Gucci',img_names,d)



def gucci(category_url):
    

    ua = UserAgent()
    header = {'User-Agent':str(ua.chrome)}

    url = category_url

    # Send an HTTP request to the URL
    response = requests.get(url, headers = header)
    soup = BeautifulSoup(response.content, 'html.parser')

    item_list = soup.select('article a')

    br = 0
    for item in item_list: 
        
        if br == 3:
            break
        else:
            link = 'https://www.gucci.com' + item['href']
            scrapp_image_description(product_n=br,link=link, header=header)

        br += 1
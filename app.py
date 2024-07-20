import streamlit as st
import pandas as pd

import base64
from io import BytesIO
from PIL import Image

from Features import world_constructions as WCf
from Features import search_from_luxury_brands as Sf


df = WCf.world_construction.init_luxury_gallery()

df_retail = WCf.world_construction.init_retail_gallery()


def base64_to_image(base64_string):
    # Remove the data URI prefix if present
    if "data:image" in base64_string:
        base64_string = base64_string.split(",")[1]
    # Decode the Base64 string into bytes
    image_bytes = base64.b64decode(base64_string)
    return image_bytes

def create_image_from_bytes(image_bytes):
    # Create a BytesIO object to handle the image data
    image_stream = BytesIO(image_bytes)

    # Open the image using Pillow (PIL)
    image = Image.open(image_stream)
    return image

def resize_image(image, new_width):
    # Open the image

    # Calculate the new height while maintaining the aspect ratio
    original_width, original_height = image.size
    aspect_ratio = original_height / original_width
    new_height = int(new_width * aspect_ratio)

    # Resize the image
    resized_image = image.resize((new_width, new_height))

    return resized_image

def organize_data(answer):

    page_content = []
    metadata_1 = []
    metadata_2 = []
    doc_id =[]

    answers = answer['answer'].replace('Piece_1: ','').replace('Piece_2: ','').replace('Piece_3: ','').replace('Piece_4: ','').replace('Piece_5: ','').replace('\n\n','').split('*')[1:]

    for i in range(0,4):

        doc_id.append(answer['context'][i].metadata['doc_id'])
        page_content.append(answer['context'][i].page_content)
        metadata_1.append(answer['context'][i].metadata['img_1'])
        metadata_2.append(answer['context'][i].metadata['img_2'])

    df_init = pd.DataFrame([doc_id,answers, page_content,metadata_1,metadata_2]).T

    df_init = pd.DataFrame(df_init)

    df_init.rename(columns={0:"Id",1:"Answer",2:"Summary",3:"Img_1",4:"Img_2"},inplace=True)


    return df_init

    

    



vectorstore = WCf.world_construction.init_chroma_db()


#####################
###   Fuctions!   ###
#####################


# when item is selected in Clothing Gallery
selected_index = None
for index, row in df.iterrows():
    if st.session_state.get(f"select_{index}", False):
        selected_index = index

        #entity = Sf.search_similarity_from_description(df.loc[selected_index],vectorstore)
        entity = Sf.seacrh_from_luxury_brands(description=df.loc[selected_index], vectorstore=vectorstore)
        answer = entity.search_similarity_from_description()
        df_recommendations = organize_data(answer=answer)

        break



# UI

if selected_index is None:

    ##################################
    ### Screen 1: Gallery of cards ###
    ##################################


    st.title("Clothing Gallery")

    cols = st.columns(4)  # 4 cards per row
    for index, row in df.iterrows():
        with cols[index % 4]:  # cycle through columns
            st.image(
                create_image_from_bytes(image_bytes=base64_to_image(row['base64'][-len(row['base64'])+1])),  
                caption=row['Brand'])  # display the first image
            st.write(f"Price: {row['Price']}")
        
            st.button("Select", key=f"select_{index}") 


    ##################################
    ### Screen 2: Selected product ###
    ##################################

else:

    col1, col2 = st.columns([3, 7])

    with col1:
        st.write("Selected Item:")

        st.image(
            create_image_from_bytes(
                image_bytes=base64_to_image(
                    df.loc[selected_index, 'base64'][0]
                )  # display the first image
            )
        )
        st.write(f"Brand: {df.loc[selected_index, 'Brand']}")
        st.write(f"Detail: {df.loc[selected_index, 'Detail']}")
        st.write(f"Summary: {df.loc[selected_index, 'Summary']}")
        
        


    with col2:
        # Show recommendation cards on the left

        st.write("Recommendations:")
        for index, row in df_recommendations.iterrows():

            col1_img, col2_img = st.columns([5, 5])

            with col1_img:
                st.image(
                    resize_image(create_image_from_bytes(image_bytes=base64_to_image(row['Img_1'])),300)
                )

            with col2_img:
                st.image(
                    resize_image(create_image_from_bytes(image_bytes=base64_to_image(row['Img_2'])),300)
                )

            st.write(f"Brand: {df_retail[df_retail.Brand_id == int(row['Id']) ].Brand}")
            st.write(f"Price: {df_retail[df_retail.Brand_id == int(row['Id']) ].Price}")
            st.write(f"Reccomendation: {row['Answer']}")
            

        # Exit button
        st.button("Exit", key="exit")
        if st.session_state.get("exit", False):
            selected_index = None
            st.write("Exiting...")
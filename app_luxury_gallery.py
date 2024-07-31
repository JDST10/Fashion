import streamlit as st
import pandas as pd

import base64
from io import BytesIO
from PIL import Image

from Features import world_constructions as WCf
from Features import search_from_luxury_brands as Sf

model_crossencoder = WCf.world_construction.init_model_crossencoder()
df_retail = WCf.world_construction.init_retail_gallery()
df = WCf.world_construction.init_luxury_gallery()

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
        entity = Sf.seacrh_from_luxury_brands(description=df.loc[selected_index].Summary, vectorstore=vectorstore)
        df_recommendations = entity.search_similarity_from_description(df_retail=df_retail,model_crossencoder=model_crossencoder)
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

    st.button("Exit", key="exit")
    col1, col2 = st.columns([5, 5])

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
        #st.write(f"Detail: {df.loc[selected_index, 'Detail']}")
        st.write(f"Summary: {df.loc[selected_index, 'Summary']}")
        
        
    with col2:
        # Show recommendation cards on the left
        st.write("Recommendations:")

        # Exit button
        if st.session_state.get("exit", False):
            selected_index = None
            st.write("Exiting...")

        for index, row in df_recommendations.iterrows():

            col1_img, col2_img = st.columns([5, 5])

            with col1_img:
                st.image(
                    resize_image(create_image_from_bytes(image_bytes=base64_to_image(row.base64[0])),300)
                )

            with col2_img:
                st.image(
                    resize_image(create_image_from_bytes(image_bytes=base64_to_image(row.base64[1])),300)
                )

            st.write(f"Brand: {row.Brand}")
            st.write(f"Price: {row.Price}")
            st.write(f"Reccomendation: {row.explanation}")



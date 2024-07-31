import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'DB_and_Azure'))
from DB_and_Azure import sql_db_functions as SQLf, apikey

import pandas as pd
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

import getpass



class feature_extraction:

    def __init__(self,img):
        self.img = img
        self.description = None
        self.form = None

    def image_to_description(self):

        if self.description == None:
            prompt_text = f"""

            Image: {self.img}

            The images are of the same shirt or top, use them to create a detailed description of it and its style.

            Take into account the following characteristics IF APPLICABLE: 

            Fit, Sleeve style, Neckline, Material, Formality, Seasson, Colors, Texture, Transparency, Details and Embellishments, Shape,
            Length, Collar Style, Sleeve Style, Patterns, Patterns placement, Fluidity of fabric, Fabric weight, Pocket Presence, Pocket placement, 
            Pocket size, Breathability, Occasion Suitability, Lapel, etc.


            DONT DESCRIBE THE MODEL.
            Use information from the image and the description.
            IGNORE BACKGROUND     
            ANSWER MUST BE AS SPECIFIC AS POSSIBLE BUT NOT COMPLEX
            WRITE IN A SINGLE PARAGRAPH
            NAME AND DESCRIBE THE COLORS USED
            """


            os.environ['OPENAI_API_KEY'] = apikey

            # LLM
            model = ChatOpenAI(model="gpt-4o", temperature=0.5)

            # Prompt template
            prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", "You are a fashion specialist."),
                    ("user", prompt_text),
                ]
            )

            chain = prompt | model

            response = chain.invoke({})

            self.description = response.content

            return response.content
        
        else:
            return self.description
    
    def image_to_form(self):

        if self.description == None:
            description = self.image_to_description()
        else: description = self.description

        if self.form == None:

            prompt_text = """

            The images are of the same Top - Shirt piece, use them to fill the following format to list attributes of the clothing piece in image, separate them with comma:  

            *Type:  
            *Fit: (NotSlim fit, regular fit, oversized, tight, loose, etc)
            *Sleeve style: (Not Applicable, Short sleeve, long sleeve, sleeveless, cap sleeve, etc)     
            *Neckline: (Not Applicable, Crew neck, V-neck, scoop neck, etc)   
            *Material: (Cotton, linen, silk, polyester, etc)
            *Formality: (Casual, Business Casual, Formal, etc)
            *Seasson: (Winter, Spring, Summer, Autum)
            *Colors:  (percentage of each color in the clothing peace) 
            *Texture: (Smooth, Rough, Ribbed, Velvety, etc)
            *Transparency: (Opaque, Semi-transparent, Transparent, etc)
            *Details and Embellishments: (e.g, buttons, zippers, embroidery, etc)
            *Shape: (e.g., boxy, fitted, flared, etc) 
            *Length: (e.g., cropped, hip-length, tunic, etc)
            *Collar Style: (e.g., Not Applicable, crew neck, V-neck, polo, button-down)
            *Sleeve Style: (e.g., Not Applicable, short, long, three-quarter, sleeveless, puffed)
            *Patterns: (e.g., stripes, floral, geometric, not applicable)
            *Patterns placement: (e.g., lower back, left sholder, right chest, not applicable) 
            *Fluidity of fabric:
            *Fabric weight: (Light, medium, or heavy)
            *Pocket Presence:(Yes,No)
            *Pocket placement:(e.g., lower back, left sholder, right chest, not applicable)
            *Pocket size:(small, medium, big, not applicable)
            *Breathability: (Low, Medium, High)
            *Occasion Suitability: (Casual, formal, business casual, etc)
            *Lapel: (not applicable, Notch, Peak, Shawl Satin, Slim, Wide, Contrasting, etc)


            Use information from the image and the description.
            IGNORE BACKGROUND
            ONLY ANSWER THE FORMAT  
            DONT USE THE BRAND NAME IN ANY DESCRIPTION  
            IN EACH DESCRIPTION - CHARACTERISTIC SHOULD BE ITS OWN DESCRIPTION
            YOU CAN USE MULTIPLE DESCRIPTIONS IN A SINGLE ATTRIBUTE  
            DONT USE MULTICOLOR OR Multicolor, NAME THE SPECIFIC COLORS  
            COLORS SHOULD INCLUDE PRINT AND CLOTHE COLORS WITHOUT ANY DESCRIPTION OF THE PRINT ONLY MAIN COLORS
        
            """

            os.environ['OPENAI_API_KEY'] = apikey

            # LLM
            model = ChatOpenAI(model="gpt-4o", temperature=0.4)

            # Prompt template
            prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", "You are a fashion specialist."),
                    ("user", prompt_text),
                ]
            )

            chain = prompt | model

            response = chain.invoke({})

            self.form = response.content

            return response.content
        
        else:
            return self.form
        


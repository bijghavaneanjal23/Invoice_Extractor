## invoice extraction

from dotenv import load_dotenv

load_dotenv()

import streamlit as st

import os
from PIL import Image
import google.generativeai as genai

##api_key

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## function
def get_gemini_response(input,image,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response= model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data=uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type" : uploaded_file.type,
                "data":bytes_data
            }
        ]
        return image_parts

    else:
        raise FileExistsError ("No File Uploaded")
    
## Streamlit    

st.set_page_config(page_title="Invoice Extractor")
st.header("Gemini Application")
input = st.text_input("Input Prompt: ", key="input")
uploaded_file= st.file_uploader("choose an Image", type= ["jpg","jpeg","png"])
image=" "

if uploaded_file is not None:
    image= Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image" ,use_column_width=True)


submit=st.button("Tell me about the invoice")

input_prompt="""
You are an expert in understanding invoices. You will
recieve input images as invoices and you will have to 
answer questions based on the input image.

"""

## submit button is clicked

if submit:
    image_data=input_image_setup (uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    

    st.subheader("The Response is...")
    st.write(response)
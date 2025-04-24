# streamlit_app.py
import streamlit as st
from PIL import Image
from ocr_utils import preprocess_image, extract_text, extract_fields
import pandas as pd
import pytesseract
import os
if os.name == 'nt':
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


st.set_page_config(page_title="Loan Document OCR", layout="centered")

st.title("📄 Automated Personal Loan Document Processor")

uploaded_file = st.file_uploader("Upload a document (image format)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Document", use_column_width=True)

    st.subheader("Step 1: OCR Text Extraction")
    processed_img = preprocess_image(image)
    text = extract_text(processed_img)
    st.text_area("Raw OCR Text", value=text, height=200)

    st.subheader("Step 2: Extracted Key Fields")
    fields = extract_fields(text)
    edited_fields = {}
    for field, value in fields.items():
        edited_fields[field] = st.text_input(field, value)

    st.subheader("Step 3: Submit to Bank System")
    if st.button("✅ Submit Application"):
        df = pd.DataFrame([edited_fields])
        st.success("Application Submitted!")
        st.dataframe(df)
        df.to_csv("submitted_applications.csv", mode="a", index=False, header=False)


import pytesseract
from PIL import Image
import re

def preprocess_image(image):
    return image.convert("L")  

def extract_text(image):
    text = pytesseract.image_to_string(image)
    return text

def extract_fields(text):
    fields = {
        "Name": re.search(r"Name[:\-]?\s*(.*)", text, re.IGNORECASE),
        "Address": re.search(r"Address[:\-]?\s*(.*)", text, re.IGNORECASE),
        "Income": re.search(r"(Income|Salary)[:\-]?\s*₹?([\d,]+)", text, re.IGNORECASE),
        "Loan Amount": re.search(r"Loan Amount[:\-]?\s*₹?([\d,]+)", text, re.IGNORECASE),
    }
    return {key: (match.group(1) if key == "Name" or key == "Address" else match.group(2)) if match else "" for key, match in fields.items()}

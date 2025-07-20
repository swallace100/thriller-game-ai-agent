import os
import pdfplumber

def extract_text_from_pdfs(directory):
    texts = []
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(directory, filename)
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
                chunks = [line.strip() for line in text.split('\n') if line.strip()]
                texts.extend(chunks)
    return texts

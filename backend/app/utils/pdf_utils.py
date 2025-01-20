import PyPDF2

def pdf_to_string(pdf_file):
    try:
        with open(pdf_file, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = "".join(page.extract_text() or "" for page in reader.pages)
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

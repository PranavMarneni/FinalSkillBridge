import PyPDF2

def pdf_to_string(pdf_file):
    try:
        with open(pdf_file, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

pdf_path = "/Users/pranavmarneni/Downloads/ScribbleTogether-2.pdf"
pdf_text = pdf_to_string(pdf_path)
if pdf_text:
    print("PDF Text Extracted:")
    print(pdf_text)
else:
    print("No text extracted from PDF.")

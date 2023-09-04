import PyPDF2
import docx2txt
import textract
from bs4 import BeautifulSoup

FILE_DIR = Path(__file__).parent.parent + "/sources"
CFG = Config()


def extract_text_from_document(file_path):
    file_extension = file_path.split(".")[-1].lower()

    if file_extension == "pdf":
        return extract_text_from_pdf(file_path)
    elif file_extension == "docx":
        return extract_text_from_docx(file_path)
    elif file_extension == "html":
        return extract_text_from_html(file_path)


def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)
            text = ""
            for page_num in range(pdf_reader.numPages):
                text += pdf_reader.getPage(page_num).extractText()
            return text
    except Exception as e:
        print(f"Error extracting text from PDF: {str(e)}")
        return ""


def extract_text_from_docx(docx_path):
    try:
        return docx2txt.process(docx_path)
    except Exception as e:
        print(f"Error extracting text from DOCX: {str(e)}")
        return ""


def extract_text_from_html(html_path):
    try:
        with open(html_path, "r", encoding="utf-8") as html_file:
            soup = BeautifulSoup(html_file, "html.parser")
            text = soup.get_text()
            return text
    except Exception as e:
        print(f"Error extracting text from HTML: {str(e)}")
        return ""


pdf_file_paths = find_pdf_files_in_folder(folder_path)
for pdf_path in pdf_file_paths:
    extracted_text = extract_text_from_document(document_path)
    print(extracted_text)

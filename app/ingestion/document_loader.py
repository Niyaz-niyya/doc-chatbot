import pandas as pd
import PyPDF2
from typing import List, Tuple

def load_pdf(file_path: str) -> List[Tuple[str, dict]]:
    chunks = []
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            metadata = {"source": file_path, "page": page_num + 1}
            chunks.append((text, metadata))
    return chunks

def load_structured_excel(file_path: str) -> pd.DataFrame:
    return pd.read_excel(file_path)

def load_structured_csv(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)

from typing import List, Tuple
import os
import uuid
from .document_loader import load_pdf, load_structured_excel, load_structured_csv
from app.vectorstore.store_and_query import add_text_chunks, clear_collection

from app.db.save_to_db import save_dataframe_to_db

def process_document(file_path: str) -> Tuple[bool, str]:
    """
    Processes the document and determines if it's structured or unstructured.

    Returns:
        (is_structured_data: bool, table_name: str or None)
    """
    clear_collection()

    if file_path.endswith('.pdf'):
        chunks = load_pdf(file_path)
        texts = [chunk[0] for chunk in chunks]
        metadatas = [chunk[1] for chunk in chunks]
        ids = [str(uuid.uuid4()) for _ in chunks]

        summary = f"This document contains {len(texts)} pages from '{os.path.basename(file_path)}'."
        texts.insert(0, summary)
        metadatas.insert(0, {"source": os.path.basename(file_path), "type": "summary"})
        ids.insert(0, str(uuid.uuid4()))

        add_text_chunks(texts, metadatas, ids)

        return False, None  # Unstructured

    elif file_path.endswith(('.xlsx', '.xls', '.csv')):
        if file_path.endswith('.csv'):
            df = load_structured_csv(file_path)
        else:
            df = load_structured_excel(file_path)
        
        from app.db.save_to_db import save_dataframe_to_db
        table_name = save_dataframe_to_db(df, os.path.basename(file_path))
        return True, table_name  # Structured

    else:
        raise ValueError("Unsupported file type")

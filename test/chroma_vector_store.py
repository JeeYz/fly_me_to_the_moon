import chromadb
import os, sys
from typing import List

# Rich 라이브러리 임포트
from rich import print

db_path = "./.chroma_vectorstore"
target_path = "./.text_data"

def _find_files(directory: str) -> List[str]:
    pdf_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))
    return pdf_files

pdf_files = _find_files(target_path)
print("_find_files:")
print(pdf_files)





from pathlib import Path

from PyPDF2 import PdfReader
from docx import Document

class ResumeParser:
    def _extract_pdf(self, file_path: Path) -> str:
        text = ""
        with open(file_path, "rb") as file:
            pdf_reader = PdfReader(file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()


    def _extract_docx(self, file_path: Path) -> str:
        doc = Document(file_path)
        return "\n".join(
            para.text for para in doc.paragraphs).strip()

    def parse(self, file_path: Path) -> str:
        suffix = file_path.suffix.lower()
        if suffix == ".pdf":
            return self._extract_pdf(file_path)
        elif suffix == ".docx":
            return self._extract_docx(file_path)
        else:
            raise ValueError(f"Unsupported file type: {suffix}")


        
            
             
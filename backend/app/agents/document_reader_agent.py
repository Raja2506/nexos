# backend/app/agents/document_reader_agent.py
from pathlib import Path
import pandas as pd
from pypdf import PdfReader
from docx import Document
from app.agents.base_agent import BaseAgent


class DocumentReaderAgent(BaseAgent):
    """
    Reads PDF, DOCX, and CSV/Excel files and converts them into plain
    text so other agents (Research, Summarizer, QA) can work with them.
    """

    def __init__(self):
        super().__init__(name="DocumentReaderAgent")

    async def run(self, input_data: dict) -> dict:
        file_path = Path(input_data["file_path"])
        self.log(f"Reading file: {file_path.name}")

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        extension = file_path.suffix.lower()

        if extension == ".pdf":
            text = self._read_pdf(file_path)
        elif extension == ".docx":
            text = self._read_docx(file_path)
        elif extension in (".csv", ".xlsx"):
            text = self._read_tabular(file_path, extension)
        else:
            raise ValueError(f"Unsupported file type: {extension}")

        self.log(f"Extracted {len(text)} characters from {file_path.name}")
        return {"file_name": file_path.name, "text": text}

    def _read_pdf(self, file_path: Path) -> str:
        reader = PdfReader(file_path)
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages)

    def _read_docx(self, file_path: Path) -> str:
        doc = Document(file_path)
        paragraphs = [p.text for p in doc.paragraphs]
        return "\n".join(paragraphs)

    def _read_tabular(self, file_path: Path, extension: str) -> str:
        if extension == ".csv":
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
        # Convert to a readable text table instead of raw dataframe repr
        return df.to_string(index=False)
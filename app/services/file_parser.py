from abc import ABC, abstractmethod
import fitz
import os

# Abstract Strategy
class TextExtractorStrategy(ABC):
    @abstractmethod
    def extract_text(self, file_path):
        pass

# Concrete Strategy for PDF
class PDFTextExtractor(TextExtractorStrategy):
    def extract_text(self, pdf_path):
        document = fitz.open(pdf_path)
        text = ""
        fonts = defaultdict(int)
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            text += page.get_text("text")
        return text

# Context class
class TextExtractor:
    def __init__(self):
        self.parsers = {
            '.pdf': PDFTextExtractor(),
        }

    def extract_text(self, file_path):
        _, ext = os.path.splitext(file_path)
        parser = self.parsers.get(ext.lower())
        if parser is not None:
            return parser.extract_text(file_path)
        else:
            raise ValueError(f"No parser available for file extension '{ext}'")
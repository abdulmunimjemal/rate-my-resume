from abc import ABC, abstractmethod
import docx
import fitz
import os
import zipfile, re
from collections import defaultdict
from app.utils.scoring_utils import format_fonts

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
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                for line in block["lines"]:
                    for span in line["spans"]:
                        font_key = (span["font"], span["size"])
                        fonts[font_key] += 1
                        
        num_pages = len(document)
        fonts = format_fonts(fonts)
        return text, num_pages, fonts

# Concrete Strategy for DOCX
class DOCXTextExtractor(TextExtractorStrategy):
    def extract_text(self, docx_path):
        doc = docx.Document(docx_path)
        num_pages = DOCXTextExtractor.get_docx_page_count(docx_path)
        text = ""
        fonts = defaultdict(int)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
            for run in paragraph.runs:
                font_key = (run.font.name, run.font.size.pt if run.font.size else None)
                fonts[font_key] += 1
        fonts = format_fonts(fonts)
        return text, num_pages, fonts
    
    @staticmethod
    def get_docx_page_count(docx_fpath):
        docx_object = zipfile.ZipFile(docx_fpath)
        docx_property_file_data = docx_object.read('docProps/app.xml').decode()
        page_count = re.search(r"<Pages>(\d+)</Pages>", docx_property_file_data).group(1)
        return int(page_count)

# Context class
class TextExtractor:
    def __init__(self):
        self.parsers = {
            '.pdf': PDFTextExtractor(),
            '.docx': DOCXTextExtractor()
        }

    def extract_text(self, file_path):
        _, ext = os.path.splitext(file_path)
        parser = self.parsers.get(ext.lower())
        if parser is not None:
            return parser.extract_text(file_path)
        else:
            raise ValueError(f"No parser available for file extension '{ext}'")

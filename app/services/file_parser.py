import asyncio
from abc import ABC, abstractmethod
import docx
import fitz
import os
import zipfile, re
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from app.utils.scoring_utils import format_fonts

# Abstract Strategy
class TextExtractorStrategy(ABC):
    @abstractmethod
    async def extract_text(self, file_path):
        pass

# Concrete Strategy for PDF
class PDFTextExtractor(TextExtractorStrategy):
    async def extract_text(self, pdf_path):
        loop = asyncio.get_event_loop()
        document = fitz.open(pdf_path)
        text = []
        fonts = Counter()

        def process_page(page_num):
            page = document.load_page(page_num)
            page_text = page.get_text("text")
            text.append(page_text)
            blocks = page.get_text("dict")["blocks"]
            local_fonts = Counter()
            for block in blocks:
                for line in block["lines"]:
                    for span in line["spans"]:
                        font_key = (span["font"], span["size"])
                        local_fonts[font_key] += 1
            return local_fonts

        with ThreadPoolExecutor() as executor:
            results = await asyncio.gather(
                *[loop.run_in_executor(executor, process_page, page_num) for page_num in range(len(document))]
            )

        for result in results:
            fonts.update(result)
        
        num_pages = len(document)
        combined_text = "".join(text)
        fonts = format_fonts(fonts)
        return combined_text, num_pages, fonts

# Concrete Strategy for DOCX
class DOCXTextExtractor(TextExtractorStrategy):
    async def extract_text(self, docx_path):
        loop = asyncio.get_event_loop()
        doc = docx.Document(docx_path)
        num_pages = await DOCXTextExtractor.get_docx_page_count(docx_path)
        text = []
        fonts = Counter()

        for paragraph in doc.paragraphs:
            text.append(paragraph.text + "\n")
            for run in paragraph.runs:
                font_key = (run.font.name, run.font.size.pt if run.font.size else None)
                fonts[font_key] += 1
        
        combined_text = "".join(text)
        fonts = format_fonts(fonts)
        return combined_text, num_pages, fonts
    
    @staticmethod
    async def get_docx_page_count(docx_fpath):
        loop = asyncio.get_event_loop()
        
        def read_docx_properties():
            with zipfile.ZipFile(docx_fpath) as docx_object:
                docx_property_file_data = docx_object.read('docProps/app.xml').decode()
                page_count = re.search(r"<Pages>(\d+)</Pages>", docx_property_file_data).group(1)
            return int(page_count)

        page_count = await loop.run_in_executor(None, read_docx_properties)
        return page_count

# Context class
class TextExtractor:
    def __init__(self):
        self.parsers = {
            '.pdf': PDFTextExtractor(),
            '.docx': DOCXTextExtractor()
        }

    async def extract_text(self, file_path):
        _, ext = os.path.splitext(file_path)
        parser = self.parsers.get(ext.lower())
        if parser is not None:
            return await parser.extract_text(file_path)
        else:
            raise ValueError(f"No parser available for file extension '{ext}'")
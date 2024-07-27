from abc import ABC, abstractmethod
import docx
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
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            text += page.get_text("text")
        num_pages = len(document)
        return text, num_pages

# Concrete Strategy for DOCX
class DOCXTextExtractor(TextExtractorStrategy):
    def extract_text(self, docx_path):
        doc = docx.Document(docx_path)
        num_pages = get_docx_page_count(docx_path)
        text = ""
        fonts = defaultdict(int)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        fonts = format_fonts(dict(fonts))
        return text, num_pages
    
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
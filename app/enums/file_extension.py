from enum import Enum

class AllowedFileExtension(str, Enum):
    PDF = ".pdf"
    DOCX = ".docx"
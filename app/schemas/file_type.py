from enum import Enum

class FileType(str, Enum):
    PDF_CO = "pdf_co"
    PDF_INVOICE = "pdf_invoice"
    IMAGE_STORAGE = "image_storage"
    LOCAL_STORAGE = "local_storage"

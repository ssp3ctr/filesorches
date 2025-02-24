from enum import Enum


class FileType(str, Enum):
    PDF_CO = "pdf_co"
    PDF_INVOICE = "pdf_invoice"
    PDF_SPEC = "pdf_spec"
    PRODUCT_IMAGE = "product_image"

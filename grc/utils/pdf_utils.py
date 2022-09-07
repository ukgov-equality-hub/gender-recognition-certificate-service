import fitz
from io import BytesIO
from typing import List
from xhtml2pdf import pisa


def create_pdf_from_html(html: str) -> BytesIO:
    pdf_stream: BytesIO = BytesIO()
    pisa.CreatePDF(html, dest=pdf_stream)

    pdf_stream.seek(0)
    return pdf_stream


def merge_pdfs(input_pdf_streams: List[BytesIO]) -> BytesIO:
    output_fitz_pdf_document: fitz.Document = fitz.open()

    for input_pdf_stream in input_pdf_streams:
        input_pdf_stream.seek(0)
        input_fits_pdf_document: fitz.Document = fitz.open(stream=input_pdf_stream, filetype='pdf')
        output_fitz_pdf_document.insert_pdf(input_fits_pdf_document)
        input_fits_pdf_document.close()

    output_pdf_stream: BytesIO = BytesIO()
    output_fitz_pdf_document.save(output_pdf_stream)
    output_fitz_pdf_document.close()

    output_pdf_stream.seek(0)
    return output_pdf_stream


def is_pdf_password_protected(pdf_stream: BytesIO) -> bool:
    pdf_stream.seek(0)

    fitz_pdf_document: fitz.Document = fitz.open(stream=pdf_stream, filetype='pdf')
    needs_password = fitz_pdf_document.needs_pass

    fitz_pdf_document.close()
    return needs_password


def is_pdf_password_correct(pdf_stream: BytesIO, password: str) -> bool:
    pdf_stream.seek(0)

    fitz_pdf_document: fitz.Document = fitz.open(stream=pdf_stream, filetype='pdf')

    needs_password = fitz_pdf_document.needs_pass
    password_correct = False
    if needs_password:
        password_correct = fitz_pdf_document.authenticate(password)

    fitz_pdf_document.close()
    return needs_password and password_correct


def remove_pdf_password_protection(input_pdf_stream: BytesIO, password: str) -> BytesIO:
    input_pdf_stream.seek(0)

    input_fitz_pdf_document: fitz.Document = fitz.open(stream=input_pdf_stream, filetype='pdf')
    input_fitz_pdf_document.authenticate(password)

    output_fitz_pdf_document: fitz.Document = fitz.open()
    output_fitz_pdf_document.insert_pdf(input_fitz_pdf_document)
    input_fitz_pdf_document.close()

    output_pdf_stream: BytesIO = BytesIO()
    output_fitz_pdf_document.save(output_pdf_stream)
    output_fitz_pdf_document.close()

    output_pdf_stream.seek(0)
    return output_pdf_stream


def remove_pdf_edit_protection(input_pdf_stream: BytesIO) -> BytesIO:
    input_pdf_stream.seek(0)

    input_fitz_pdf_document: fitz.Document = fitz.open(stream=input_pdf_stream, filetype='pdf')

    output_fitz_pdf_document: fitz.Document = fitz.open()
    output_fitz_pdf_document.insert_pdf(input_fitz_pdf_document)
    input_fitz_pdf_document.close()

    output_pdf_stream: BytesIO = BytesIO()
    output_fitz_pdf_document.save(output_pdf_stream)
    output_fitz_pdf_document.close()

    output_pdf_stream.seek(0)
    return output_pdf_stream

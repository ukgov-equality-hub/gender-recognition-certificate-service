import fitz
from io import BytesIO
from typing import Any, List
from flask import make_response
from xhtml2pdf import pisa
from grc.utils.logger import LogLevel, Logger

logger = Logger()


class PDFUtils():
    def __init__(self):
        pass


    def create_pdf_from_html(self, html: str, title: str = None) -> BytesIO:
        pdf_stream: BytesIO = BytesIO()
        pisa.CreatePDF(html, dest=pdf_stream)

        pdf_stream.seek(0)

        if title:
            pdf_stream = self.add_pdf_toc(pdf_stream, title)

        return pdf_stream


    def merge_pdfs(self, input_pdf_streams: List[BytesIO], update_toc: bool = True) -> BytesIO:
        output_fitz_pdf_document: fitz.Document = fitz.open()

        page_count = 1
        new_toc = []
        current_section = ''

        for input_pdf_stream in input_pdf_streams:
            input_pdf_stream.seek(0)
            input_fitz_pdf_document: fitz.Document = fitz.open(stream=input_pdf_stream, filetype='pdf')

            if update_toc:
                toc = input_fitz_pdf_document.get_toc()
                for t in toc:
                    if t[1][: 2] == '__':
                        this_section = t[1][2: ]
                        this_file = ''
                        if ':' in this_section:
                            this_file = this_section[this_section.index(':') + 1:]
                            this_section = this_section[: this_section.index(':')]

                        if current_section != this_section:
                            new_toc.append([1, this_section, t[2] + page_count - 1])
                        if this_file != '':
                            new_toc.append([2, this_file, t[2] + page_count - 1])

                        current_section = this_section

                page_count += len(input_fitz_pdf_document)

            if input_fitz_pdf_document.is_form_pdf:
                input_fitz_pdf_document = self.flatten_form_pdf(input_fitz_pdf_document)

            output_fitz_pdf_document.insert_pdf(input_fitz_pdf_document)
            input_fitz_pdf_document.close()

        if update_toc:
            output_fitz_pdf_document.set_toc(new_toc)

        output_pdf_stream: BytesIO = BytesIO()
        output_fitz_pdf_document.ez_save(output_pdf_stream)
        output_fitz_pdf_document.close()

        output_pdf_stream.seek(0)
        return output_pdf_stream


    def is_pdf_password_protected(self, pdf_stream: BytesIO) -> bool:
        pdf_stream.seek(0)

        fitz_pdf_document: fitz.Document = fitz.open(stream=pdf_stream, filetype='pdf')
        needs_password = fitz_pdf_document.needs_pass

        fitz_pdf_document.close()
        return needs_password


    def is_pdf_form(self, pdf_stream: BytesIO) -> bool:
        pdf_stream.seek(0)

        fitz_pdf_document: fitz.Document = fitz.open(stream=pdf_stream, filetype='pdf')
        is_form_pdf = fitz_pdf_document.is_form_pdf

        fitz_pdf_document.close()
        return is_form_pdf


    def is_pdf_password_correct(self, pdf_stream: BytesIO, password: str) -> bool:
        pdf_stream.seek(0)

        fitz_pdf_document: fitz.Document = fitz.open(stream=pdf_stream, filetype='pdf')

        needs_password = fitz_pdf_document.needs_pass
        password_correct = False
        if needs_password:
            password_correct = fitz_pdf_document.authenticate(password)

        fitz_pdf_document.close()
        return needs_password and password_correct


    def remove_pdf_password_protection(self, input_pdf_stream: BytesIO, password: str) -> BytesIO:
        input_pdf_stream.seek(0)

        input_fitz_pdf_document: fitz.Document = fitz.open(stream=input_pdf_stream, filetype='pdf')
        input_fitz_pdf_document.authenticate(password)

        output_fitz_pdf_document: fitz.Document = fitz.open()
        if input_fitz_pdf_document.is_form_pdf:
            input_fitz_pdf_document = self.flatten_form_pdf(input_fitz_pdf_document)
        output_fitz_pdf_document.insert_pdf(input_fitz_pdf_document)
        input_fitz_pdf_document.close()

        output_pdf_stream: BytesIO = BytesIO()
        output_fitz_pdf_document.ez_save(output_pdf_stream)
        output_fitz_pdf_document.close()

        output_pdf_stream.seek(0)
        return output_pdf_stream


    def remove_pdf_edit_protection(self, input_pdf_stream: BytesIO) -> BytesIO:
        input_pdf_stream.seek(0)

        input_fitz_pdf_document: fitz.Document = fitz.open(stream=input_pdf_stream, filetype='pdf')

        output_fitz_pdf_document: fitz.Document = fitz.open()
        if input_fitz_pdf_document.is_form_pdf:
            input_fitz_pdf_document = self.flatten_form_pdf(input_fitz_pdf_document)
        output_fitz_pdf_document.insert_pdf(input_fitz_pdf_document)
        input_fitz_pdf_document.close()

        output_pdf_stream: BytesIO = BytesIO()
        output_fitz_pdf_document.ez_save(output_pdf_stream)
        output_fitz_pdf_document.close()

        output_pdf_stream.seek(0)
        return output_pdf_stream


    def flatten_form_pdf(self, input_fitz_pdf_document: fitz.Document) -> fitz.Document:
        output_fitz_pdf_document: fitz.Document = fitz.open()

        for page in input_fitz_pdf_document:
            try:
                pix = page.get_pixmap(dpi=150)
                new_page = output_fitz_pdf_document.new_page(pno=-1)
                new_page.insert_image(rect=new_page.bound(), pixmap=pix)
            except Exception as e:
                logger.log(LogLevel.ERROR, e)

        return output_fitz_pdf_document


    def flatten_form_pdf_stream(self, input_pdf_stream: BytesIO) -> BytesIO:
        input_pdf_stream.seek(0)

        input_fitz_pdf_document: fitz.Document = fitz.open(stream=input_pdf_stream, filetype='pdf')
        flattened_pdf_document = self.flatten_form_pdf(input_fitz_pdf_document)

        output_pdf_stream: BytesIO = BytesIO()
        flattened_pdf_document.ez_save(output_pdf_stream)
        flattened_pdf_document.close()

        output_pdf_stream.seek(0)
        return output_pdf_stream


    def add_pdf_toc(self, input_pdf_document: BytesIO, title: str) -> BytesIO:
        fitz_pdf_document: fitz.Document = fitz.open(stream=input_pdf_document, filetype='pdf')
        fitz_pdf_document.set_toc([[1, f'__{title}', 1]])

        output_pdf_stream: BytesIO = BytesIO()
        fitz_pdf_document.ez_save(output_pdf_stream)
        fitz_pdf_document.close()

        output_pdf_stream.seek(0)
        return output_pdf_stream


    def create_pdf_toc(self, input_pdf_document: BytesIO, toc_levels: int = 9) -> BytesIO:
        input_fitz_pdf_document: fitz.Document = fitz.open(stream=input_pdf_document, filetype='pdf')
        toc = input_fitz_pdf_document.get_toc()
        toc_html = self.get_toc_html(toc, toc_levels, 0)
        test_contents_page = self.create_pdf_from_html(toc_html)
        number_of_contents_pages = self.get_pdf_number_of_pages(test_contents_page)
        toc_html = self.get_toc_html(toc, toc_levels, number_of_contents_pages)

        pdfs = []
        contents_page = self.create_pdf_from_html(toc_html)
        pdfs.append(contents_page)
        pdfs.append(input_pdf_document)
        output_pdf_document = self.merge_pdfs(pdfs, update_toc=False)

        fitz_pdf_document: fitz.Document = fitz.open(stream=output_pdf_document, filetype='pdf')
        new_toc = []
        for t in toc:
            if t[0] < toc_levels:
                new_toc.append([t[0], t[1], t[2] + number_of_contents_pages])
        fitz_pdf_document.set_toc(new_toc)

        output_pdf_stream: BytesIO = BytesIO()
        fitz_pdf_document.ez_save(output_pdf_stream)
        fitz_pdf_document.close()

        output_pdf_stream.seek(0)
        return output_pdf_stream


    def get_toc_html(self, toc: Any, toc_levels: int, page_adjust: int = 0) -> str:
        toc_html = '<h1 style="font-family: Arial; font-size: 24px;">CONTENTS</h1><p>&nbsp;</p><p>&nbsp;</p><table>'
        for t in toc:
            if t[0] < toc_levels:
                toc_html += f'<tr> \
                                <td style="padding: 0 0 5px {t[0]}0px; font-family: Arial; font-size: 16px;">{t[1]}</td> \
                                <td style="width: 30px; padding: 0 0 5px 0; text-align: right; font-family: Arial; font-size: 16px;">{t[2] + page_adjust}</td> \
                            </tr>'
        toc_html += '</table>'
        return toc_html


    def paginate_pdf(self, input_pdf_document: BytesIO) -> BytesIO:
        input_fitz_pdf_document: fitz.Document = fitz.open(stream=input_pdf_document, filetype='pdf')

        try:
            fontsize = 12
            fontname = 'helv'
            colour = (0, 0, 0)

            for idx, page in enumerate(input_fitz_pdf_document):
                page = input_fitz_pdf_document[idx]
                text = str(idx + 1)
                text_length = fitz.get_text_length(text, fontname=fontname, fontsize=fontsize)

                rect_x1 = (page.bound()[2] / 2) - (text_length / 2)
                rect_y1 = page.bound()[3] - 35
                rect_x2 = rect_x1 + text_length + 2
                rect_y2 = rect_y1 + fontsize + 2
                rect = (rect_x1, rect_y1, rect_x2, rect_y2)

                #page.draw_rect(rect, color=colour)
                page.insert_textbox(rect, text, fontsize=fontsize, fontname=fontname, color=colour, border_width=0, align=1)
        except Exception as e:
            logger.log(LogLevel.ERROR, e)

        output_pdf_stream: BytesIO = BytesIO()
        input_fitz_pdf_document.ez_save(output_pdf_stream)
        input_fitz_pdf_document.close()

        output_pdf_stream.seek(0)
        return output_pdf_stream


    def get_filename_without_pdf_extension(self, input_file_name: str) -> str:
        if input_file_name.lower().endswith('.pdf'):
            return input_file_name[:-4]
        return input_file_name


    def get_pdf_number_of_pages(self, input_pdf_document: BytesIO) -> int:
        fitz_pdf_document: fitz.Document = fitz.open(stream=input_pdf_document, filetype='pdf')
        number_of_pages = len(fitz_pdf_document)
        fitz_pdf_document.close()

        return number_of_pages


    def make_pdf_download_response(self, pdf_bytes, output_file_name):
        response = make_response(pdf_bytes)
        response.headers.set('Content-Type', 'application/pdf')
        response.headers.set('Content-Disposition', 'attachment', filename=output_file_name)
        return response

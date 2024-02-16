import json
import os
import re
import html

import concurrent
from concurrent.futures import ThreadPoolExecutor
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak


def write_data(output_file: str, data: dict, mode: str) -> None:
    if mode == "pdf":
        generate_pdf_report(data=data, output_filename=output_file)
    elif mode == "json":
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f)


class FastCanvas(canvas.Canvas):
    def showPage(self):
        self._startPage()
        self._doPage()


def generate_pdf_report(data, output_filename):
    module_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(module_dir, "fonts", "dejavu-serif.ttf")
    pdfmetrics.registerFont(TTFont('DejaVuSerif', font_path, 'UTF-8'))
    domain_regex = re.compile(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

    def format_value(value_data, value_style, depth=0):
        indent = "&nbsp;" * (depth * 8)

        def string_handle(string):
            if domain_regex.match(string):
                return f"<a href='https://{html.escape(string)}'>{string}</a>"
            elif string.startswith('https://'):
                return f"<u><a href='{html.escape(string)}'>{string.replace('https://', '').split('/')[0]}</a></u>"
            return string

        def extra_br_dict(sub_value):
            return '<br/>' if isinstance(sub_value, dict) else ''

        def extra_br_list(sub_value):
            return '<br/>' if all(isinstance(el, dict) for el in sub_value) else ''

        def dict_handle(dict_data):
            formatted_value_data = "<br/>".join(
                [f"{extra_br_dict(sub_value)}<font color='blue'><b>{indent}{key}: </b></font>"
                 f"{format_value(sub_value, value_style, depth + 1)}{extra_br_dict(sub_value)}"
                 for key, sub_value in dict_data.items()])
            return f"<br/>{formatted_value_data}"

        def list_handle(list_value):
            formatted_value_data = "<br/>".join(
                [f"{indent}{format_value(item, value_style, depth + 1)}"
                 for item in list_value])
            return f"<br/>{formatted_value_data}{extra_br_list(list_value)}"

        if isinstance(value_data, dict):
            return dict_handle(value_data)
        elif isinstance(value_data, list):
            return list_handle(value_data)
        else:
            return string_handle(str(value_data))

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontName='DejaVuSerif',
        fontSize=20,
        leftIndent=-50,
        leading=12,
    )
    content_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontName='DejaVuSerif',
        fontSize=8,
        leftIndent=-50,
        leading=10,
    )

    def make_pages(canvas, doc_):
        canvas.saveState()
        canvas.rect(10, 10, A4[0] - 20, A4[1] - 20, fill=0)
        canvas.setFont('DejaVuSerif', 8)
        canvas.drawString(A4[0] // 2, A4[1] // 25, "%d" % doc_.page)
        canvas.restoreState()

    def make_first_page(canvas, doc_) -> None:
        canvas.saveState()
        canvas.setFont('DejaVuSerif', 40)
        canvas.drawString(A4[0] // 2, A4[1] // 2, "%s" % "OSINT Report")
        canvas.restoreState()

    story = []

    def build_page(service_name, value_data):
        temp_story = []
        if value_data:
            title = Paragraph(service_name, title_style)
            temp_story.append(title)
            formatted_value = format_value(value_data, content_style)
            if formatted_value:
                formatted_value = formatted_value.replace('<br/><br/><br/>','<br/><br/>')
                formatted_value = Paragraph(formatted_value, content_style)

                temp_story.append(formatted_value)
                temp_story.append(PageBreak())
        story.extend(temp_story)

    with ThreadPoolExecutor() as executor:
        futures = []

        for service, value in data.items():
            if not value:
                continue

            futures.append(executor.submit(build_page, service, value))

        for future in concurrent.futures.as_completed(futures):
            future.result()

    doc = SimpleDocTemplate(output_filename, pagesize=A4, canvasmaker=FastCanvas)
    doc.build([PageBreak()] + story, onFirstPage=make_first_page, onLaterPages=make_pages)


def main():
    pass


if __name__ == "__main__":
    main()

import json
import os
import re


from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak


def generate_tree(pdf: list, data: dict | list | str, level: int = 0, font_size: int = None) -> None:
    styles = getSampleStyleSheet()
    indent = level * 25

    if font_size is None:
        font_size = 20

    def set_key_page_style(page_style):
        page_style.fontName = 'DejaVuSerif'
        page_style.leftIndent = indent
        page_style.fontSize = font_size
        page_style.textColor = (0, 0, 0.8)
        return page_style

    def set_value_page_style(page_style):
        page_style.fontName = 'DejaVuSerif'
        page_style.leftIndent = indent
        page_style.fontSize = 14
        page_style.leading = font_size * 0.95
        page_style.spaceBefore = 0
        page_style.spaceAfter = 0
        return page_style

    def set_zero_ident_style(page_style):
        page_style.fontSize = 28
        page_style.alignment = 1
        page_style.textColor = (0.5, 0.2, 0.8)
        return page_style

    def set_non_zero_ident_style(page_style):
        page_style.spaceBefore = 0
        page_style.spaceAfter = 0
        return page_style

    def add_key_paragraph(text: str, page_style):
        clean_text = re.sub(r'<.*?>', '', str(text))
        paragraph = Paragraph(clean_text, page_style)
        paragraph.keepWithNext = True
        return paragraph

    def add_value_paragraph(text: str, page_style):
        clean_text = re.sub(r'<.*?>', '', str(text))
        paragraph = Paragraph(clean_text, page_style)
        return paragraph

    if isinstance(data, dict):
        for key, value in data.items():
            key_style = styles['Heading1']
            key_style = set_key_page_style(key_style)
            if indent == 0:
                pdf.append(PageBreak())
                key_style = set_zero_ident_style(key_style)
            else:
                key_style = set_non_zero_ident_style(key_style)
            key_paragraph = add_key_paragraph(key, key_style)
            pdf.append(key_paragraph)
            generate_tree(pdf, value, level + 1, font_size - 1)
    elif isinstance(data, list):
        for item in data:
            generate_tree(pdf, item, level + 1, font_size - 1)
    else:
        value_style = styles['Normal']
        value_style = set_value_page_style(value_style)
        value_paragraph = add_value_paragraph(data, value_style)
        pdf.append(value_paragraph)


def generate_pdf_report(data: dict, output_file: str) -> None:
    module_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(module_dir, "fonts", "dejavu-serif.ttf")
    pdfmetrics.registerFont(TTFont('DejaVuSerif', font_path, 'UTF-8'))

    pdf = SimpleDocTemplate(output_file, pagesize=A4, topMargin=0.25 * inch)

    styles = getSampleStyleSheet()
    styles['Heading1'].fontName = 'DejaVuSerif'

    artwork = styles['Normal']

    elements = [Paragraph("", artwork), Spacer(1, 0.5 * inch)]
    generate_tree(elements, data)

    def make_pages(canvas, doc) -> None:
        canvas.saveState()
        canvas.rect(10, 10, A4[0]-20, A4[1]-20, fill=0)
        canvas.setFont('DejaVuSerif', 8)
        canvas.drawString(A4[0] // 2, 15, "%d" % doc.page)
        canvas.restoreState()

    def make_first_page(canvas, doc) -> None:
        canvas.saveState()
        canvas.setFont('DejaVuSerif', 40)
        canvas.drawString(A4[0] // 2, A4[1] // 2, "%s" % "OSINT Report")
        canvas.restoreState()

    pdf.build(elements, onFirstPage=make_first_page, onLaterPages=make_pages)


def write_data(output_file: str, data: dict, mode: str) -> None:
    if mode == "pdf":
        generate_pdf_report(data=data, output_file=output_file)
    elif mode == "json":
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f)


def main():
    pass


if __name__ == "__main__":
    main()

import json
import os
import re


from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak


def generate_tree(pdf, data, level=0, font_size=None):
    styles = getSampleStyleSheet()
    indent = level * 25

    if font_size is None:
        font_size = 20

    if isinstance(data, dict):
        for key, value in data.items():
            key_style = styles['Heading1']
            styles['Heading1'].fontName = 'DejaVuSerif'
            key_style.leftIndent = indent
            key_style.fontSize = font_size
            key_style.textColor = (0, 0, 0.8)
            if indent == 0:
                pdf.append(PageBreak())
                key_style.fontSize = 28
                key_style.alignment = 1
                key_style.textColor = (0.5, 0.2, 0.8)
            else:
                key_style.spaceBefore = 0
                key_style.spaceAfter = 0
            clean_text = re.sub(r'<.*?>', '', str(key))
            key_paragraph = Paragraph(clean_text, key_style)
            key_paragraph.keepWithNext = True
            pdf.append(key_paragraph)
            generate_tree(pdf, value, level + 1, font_size - 1)
    elif isinstance(data, list):
        for item in data:
            generate_tree(pdf, item, level + 1, font_size - 1)
    else:
        value_style = styles['Normal']
        styles['Normal'].fontName = 'DejaVuSerif'
        value_style.leftIndent = indent
        value_style.fontSize = 14
        value_style.leading = font_size * 0.95
        value_style.spaceBefore = 0
        value_style.spaceAfter = 0
        clean_text = re.sub(r'<.*?>', '', str(data))
        pdf.append(Paragraph(clean_text, value_style))


def generate_pdf_report(data, output_file):
    module_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(module_dir, "fonts", "dejavu-serif.ttf")
    pdfmetrics.registerFont(TTFont('DejaVuSerif', font_path, 'UTF-8'))

    pdf = SimpleDocTemplate(output_file, pagesize=A4, topMargin=0.25 * inch)

    styles = getSampleStyleSheet()
    styles['Heading1'].fontName = 'DejaVuSerif'

    artwork = styles['Normal']

    elements = [Paragraph("", artwork), Spacer(1, 0.5 * inch)]
    generate_tree(elements, data)

    def myLaterPages(canvas, doc):
        canvas.saveState()
        canvas.rect(10, 10, A4[0]-20, A4[1]-20, fill=0)
        canvas.setFont('DejaVuSerif', 8)
        canvas.drawString(A4[0] // 2, 15, "%d" % doc.page)
        canvas.restoreState()

    def myFirstPage(canvas, doc):
        canvas.saveState()
        canvas.setFont('DejaVuSerif', 40)
        canvas.drawString(A4[0] // 2, A4[1] // 2, "%s" % "OSINT Report")
        canvas.restoreState()

    pdf.build(elements, onFirstPage=myFirstPage, onLaterPages=myLaterPages)


def write_data(output_file, data, mode):
    if mode == "pdf":
        generate_pdf_report(data=data, output_file=output_file)
    elif mode == "json":
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f)


def main():
    pass


if __name__ == "__main__":
    main()

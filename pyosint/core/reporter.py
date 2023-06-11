from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


def generate_tree(pdf, data, level=0):
    styles = getSampleStyleSheet()
    indent = level * 10

    if isinstance(data, dict):
        for key, value in data.items():
            key_style = styles['Heading1']
            styles['Heading1'].fontName = 'DejaVuSerif'
            key_style.leftIndent = indent
            pdf.append(Paragraph(str(key.replace('<img>', 'img').replace('<a>', 'a')), key_style))
            generate_tree(pdf, value, level + 1)
    elif isinstance(data, list):
        for item in data:
            generate_tree(pdf, item, level + 1)
    else:
        value_style = styles['Normal']
        styles['Normal'].fontName = 'DejaVuSerif'
        value_style.leftIndent = indent
        pdf.append(Paragraph(str(data).encode('utf-8'), value_style))
    pdf.append(Spacer(1, 0.1 * inch))


def generate_pdf_report(data, output_file):
    pdfmetrics.registerFont(TTFont('DejaVuSerif', '../../fonts/dejavu-serif.ttf', 'UTF-8'))
    pdf = SimpleDocTemplate(output_file, pagesize=letter)
    styles = getSampleStyleSheet()
    styles['Heading1'].fontName = 'DejaVuSerif'
    elements = [Paragraph("OSINT Report", styles['Heading1']), Spacer(1, 0.5 * inch)]
    generate_tree(elements, data)
    pdf.build(elements)


def main():
    pass


if __name__ == "__main__":
    main()

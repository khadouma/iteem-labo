from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def render_to_pdf(template_path,output, context):
    template = get_template(template_path)
    html = template.render({"obj":context})
    pdf_file = HttpResponse(content_type='application/pdf')
    pdf_file['Content-Disposition'] = f'inline; filename={output}'

    pisa_status = pisa.CreatePDF(html, dest=pdf_file)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return pdf_file


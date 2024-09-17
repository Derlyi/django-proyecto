# utils.py
from io import BytesIO
from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa
from .models import Order

def generate_invoice_pdf(order_id):
    # Obtener el pedido
    order = Order.objects.get(id=order_id)
    
    # Renderizar la plantilla HTML con el pedido
    html = render_to_string('orders/order/invoice.html', {'order': order})
    
    # Crear un buffer en memoria para el PDF
    buffer = BytesIO()
    
    # Convertir HTML a PDF
    pdf = pisa.CreatePDF(BytesIO(html.encode('utf-8')), dest=buffer)
    
    # Obtener el contenido del PDF
    pdf_content = buffer.getvalue()
    buffer.close()
    
    # Crear una respuesta HTTP para el archivo PDF
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order_id}.pdf"'
    
    return response

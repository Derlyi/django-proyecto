# utils.py
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from .models import Order

def create_invoice_pdf(order_id):
    # Obtener el pedido
    order = Order.objects.get(id=order_id)
    
    # Crear un buffer en memoria para el PDF
    buffer = BytesIO()
    
    # Crear un objeto Canvas para el PDF
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Títulos y detalles
    c.drawString(1 * inch, height - 1 * inch, f"Invoice #{order.id}")
    c.drawString(1 * inch, height - 1.5 * inch, f"Date: {order.created.strftime('%Y-%m-%d')}")
    c.drawString(1 * inch, height - 2 * inch, f"Name: {order.first_name} {order.last_name}")
    c.drawString(1 * inch, height - 2.5 * inch, f"Email: {order.email}")
    c.drawString(1 * inch, height - 3 * inch, f"Address: {order.address}")
    c.drawString(1 * inch, height - 3.5 * inch, f"Postal Code: {order.postal_code}")
    c.drawString(1 * inch, height - 4 * inch, f"City: {order.city}")
    
    y_position = height - 5 * inch

    c.drawString(1 * inch, y_position, "Order Details:")
    y_position -= 0.5 * inch

    for item in order.items.all():
        c.drawString(1 * inch, y_position, f"{item.quantity}x {item.product.name} - ${item.price}")
        y_position -= 0.25 * inch

    c.drawString(1 * inch, y_position, f"Total: ${order.get_total_cost()}")

    # Finalizar el PDF
    c.showPage()
    c.save()

    # Obtener el contenido del PDF
    pdf_content = buffer.getvalue()
    buffer.close()

    # Crear una respuesta HTTP para el archivo PDF
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order_id}.pdf"'
    
    return response

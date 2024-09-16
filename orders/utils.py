from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from .models import Order, OrderItem

def generate_invoice_pdf(order_id):
    # Obtén el pedido y los elementos del pedido
    order = Order.objects.get(id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    
    # Crea un objeto de respuesta HTTP para devolver el archivo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order_id}.pdf"'
    
    # Crea un documento PDF
    p = canvas.Canvas(response, pagesize=letter)
    
    # Dibuja el encabezado de la factura
    p.drawString(100, 750, f"Invoice for Order #{order_id}")
    p.drawString(100, 735, f"Date: {order.created_at.strftime('%Y-%m-%d')}")
    
    # Dibuja los detalles del pedido
    y = 700
    for item in order_items:
        p.drawString(100, y, f"Product: {item.product.name}")
        p.drawString(300, y, f"Quantity: {item.quantity}")
        p.drawString(400, y, f"Price: ${item.price:.2f}")
        y -= 15
    
    # Dibuja el monto total
    total = sum(item.price * item.quantity for item in order_items)
    p.drawString(100, y - 30, f"Total: ${total:.2f}")
    
    # Finaliza el documento PDF
    p.showPage()
    p.save()
    
    return response

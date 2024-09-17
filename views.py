from django.shortcuts import render, redirect
from django.urls import reverse
from cart.cart import Cart
from .forms import OrderCreateForm
from .models import Order, OrderItem
from .utils import generate_invoice_pdf as generate_pdf

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            # Aquí guardamos la información del usuario en el pedido
            order.user = request.user if request.user.is_authenticated else None
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
            cart.clear()
            # Redirigir a la página de confirmación de pedido usando reverse
            return redirect(reverse('orders:order_created', kwargs={'order_id': order.id}))
    else:
        form = OrderCreateForm()
    return render(
        request,
        'orders/order/create.html',
        {'cart': cart, 'form': form},
    )

def order_created(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        # Manejar el caso donde la orden no existe
        return render(request, 'orders/order/404.html', status=404)
    
    if request.method == 'POST' and 'download_invoice' in request.POST:
        # Generar y devolver el PDF
        response = generate_pdf(order_id)
        return response
    
    return render(
        request,
        'orders/order/created.html',
        {'order': order},
    )

def generate_invoice_pdf(request, order_id):
    # Generar el PDF y devolver la respuesta
    response = generate_pdf(order_id)
    return response

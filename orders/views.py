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
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
            cart.clear()
            # Redirigir a la página de confirmación de pedido usando reverse
            return redirect(reverse('order_created', kwargs={'order_id': order.id}))
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
    return render(
        request,
        'orders/order/created.html',
        {'order': order},
    )

def generate_invoice_pdf(request, order_id):
    response = generate_pdf(order_id)
    return response

# views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from cart.cart import Cart
from .forms import OrderCreateForm
from .models import Order, OrderItem
from .utils import create_invoice_pdf  # Cambia el nombre aquí

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
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
            return redirect(reverse('orders:order_created', kwargs={'order_id': order.id}))
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})

def order_created(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return render(request, 'orders/order/404.html', status=404)
    
    return render(request, 'orders/order/created.html', {'order': order})

def generate_invoice_pdf(request, order_id):
    return create_invoice_pdf(order_id)  # Cambia el nombre aquí

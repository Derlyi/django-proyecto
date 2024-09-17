from django.urls import path

from . import views


app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('order/<int:order_id>/', views.order_created, name='order_created'),
    path('order/<int:order_id>/invoice/', views.generate_invoice_pdf, name='order_invoice'),
]

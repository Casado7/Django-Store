from django.shortcuts import render, redirect
from .carro import Cart
from store.models import Product

# Create your views here.

def add_product(request, product_id):
    
    cart= Cart(request)
    product=Product.objects.get(id=product_id)
    cart.add(product=product)

    return redirect("store:all")

def delete_product(request, product_id):
    
    cart= Cart(request)
    product=Product.objects.get(id=product_id)
    cart.delete(product=product)

    return redirect("store:all")

def subtract_product(request, product_id):
    
    cart= Cart(request)
    product=Product.objects.get(id=product_id)
    cart.subtract(product=product)

    return redirect("store:all")

def clear_cart(request):
    
    cart= Cart(request)
    cart.clear_cart()

    return redirect("store:all")
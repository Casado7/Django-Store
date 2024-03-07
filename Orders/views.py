from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db.models import Q
from Orders.models import Order, Order_Line
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail

from cart.carro import Cart



def process_order(request):
    order= Order.objects.create(owner=request.user)
    cart = Cart(request)
    order_line = list()
    for key, value in cart.cart.items():
        order_line.append(Order_Line(
            product_id = key,
            quantity = value["quantity"],
            owner = request.user,
            order = order
        ))
    Order_Line.objects.bulk_create(order_line)
    send_mail_store(
        order=order,
        order_line= order_line,
        owner = request.user.username,
        email = request.user.email,
    )
    messages.success(request, "The Order has been created")
    
    return redirect("../store")


class Process_Order2(LoginRequiredMixin):
    model = Order
    def get(self, request) :
        order= Order.objects.create(user=request.user)
        cart = Cart(request)
        order_line = list()
        for key, value in cart.cart.items():
            order_line.append(Order_Line(
                product_id = key,
                quantity = value["quantity"],
                owner = request.user,
                order = order
            ))
        Order_Line.objects.bulk_create(order_line)
        send_mail_store(
            order=order,
            order_line= order_line,
            owner = request.user.username,
            email = request.user.email,
        )
        messages.success(request, "The Order has benn created")
        
        return redirect("../store")

def send_mail_store(**kwargs):
    subject="Thanks for the Order"
    message=render_to_string("emails/order.html",{
        "order": kwargs.get("order"),
        "order_line": kwargs.get("order_line"),
        "owner": kwargs.get("owner"),
        "email": kwargs.get("email")})
    message_text= strip_tags(message)
    from_email="themasterale2@gmail.com"
    to= kwargs.get("email")
    send_mail(subject, message_text,from_email,[to], html_message=message)
     
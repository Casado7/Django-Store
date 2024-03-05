from django.urls import path, reverse_lazy
from . import views

app_name='cart'
urlpatterns = [
    path('add/<int:product_id>', views.add_product, name='add_product'),
    path('delete/<int:product_id>', views.delete_product, name='delete_product'),
    path('subtract/<int:product_id>', views.subtract_product, name='subtract_product'),
    path('clearcart/', views.clear_cart, name='clear_cart'),
]
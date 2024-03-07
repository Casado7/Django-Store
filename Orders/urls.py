from django.urls import path, reverse_lazy
from . import views

app_name='Orders'
urlpatterns = [
    path('', views.process_order, name='process_order'),

]
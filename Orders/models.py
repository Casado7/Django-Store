from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
from django.contrib.auth.models import User
from store.models import Product
from django.db.models import F, Sum, FloatField

class Order(models.Model) :
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )
    # Shows up in the admin list
    def __str__(self):
        return self.id

    class Meta:
        verbose_name="Order"
        verbose_name_plural="Orders"
        ordering=["id"]
    @property
    def total(self):
        return self.order_line_set.aggregate(
            total=Sum(F("price")*F("quantity"), output_filed=FloatField())
        )["total"]

class Order_Line(models.Model) :
    product =models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        return f"{self.quantity} units of {self.product.title}"
    
    class Meta:
        verbose_name="Order Line"
        verbose_name_plural="Orders Lines"
        ordering=["id"]

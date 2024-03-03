from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


class Product(models.Model) :
    title = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    text = models.TextField()
    tags = TaggableManager(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Product_Comment', related_name='product_comments_owned')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    picture = models.BinaryField(null=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Product_Fav', related_name='favorite_products')

    # Shows up in the admin list
    def __str__(self):
        return self.title

class Product_Comment(models.Model) :
    text = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        if len(self.text) < 15 : return self.text
        return self.text[:11] + ' ...'



class Product_Fav(models.Model) :
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # https://docs.djangoproject.com/en/4.2/ref/models/options/#unique-together
    class Meta:
        unique_together = ('product', 'user')

    def __str__(self) :
        return '%s likes %s'%(self.user.username, self.product.title[:10])
from django.urls import path, reverse_lazy
from . import views

app_name='store'
urlpatterns = [
    path('', views.ProductListView.as_view(), name='all'),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='product_detail'),
    path('product/create',
        views.ProductCreateView.as_view(success_url=reverse_lazy('store:all')), name='product_create'),
    path('product/<int:pk>/update',
        views.ProductUpdateView.as_view(success_url=reverse_lazy('store:all')), name='product_update'),
    path('product/<int:pk>/delete',
        views.ProductDeleteView.as_view(success_url=reverse_lazy('store:all')), name='product_delete'),
    path('product_picture/<int:pk>', views.stream_file, name='product_picture'),
    path('product/<int:pk>/comment',
        views.Product_CommentCreateView.as_view(), name='product_comment_create'),
    path('comment/<int:pk>/delete',
        views.Product_CommentDeleteView.as_view(success_url=reverse_lazy('store:all')), name='product_comment_delete'),
    path('product/<int:pk>/favorite',
        views.AddProduct_FavoriteView.as_view(), name='product_favorite'),
    path('product/<int:pk>/unfavorite',
        views.DeleteProduct_FavoriteView.as_view(), name='product_unfavorite'),
]
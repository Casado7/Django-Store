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
from django.core.paginator import Paginator

from store.models import Product, Product_Comment, Product_Fav
from store.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from store.forms import CreateForm, Product_CommentForm


class ProductListView(OwnerListView):
    model = Product
    template_name = "store/product_list.html"
    # template_name = "myarts/article_list.html"

    def get(self, request) :
        strval =  request.GET.get("search", False)
        if strval :
            # Simple title-only search
            # objects = Post.objects.filter(title__contains=strval).select_related().distinct().order_by('-updated_at')[:10]

            # Multi-field search
            # __icontains for case-insensitive search
            query = Q(title__icontains=strval)
            query.add(Q(text__icontains=strval), Q.OR)
            query.add(Q(tags__name__in=[strval]), Q.OR)
            product_list = Product.objects.filter(query).select_related().distinct().order_by('-updated_at')[:10]
            paginator = Paginator(product_list, 4)  # Show 4 contacts per page.
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
        else :
            product_list = Product.objects.all().order_by('-updated_at')[:10]
            paginator = Paginator(product_list, 4)  # Show 4 contacts per page.
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
        for obj in page_obj:
            obj.natural_updated = naturaltime(obj.updated_at)
        favorites = list()
        if request.user.is_authenticated:
            # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
            rows = request.user.favorite_products.values('id')
            # favorites = [2, 4, ...] using list comprehension
            favorites = [ row['id'] for row in rows ]
        ctx = {'product_list' : product_list, 'favorites': favorites, 'search': strval, "page_obj":page_obj}
        return render(request, self.template_name, ctx)

    # By convention:



class ProductDetailView(OwnerDetailView):
    model = Product
    template_name = "store/product_detail.html"
    def get(self, request, pk) :
        x = get_object_or_404(Product, id=pk)
        comments = Product_Comment.objects.filter(product=x).order_by('-updated_at')
        comment_form = Product_CommentForm()
        context = { 'product' : x, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)

class ProductCreateView(OwnerCreateView, View):
    template_name = 'store/product_form.html'
    success_url = reverse_lazy('store:all')
    def get(self, request, pk=None):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Adjust the model owner before saving
        inst = form.save(commit=False)
        inst.owner = self.request.user
        inst.save()

        # https://django-taggit.readthedocs.io/en/latest/forms.html#commit-false
        form.save_m2m()    # Add this
        return redirect(self.success_url)
        # https://django-taggit.readthedocs.io/en/latest/forms.html#commit-false



class ProductUpdateView(LoginRequiredMixin, View):
    template_name = 'store/product_form.html'
    success_url = reverse_lazy('store:all')

    def get(self, request, pk):
        pic = get_object_or_404(Product, id=pk, owner=self.request.user)
        form = CreateForm(instance=pic)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        pic = get_object_or_404(Product, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=pic)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        pic = form.save(commit=False)
        pic.save()
        form.save_m2m()

        return redirect(self.success_url)


class ProductDeleteView(OwnerDeleteView):
    model = Product

def stream_file(request, pk):
    product = get_object_or_404(Product, id=pk)
    response = HttpResponse()
    response['Content-Type'] = product.content_type
    response['Content-Length'] = len(product.picture)
    response.write(product.picture)
    return response

class Product_CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        a = get_object_or_404(Product, id=pk)
        comment = Product_Comment(text=request.POST['comment'], owner=request.user, product=a)
        comment.save()
        return redirect(reverse('store:product_detail', args=[pk]))

class Product_CommentDeleteView(OwnerDeleteView):
    model = Product_Comment
    template_name = "store/comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        product = self.object.product
        return reverse('store:product_detail', args=[product.id])

@method_decorator(csrf_exempt, name='dispatch')
class AddProduct_FavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Add PK",pk)
        product = get_object_or_404(Product, id=pk)
        fav = Product_Fav(user=request.user, product=product)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteProduct_FavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Delete PK",pk)
        product = get_object_or_404(Product, id=pk)
        try:
            fav = Product_Fav.objects.get(user=request.user, product=product).delete()
        except Product_Fav.DoesNotExist:
            pass

        return HttpResponse()

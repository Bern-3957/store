from django.db.models import Count
from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from common.views import TitleMixin


# Create your views here.

class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'

class ProductsListView(ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    context_object_name = 'products'
    title = 'Store - Каталог'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        context['categories'] = ProductCategory.objects.annotate(c=Count('product')).filter(c__gte=1)
        # context['categories'] = ProductCategory.objects.all()
        context['category_id'] = self.kwargs.get('category_id')
        return context

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset


@login_required  # Позволяет не получать доступ к данному url (и функции соответсвенно) неавторизованным userам
def basket_add(request, product_id):
    product = Product.objects.get(pk=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)
    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])



# def index(request):
#     context = {
#         'title': 'store',
#     }
#     return render(request, 'products/index.html', context)

# def products(request, category_id=None, page_number=1):
#     products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
#     paginator = Paginator(products, 3, 1)
#     products_paginator = paginator.page(page_number)
#     context = {
#         'title': 'store',
#         'categories': ProductCategory.objects.annotate(c=Count('product')).filter(c__gte=1),
#         'products': products_paginator,
#     }
#     return render(request, 'products/products.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, DetailView, ListView
from django.db.models import Count
from .models import Product, Rate, ProductIPAddress
#from payments.models import Plan
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db import IntegrityError
#from django import forms
from json import JSONEncoder
from django.contrib import messages

class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        return Product.objects.all()#filter(address__village__mandal=self.request.user.address.village.mandal)

class ProductDetailView(DetailView):
    model = Product

class ProductRatesListView(ListView):
    model = Rate
    template_name = 'home/products_rates_list.html'
    context_object_name = 'rates'

    def get_queryset(self):
        product = get_object_or_404(Product,pk=self.kwargs.get('pk'))
        return Rate.objects.filter(product_id=product.id)
class MyProductsListView(LoginRequiredMixin, ListView):
#    model = Product
    template_name = 'product/my_devices.html'

    def get_queryset(self):
        return Product.objects.filter(owner=self.request.user)#.annotate(id__count=Count('id'),plan__count=Count('plan')) #Plan.objects.annotate(product__count=Count('product'))#.filter(product)#Product.objects.filter(owner=self.request.user)
    def get_context_data(self):
        context = super().get_context_data()
        context['inactive__count'] = Product.objects.filter(owner=self.request.user).filter(plan__is_active=False).annotate(inactive__count=Count('plan__is_active'))
        return context
    # def get_context_data(self):
    #     context = super().get_context_data()
    #     context['count'] = Plan.
    
class RateCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Rate
    fields = ['amount','liters_per_unit','units']
    def form_valid(self,form):
        form.instance.product = Product.objects.get(id=self.request.POST['product'])
        return super().form_valid(form)
    def test_func(self):
        user = self.request.user
        if user.is_authenticated:
            return True
        return False
    def get_context_data(self):
        products = Product.objects.filter(owner=self.request.user)
        context = super().get_context_data()
        context['products'] = products
        return context
class RateListView(ListView):
    model = Rate
    context_object_name = 'rates'

class RateDetailView(DetailView):
    model = Rate

# def update_product_ip(request):
#     response = dict()
#     if request.method == "GET":
#         g = request.GET
#         if 'prod' in g and 'ip' in g and 'key' in g:

#         else:
#             response['code'] = 100
#             response['error'] = "Some data is missing"
#     else:
#         response['code'] = 101
#         response['error'] = "Not a get request"
#     e = JSONEncoder()
#     return HttpResponse(e.encode(response))

def product_ip(request):
    response = dict()
    if request.method == "GET":
        g = request.GET
        if 'prod' in g and 'ip' in g and 'key' in g :
            try:
                prod_ips = ProductIPAddress.objects.filter(product_id=g['prod'])
                if len(prod_ips) >= 1:
                    if len(prod_ips) > 100:#delete history
                        pass
                    prod_ip = prod_ips.last()
                    if prod_ip.server_key == g['key']:
                        api_key = "nithin" # pending generete hash
                        serv_key = "nithinPk"#pending generate hash
                        new_prod_ip = ProductIPAddress.objects.create(product_id=g['prod'],ip=g['ip'],product_key=api_key,server_key=serv_key)
                        new_prod_ip.save()
                        response = {"api_key":api_key,"ssid":"kadapalla","password":"12345678"}
                        response['code'] = 200 #ok
                    else:
                        response['code'] = 403
                        response['error'] = "Not authenticated"
                else:
                    response['code'] = 201
                    response["error"] = 'not initialized properly'# i.e you don't have a server_key that is sent by server or product may not be present
            except IntegrityError:
                response['code'] = 202
                response['error'] = "IntegriryError"
            except ValueError:
                response['code'] = 203
                response['error'] = "ValueError" #may be product_id is not provided
            except OverflowError:
                response['code'] = 204
                response['error'] = "OverflowError"
        else:
            response['code'] = 100
            response['error'] = "Some data is missing"
    else:
        response['code'] = 101
        response["error"] = "Not a get request"
    e = JSONEncoder()
    return HttpResponse(e.encode(response))#'{"api_key":"'+api_key+'","ssid":"kadapalla","password":"12345678"}'
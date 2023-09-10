from django.http import HttpResponse
from django.shortcuts import render
from .models import Product

# Create your views here.

# /products -> index
# uniform resource locator (address)
def index(request):
    products = Product.objects.all()
    return render(request,'index.html', {'products': products})


def new(request):
    return HttpResponse('New Products')

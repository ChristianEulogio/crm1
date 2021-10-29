from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.

def home(request):
    orders= Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()

    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    #envez de pasarlos por el render lo pasamos en context y luego a render
    context = {'orders':orders, 'customers':customers,
    'total_orders':total_orders,'delivered':delivered,
    'pending':pending}
    return render(request, 'accounts/dashboard.html', context)

def products(request):
    #use the queryDemos gracias a que tenemos los modelos importados
    products = Product.objects.all()
    #pass these into the template to the render function
    return render(request, 'accounts/products.html',{'products':products})

def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders = customer.order_set.all()
    order_count = orders.count()
    context = {'customer':customer, 'orders':orders, 'order_count':order_count}
    return render(request, 'accounts/customer.html', context)


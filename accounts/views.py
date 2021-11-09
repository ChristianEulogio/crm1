from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
#para el inico de secion y cierre
from django.contrib.auth import authenticate, login, logout
# messages flash
from django.contrib import messages 
#para requerir el login
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter

def registerPage(request):
    #si el usuario esta autentiado-logeado manda a la pagina home 
    if request.user.is_authenticated:
        return redirect('home')
    #si no lo esta significa que apenas se esta registrando
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            #al darle submit le pasamos la informacion 
            #del form en request.POST 
            form = CreateUserForm(request.POST)
            #si el form es valido save
            if form.is_valid():
                form.save()
                #name of user
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                #redirect login/
                return redirect('login')

        context = {'form':form}
        return render(request, 'accounts/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        #si le damos en login se obtendra con request.POST.get()
        #el user y la pass que metimos  
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
        #verificara con authenticate si coinciden con los datos de la base
            user = authenticate(request, username=username, password=password)
        #si los datos coinciden user no sera None
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

#si no estas logiado te manda a login
@login_required(login_url='login')

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
@login_required(login_url='login')

def products(request):
    #use the queryDemos gracias a que tenemos los modelos importados
    products = Product.objects.all()
    #pass these into the template to the render function
    return render(request, 'accounts/products.html',{'products':products})
@login_required(login_url='login')

def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter= OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer':customer, 'orders':orders, 
    'order_count':order_count, 'myFilter':myFilter}
    return render(request, 'accounts/customer.html', context)
@login_required(login_url='login')

def createOrder(request, pk):

    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=6 )
    customer = Customer.objects.get(id=pk)
    #queryset=order.objects.none() if we have onjects there don't reference them just let it all be new items 
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    #form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        #print('Printing POST:',request.POST)
        #form= OrderForm(request.POST)
        formset= OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset':formset}
    return render(request, 'accounts/order_form.html', context)
@login_required(login_url='login')

def updateOrder(request, pk):
    #para rellenar los  campos en la actualizacion
    order= Order.objects.get(id = pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form= OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)
@login_required(login_url='login')

def deleteOrder(request, pk):
    order= Order.objects.get(id = pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'item':order}
    return render(request,'accounts/delete.html',context)

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
from django.contrib.auth.models import Group
# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only
#, allowed_users
@unauthenticated_user
def registerPage(request): 
    form = CreateUserForm()
    if request.method == 'POST':
        #al darle submit le pasamos la informacion 
        #del form en request.POST 
        form = CreateUserForm(request.POST)
        #si el form es valido save
        if form.is_valid():
            user = form.save()
            #name of user
            username = form.cleaned_data.get('username')
            #obtenemos group
            group = Group.objects.get(name='customer')
            user.groups.add(group)#le añadimos el grupo a user
            #se crea un customer para el nuevo user
            Customer.objects.create(
                user=user,
            )

            messages.success(request, 'Account was created for ' + username)
            #redirect login/
            return redirect('login')

    context = {'form':form}
    return render(request, 'accounts/register.html', context)

'''
if the user is authenticated we never actually call login page so we
just go ahead and redirect that user home and if the user is not
authenticated then we return the view function 
'''
#no se ejecutare a menos que se ejecute wrapper_func(loginPage)
@unauthenticated_user
def loginPage(request):
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
#@allowed_users(allowed_roles=['admin'])
@admin_only
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
@allowed_users(allowed_roles=['customer'])#para que el customer pueda aceder
def userPage(request):
    #para sacar las ordernes de customer no el usuario ya que tiene un onetoOne
    #llamamos al customer del 'user' logiado con request
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders':orders, 'total_orders':total_orders,'delivered':delivered,
    'pending':pending}
    #show me the orders form customer
    print('ORDERS:', orders)
    return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    #this is just going to get us that logged in user and the customer associated at
    #any point in time and let's pass in that form 
    customer= request.user.customer
    #instance es para rellenar los campos 
    form = CustomerForm(instance=customer)

    #para guardar datos 
    if request.method =='POST':
        #obtenemos los datos del POST y se los pasamos
        # a CustomerForm y los gardamos en form tambien se los pasamos al instance 
        form = CustomerForm(request.POST, request.FILES,instance=customer)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, 'accounts/account_settings.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    #use the queryDemos gracias a que tenemos los modelos importados
    products = Product.objects.all()
    #pass these into the template to the render function
    return render(request, 'accounts/products.html',{'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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
@allowed_users(allowed_roles=['admin'])
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
@allowed_users(allowed_roles=['admin'])
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
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order= Order.objects.get(id = pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'item':order}
    return render(request,'accounts/delete.html',context)

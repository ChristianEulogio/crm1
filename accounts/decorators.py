from django.http import HttpResponse
from django.shortcuts import redirect

#view_func is login page in this case
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        #si el usuario esta autentiado-logeado manda a la pagina home 
        if request.user.is_authenticated:
            return redirect('home')
        #si no lo esta significa que apenas se esta registrando o iniciando secion
        return view_func(request, *args, **kwargs)
    return wrapper_func
#asta a qui funciona bien
#especificamos el grupp de los que si queremos que funcione
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            #si el user tiene grupos
            if request.user.groups.exists():
                #obtener los grupos del user
                group = request.user.groups.all()[0].name
                #si el grupo esta en los allowed roles
            if group in allowed_roles:
                #manda a la vista
                return view_func(request, *args, **kwargs)
            else:
                #si no esta en los grupos no 
                return HttpResponse('You are not authorized to view this page')
            
            return view_func(request, *args, **kwargs)
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
    #si el grupo es customer redirije a user page
        if group == 'customer':
            return redirect('user-page')
    #si no sighue con la view
        if group == 'admin':
            return view_func(request, *args, **kwargs)

    return wrapper_function

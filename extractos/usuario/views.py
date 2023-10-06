from django.shortcuts import render, HttpResponse, redirect
from usuario.forms import LogUsuario
from usuario.models import Usuario
from cuenta.models import Cuenta
from django.contrib import messages

# Funcion creada para probar conexion con la ruta..
def usuario_test_hello(request):
    return HttpResponse("Hola usuario")

# Conexion con index.
def index_user(request):
    return render(request,'index.html') 

#Ingresar la cédula.
def validar_usuario(request):
    if(request.method=='GET'):
        return render(request,
                      'validar_usuario.html',
                      {'form': LogUsuario()})
    else:
        try:
            user=Usuario.objects.get(identificacion=request.POST['identificacion'])
            cuenta=Cuenta.objects.filter(titular_id=user.identificacion)
            return redirect('extracto_cuenta', n_cuenta=cuenta[0].n_cuenta)
        except:
            messages.error(request,'Identificacion NO válida o Identifiación NO POSEE CUENTA.')
            return redirect('validar_usuario')
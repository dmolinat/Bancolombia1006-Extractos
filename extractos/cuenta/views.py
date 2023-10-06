from django.shortcuts import render, HttpResponse
from cuenta.models import Cuenta
from movimiento.models import Movimiento

# Create your views here.
def test_cuenta_hello(request):
    return HttpResponse("Hola cuenta")
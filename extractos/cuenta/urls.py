from django.urls import path
from cuenta.views import test_cuenta_hello

urlpatterns = [
    path('cuenta/hellocuenta', test_cuenta_hello),   
]

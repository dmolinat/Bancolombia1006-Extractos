from django.db import models
from usuario.models import Usuario

# Creacion del modelo de Cuenta
class Cuenta(models.Model):
    n_cuenta = models.CharField(default="XXXX", max_length=50, primary_key=True)
    tipo_cuenta = models.CharField(default="AHORROS", max_length=20)
    saldo = models.FloatField(default=0)
    titular = models.OneToOneField(Usuario, on_delete=models.CASCADE)
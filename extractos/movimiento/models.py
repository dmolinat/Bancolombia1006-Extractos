from django.db import models
from cuenta.models import Cuenta
from django.utils import timezone

# Creacion del modelo de movimiento.
class Movimiento(models.Model):
    fecha = models.DateField(default=timezone.now())
    n_cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    valor = models.FloatField()
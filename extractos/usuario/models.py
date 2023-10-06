from django.db import models

# Creacion del modelo usuario.
class Usuario(models.Model):
    identificacion = models.CharField(max_length=50, primary_key=True)
from django import forms

class LogUsuario(forms.Form):
    identificacion = forms.CharField(label="Ingrese su documento de identificacion", max_length=49)

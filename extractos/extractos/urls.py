from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('',include('movimiento.urls')),
    path('',include('cuenta.urls')),
    path('',include('usuario.urls')),
    path('admin/', admin.site.urls),
]

from django.urls import path
from usuario.views import usuario_test_hello, index_user, validar_usuario

urlpatterns = [
    path('usuario/hellousuario', usuario_test_hello),
    path('',index_user),
    path('usuario/validar', validar_usuario, name="validar_usuario")
]
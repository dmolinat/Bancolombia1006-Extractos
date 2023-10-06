from django.urls import path
from movimiento.views import test_hello_movement, get_movimientos_por_cuenta, generate_extracto

urlpatterns = [
    path('movimiento/hellomov', test_hello_movement),
    path('movimiento/movimientosCuentas/<str:n_cuenta>', get_movimientos_por_cuenta, name="movimiento_cuenta"),
    path('movimiento/getExtracto/<str:n_cuenta>', generate_extracto, name="extracto_cuenta"),
]
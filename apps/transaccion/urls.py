from django.urls import path
from apps.transaccion.views import transaccionIndex

urlpatterns = [
    path('', transaccionIndex, name='transaccionIndex')
]
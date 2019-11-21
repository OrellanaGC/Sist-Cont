from django.urls import path
from django.conf.urls import url
from apps.reportes.views import libroDiario, libroMayor, kardex, balanceGeneral, estadoResultado, flujoEfectivo

urlpatterns = [
    path('libroDiario', libroDiario, name="libroDiario"),
    path('libroMayor', libroMayor, name="libroMayor"),
    path('kardex/<int:idKardexRequest>', kardex, name="kardex"),
    path('balanceGeneral', balanceGeneral, name="balanceGeneral"),
    path('estadoResultado', estadoResultado, name="estadoResultado"),
    path('flujoEfectivo', flujoEfectivo, name="flujoEfectivo"),
]
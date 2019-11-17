from django.urls import path
from django.conf.urls import url
from apps.reportes.views import libroDiario, libroMayor, kardex

urlpatterns = [
    path('libroDiario', libroDiario, name="libroDiario"),
    path('libroMayor', libroMayor, name="libroMayor"),
    path('kardex', kardex, name="kardex"),
]
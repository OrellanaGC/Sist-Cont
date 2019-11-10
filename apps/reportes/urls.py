from django.urls import path
from django.conf.urls import url
from apps.reportes.views import libroDiario

urlpatterns = [
    path('libroDiario', libroDiario, name="libroDiario"),
]
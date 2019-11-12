from django.urls import path
from django.conf.urls import url
from apps.index.views import index

urlpatterns = [
    path('', index, name="index2"),
]

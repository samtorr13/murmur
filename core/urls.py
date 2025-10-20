from . import views
from django.urls import path
urlpatterns = [
    path('validate/username', views.validar_username, name='validar_username')
]

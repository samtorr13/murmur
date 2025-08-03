from . import views
from django.urls import path
urlpatterns = [
    path('profile/<str:username>/', views.userprofile, name='userprofile'),
]

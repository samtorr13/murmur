from . import views
from django.urls import path
urlpatterns = [
    path('profile/edit/', views.profileEdit, name='profile_edit'),
    path('profile/<str:username>/', views.userprofile, name='userprofile'),
]

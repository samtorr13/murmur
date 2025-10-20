from . import views
from django.urls import path
urlpatterns = [
    path('profile/edit/', views.profileEdit, name='profile_edit'),
    path('profile/upd/', views.profileUpdate, name='profileUpdate'),
    path('profile/<str:username>/', views.userprofile, name='userprofile'),
    path('profile/delete_post/<int:post_id>/', views.deletePost, name='delete_post'),
    
]

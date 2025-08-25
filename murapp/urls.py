
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from murapp import settings


from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('accounts/', include('allauth.urls')),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('post/like/<int:post_id>/', views.like_post, name='like_post'),
    path('', include('user_profile.urls')),
    path('posts/comment/<int:post_id>/', view=views.comment_as_view, name='comment_as_view'),
    path('posts/report/<int:post_id>/', view=views.report_post, name='report_post'),
    path('welcome/', views.welcome_wizard, name='welcome')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
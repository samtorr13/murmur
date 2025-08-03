from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from posts.models import Like, Post
from user_profile.models import UserProfile


@login_required
def userprofile(request, username):
    profile = get_object_or_404(UserProfile, user__username=username)
    viewer_profile = request.user.profile if request.user.is_authenticated else None
    prof_photo = viewer_profile.profile_picture if viewer_profile and viewer_profile.profile_picture else None

    posts = Post.objects.filter(author=profile.user).order_by('-created_at')

    return render(request, 'profile.html', {
        'posts': posts,
        'user': profile.user,  
        'profile': profile,    
        'userprofile': viewer_profile,
    })

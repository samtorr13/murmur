from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from posts.models import Like, Post
from user_profile.models import UserProfile
import os
from uuid import uuid4



@login_required
def userprofile(request, username):
    profile = get_object_or_404(UserProfile, user__username=username)
    viewer_profile = request.user.profile if request.user.is_authenticated else None
    prof_photo = viewer_profile.profile_picture if viewer_profile and viewer_profile.profile_picture else None

    posts = Post.objects.filter(author=profile.user, anonymous=False ).order_by('-created_at')

    if profile.user == request.user:
        selfUser = True
    else:
        selfUser = False


    return render(request, 'profile.html', {
        'posts': posts,
        'user': profile.user,  
        'profile': profile,    
        'userprofile': viewer_profile,
        'selfUser': selfUser
    })

def profileEdit(request):
    profile = get_object_or_404(UserProfile, user__username=request.user.username)
    temas = list(profile.themes.values_list('name', flat=True))

    if request.method == 'POST':
        profile.bio = request.POST.get('bio', profile.bio)
        profile.profile_picture = request.FILES.get('profile_picture', profile.profile_picture)
        profile.prof_theme = request.POST.get('theme', profile.prof_theme)
        profile.save()


        return redirect('userprofile', username=request.user.username)

    return render(request, 'profile_edit.html', {
        'profile': profile,
        'temas': temas,
        
    })

@login_required
def deletePost(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id, author=request.user)
        post.delete()
        return redirect('userprofile', username=request.user.username)
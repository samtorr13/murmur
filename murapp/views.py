from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from posts.models import Like, Post, Comment, Media, Report
from user_profile.models import Theme, UserProfile
from django.core.paginator import Paginator
from django.template.loader import render_to_string


def home(request):
    if request.user.is_authenticated and not hasattr(request.user, 'profile'):
        return redirect('welcome')
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        is_anon = request.POST.get('anonymous') == 'on'
        image = request.FILES.get('image')

        if content or image:
            post_obj = Post.objects.create(
            author=request.user,
            content=content,
            anonymous=is_anon,
            )
            if image:
                Media.objects.create(
                    post=post_obj,
                    file=image
                )

        
            return redirect('home')
    username = request.user.username if request.user.is_authenticated else 'Guest'
    page = request.GET.get("page", 1)
    posts = Post.objects.order_by("-created_at")
    paginator = Paginator(posts, 5)  # 10 posts por "página"
    page_obj = paginator.get_page(page)

    if request.headers.get("HX-Request"):
        return render(request, "components/post_loop.html", {"posts": page_obj})

    return render(request, 'index.html', {'posts': page_obj})

class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return self.request.GET.get('next', 'home')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    like = Like.objects.filter(user=request.user, post=post).first()

    if like:
        like.delete()
    else:
        Like.objects.create(user=request.user, post=post)

    post.like_count = post.likes.count()
    post.save()

    if request.headers.get('HX-Request'):
        html = render_to_string("like_btn.html", {"post": post, "user": request.user})
        return HttpResponse(html)


    return redirect('home')

@login_required
def comment_as_view(request, post_id):
    if request.method == "POST":
        content = request.POST.get("content")
        post = Post.objects.get(id=post_id)
        is_anon = request.POST.get('anonymous') == 'on'
        comment = Comment.objects.create(
            post=post,
            author=request.user,
            content=content,
            anonymous=is_anon
        )
    comments = get_object_or_404(Post, id=post_id).comments.filter(parent__isnull=True).order_by('-created_at')


    if request.headers.get('HX-Request'):
        return render(request, "components/comment.html", {"post_id": post_id, "comments": comments})
    return render(request, "posts/comment_form.html", {"comments": comments})

@login_required
def report_post(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        reason = request.POST.get("reason")

        report = Report.objects.create(
            post=post,
            user=request.user,
            reason=reason
        )

        return redirect('home')
    return HttpResponse(status=400)

@login_required
def welcome_wizard(request):
    if hasattr(request.user, 'profile'):
        return redirect('home')
    
    if request.method == 'POST':
        bio = request.POST.get('bio')
        profile_picture = request.FILES.get('profile_picture')
        prof_theme = request.POST.get('theme')

        UserProfile.objects.create(
            user = request.user,
            bio = bio,
            profile_picture = profile_picture,
            prof_theme = prof_theme
        )
        
        return redirect('userprofile', username=request.user.username)
    
    temas = list(Theme.objects.filter(group="User"))
    return render(request, 'welcome.html', {'temas': temas})
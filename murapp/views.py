from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from posts.models import Like, Post
from django.core.paginator import Paginator
from django.template.loader import render_to_string

@login_required
def home(request):
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        is_anon = request.POST.get('anonymous') == 'on'

        if content:
            Post.objects.create(
                author=request.user,
                content=content,
                anonymous=is_anon
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

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from posts.models import Like, Post

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
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'posts': posts})

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

    return redirect('home')

from django.shortcuts import redirect, render
from models import Post, Comment


def comment_as_view(request, post_id):
    if request.method == "POST":
        content = request.POST.get("content")
        post = Post.objects.get(id=post_id)
        comment = Comment.objects.create(
            post=post,
            author=request.user,
            content=content
        )
        return redirect("post_detail", post_id=post.id)
    return render(request, "posts/comment_form.html")

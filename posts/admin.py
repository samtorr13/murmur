from django.contrib import admin
from posts.models import Post, Like, Comment


class LikeInline(admin.TabularInline):
    model = Like
    extra = 0  
    readonly_fields = ('user', 'liked_at') 

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0  
    readonly_fields = ('author', 'created_at', 'content')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('general_pid', 'author', 'created_at')
    search_fields = ('author__username', 'content')
    list_filter = ('created_at',)
    inlines = [LikeInline]
    ordering = ('-created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('general_pid', 'author', 'created_at', 'post')
    search_fields = ('author__username', 'content')
    list_filter = ('created_at',)

    ordering = ('-created_at',)

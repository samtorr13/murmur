from django.contrib import admin
from posts.models import Post, Like


class LikeInline(admin.TabularInline):
    model = Like
    extra = 0  
    readonly_fields = ('user', 'liked_at') 

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('general_pid', 'author', 'created_at')
    search_fields = ('author__username', 'content')
    list_filter = ('created_at',)
    inlines = [LikeInline]
    ordering = ('-created_at',)
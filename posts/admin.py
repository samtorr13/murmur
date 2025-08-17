from django.contrib import admin
from posts.models import Post, Like, Comment, Media, Report


class LikeInline(admin.TabularInline):
    model = Like
    extra = 0  
    readonly_fields = ('user', 'liked_at') 

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0  
    readonly_fields = ('author', 'created_at', 'content')

class MediaInline(admin.TabularInline):
    model = Media
    extra = 0
    readonly_fields = ('post', 'file')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('general_pid', 'author', 'created_at', 'like_count', 'content', 'anonymous')
    search_fields = ('author__username', 'content')
    list_filter = ('created_at',)
    inlines = [LikeInline, CommentInline, MediaInline]
    ordering = ('-created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('general_pid', 'author', 'created_at', 'post')
    search_fields = ('author__username', 'content')
    list_filter = ('created_at',)

    ordering = ('-created_at',)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    readonly_fields = ('post', 'user', 'created_at', 'reason',)
    list_display = ('post', 'resolved', 'deleted', 'reason')
    search_fields = ('post__content', 'user__username', 'reason', 'resolved', 'deleted')
    list_filter = ('resolved',)
    ordering = ('-created_at', 'resolved')

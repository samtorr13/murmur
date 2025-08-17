from django.conf import settings
from django.db import models
from core.models import GlobalPostIdentifier

class Post(models.Model):
    general_pid = models.OneToOneField(GlobalPostIdentifier, on_delete=models.CASCADE)
    like_count = models.IntegerField(default=0)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    anonymous = models.BooleanField(default=False)


    def __str__(self):
        return f"Post {self.general_pid} by {self.author.username}"

    def save(self, *args, **kwargs):
        if not self.general_pid_id:  # Si aún no tiene un general_pid
            pid = GlobalPostIdentifier.objects.create()
            self.general_pid = pid
        super().save(*args, **kwargs)

class Comment(models.Model):
    general_pid = models.OneToOneField(GlobalPostIdentifier, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    anonymous = models.BooleanField(default=False)

    parent = models.ForeignKey(
        'self',                  
        null=True,               
        blank=True,
        related_name='replies',  
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Comment {self.general_pid} on {self.post} by {self.author.username}"
    
    def save(self, *args, **kwargs):
        if not self.general_pid_id: 
            pid = GlobalPostIdentifier.objects.create()
            self.general_pid = pid
        super().save(*args, **kwargs)
            

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user} le dió like a {self.post}"

class Media(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media')
    file = models.FileField(upload_to='media/post/')
    def __str__(self):
        return f"Media for {self.post.general_pid}"

class Report(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reports')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reason = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Report {self.id} for {self.post.general_pid} by {self.user.username}"
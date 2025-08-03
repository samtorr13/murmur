from django.db import models
from django.core.files.base import ContentFile
import requests


class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='prof_pics/', blank=True, null=True)
    posts = models.ManyToManyField('posts.Post', related_name='user_posts', blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        if not self.profile_picture:
            seed = self.user.username or "anon"
            url = f"https://api.dicebear.com/9.x/avataaars-neutral/svg?seed={seed}"
            response = requests.get(url)
            if response.status_code == 200:
                file_name = f"{self.user.username}_avatar.svg"
                self.profile_picture.save(file_name, ContentFile(response.content), save=False)
        super().save(*args, **kwargs)  # Call the "real" save() method.

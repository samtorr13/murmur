from django.db import models
from django.core.files.base import ContentFile
import requests

class Theme(models.Model):
    name = models.CharField(max_length=50,)
    group = models.CharField(max_length=50,)
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    def avatar_upload_path(instance, filename):
        ext = filename.split('.')[-1]
        return f'prof_pics/{instance.user.username}_avatar.{ext}'

    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to=avatar_upload_path, blank=True, null=True)
    posts = models.ManyToManyField('posts.Post', related_name='user_posts', blank=True)
    prof_theme = models.TextField(blank=True, default='light')
    themes = models.ManyToManyField(Theme, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):

        try:
            this = UserProfile.objects.get(id=self.id)
            if this.profile_picture != self.profile_picture and this.profile_picture.name:
                this.profile_picture.delete(save=False)
        except UserProfile.DoesNotExist:
                pass

        if not self.profile_picture:
            seed = self.user.username or "anon"
            url = f"https://api.dicebear.com/9.x/avataaars-neutral/svg?seed={seed}"
            response = requests.get(url)
            if response.status_code == 200:
                file_name = f"{self.user.username}_avatar.svg"
                self.profile_picture.save(file_name, ContentFile(response.content), save=False)

        super().save(*args, **kwargs)  # Call the "real" save() method.
        if not self.themes.exists():
            iniciales = Theme.objects.filter(name__in=['light', 'dark'])
            self.themes.set(iniciales)

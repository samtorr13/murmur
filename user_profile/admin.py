from django.contrib import admin
from user_profile.models import UserProfile, Theme
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ("themes", "posts")
    list_display = ('user', 'bio', 'profile_picture')
    search_fields = ('user__username',)
    readonly_fields = ('user',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    
    def save_model(self, request, obj, form, change):
        obj.save()
        if not change:  # If creating a new profile, ensure it is linked to the user
            obj.user.userprofile = obj
            obj.user.save()
        super().save_model(request, obj, form, change)
    def has_add_permission(self, request):
        return False

@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display= ('name', )
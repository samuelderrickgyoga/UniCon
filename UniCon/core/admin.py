from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile

class UserAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        for user in queryset:
            if not hasattr(user, 'profile'):
                Profile.objects.create(user=user)
        return queryset

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile)
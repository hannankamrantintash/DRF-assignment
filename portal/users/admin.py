from django.contrib import admin
from users.models import User, Post
from django.contrib.auth.models import Group


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'cnic', 'email')


@admin.register(Post)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'text')

    def user(self, obj):
        return obj.user.email


admin.site.unregister(Group)

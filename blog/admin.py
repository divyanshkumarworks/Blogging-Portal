from django.contrib import admin
from .models import Post, Comment, UserFollowing, Message

admin.site.register(Comment)
admin.site.register(UserFollowing)
admin.site.register(Message)
admin.site.register(Post)



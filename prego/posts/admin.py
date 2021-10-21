from django.contrib import admin

from .models import Post, PostTranslation, PostSeo

admin.site.register(Post)
admin.site.register(PostTranslation)
admin.site.register(PostSeo)

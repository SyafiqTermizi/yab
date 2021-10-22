from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import PostTranslation


class CreatePostView(LoginRequiredMixin, CreateView):
    queryset = PostTranslation.objects.all()
    success_url = ""
    fields = ["post", "title", "body", "language", "draft"]
    template_name = "posts/create.html"

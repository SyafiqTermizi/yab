from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.views.generic import TemplateView

from .models import PostTranslation, Post, Languages


class CreatePostView(LoginRequiredMixin, TemplateView):
    template_name = "posts/create.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "languages": Languages.choices,
                "posts": Post.objects.annotate(
                    translation_count=Count("translations"),
                )
                .filter(
                    translation_count__lt=30,
                )
                .values(
                    "pk",
                    "slug",
                ),
            }
        )
        return context

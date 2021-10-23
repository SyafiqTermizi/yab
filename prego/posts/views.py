from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse
from django.views.generic import TemplateView

from .forms import PostTranslationForm
from .models import Post, Languages


class CreatePostView(LoginRequiredMixin, TemplateView):
    template_name = "posts/create.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "languages": Languages.choices,
                "posts": Post.objects.all(),
            }
        )
        return context

    def post(self, request, *args, **kwargs):
        form = PostTranslationForm(data=request.POST)

        if not form.is_valid():
            return self.response_class(
                request=request,
                template=self.get_template_names(),
                context={**self.get_context_data(), "errors": form.errors},
            )
        form.save()

        return JsonResponse({"msg": "..."})

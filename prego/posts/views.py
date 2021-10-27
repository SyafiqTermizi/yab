from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse
from django.views.generic import TemplateView

from .serializers import PostTranslationSerializer
from .models import Post, Languages


class CreatePostView(LoginRequiredMixin, TemplateView):
    template_name = "posts/create.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "languages": Languages.choices,
                "posts": Post.objects.get_post_with_incomplete_translation(),
            }
        )
        return context

    def post(self, request, *args, **kwargs):
        serializer = PostTranslationSerializer(
            data=request.POST,
            context={"created_by": request.user},
        )

        if not serializer.is_valid():
            context = {
                **self.get_context_data(),
                "serializer_errors": serializer.errors,
                "serializer_data": serializer.data,
            }

            return self.response_class(
                request=request,
                template=self.get_template_names(),
                context=context,
            )
        serializer.save()

        return JsonResponse({"msg": "..."})

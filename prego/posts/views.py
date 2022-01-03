from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.http.response import HttpResponseRedirect
from django.http.request import HttpRequest
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Post, PostTranslation, PostTranslationImage, Languages
from .serializers import PostTranslationSerializer, ImageUploadSerializer
from .utils import get_post_qs


class CreatePostView(LoginRequiredMixin, TemplateView):
    template_name = "posts/posttranslation_form.html"

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
        post = serializer.save()

        return HttpResponseRedirect(
            reverse(
                "posts:detail",
                kwargs={"slug": post.slug},
            )
        )


class ListPostView(ListView):
    context_object_name = "post_translations"

    def get_queryset(self) -> QuerySet[PostTranslation]:
        return get_post_qs(user=self.request.user, language=self.request.LANGUAGE_CODE)


class DetailPostView(DetailView):
    def get_queryset(self) -> QuerySet[PostTranslation]:
        return get_post_qs(self.request.user, language=self.request.LANGUAGE_CODE)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_image_view(request: HttpRequest):
    # Validate POST data
    serializer = ImageUploadSerializer(request.POST, request.FILES)
    serializer.is_valid(raise_exception=True)

    # Save image to DB
    post_image = PostTranslationImage(image=request.FILES["image"])
    post_image.save()

    # Return data to user
    serializer = ImageUploadSerializer(instance=post_image)
    return Response({"data": serializer.data})

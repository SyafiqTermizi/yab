from django.db.models.query import QuerySet

from blog.users.models import User

from .models import PostTranslation


def get_post_qs(user: User, language: str = None) -> QuerySet[PostTranslation]:
    qs = PostTranslation.objects.filter(draft=False)

    if user.is_authenticated:
        qs = qs | PostTranslation.objects.filter(draft=True, created_by=user)

    if language:
        qs = qs.filter(language=language)

    return qs

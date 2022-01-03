import pytest
from django.utils.text import slugify
from rest_framework import serializers
from blog.posts.models import PostTranslation

from blog.posts.serializers import PostTranslationSerializer, Languages


def test_post_translation_serializer_valid(db, create_user):
    """
    User should be able to create a new posts.PostTranslation in 'en' without
    a posts.Post instance
    """
    user = create_user()
    data = {
        "title": "Post title",
        "body": "Post Body",
        "language": "en",
    }
    serializer = PostTranslationSerializer(data=data, context={"created_by": user})
    assert serializer.is_valid(raise_exception=True)


@pytest.mark.parametrize("language", ["zh", "ms", "en"])
def test_post_translation_seralizer_invalid_existing_language(
    db,
    create_user,
    create_post,
    create_post_translation,
    language,
):
    """
    User should not be able to create posts.PostTranslation with a language that already exist
    """
    post = create_post()

    create_post_translation(post=post)
    create_post_translation(post=post, language=Languages.MS)
    create_post_translation(post=post, language=Languages.ZH)

    data = {
        "post": post,
        "title": "Existing language",
        "body": "Testing existing language",
        "language": language,
    }

    serializer = PostTranslationSerializer(
        data=data, context={"created_by": create_user()}
    )

    with pytest.raises(serializers.ValidationError):
        serializer.is_valid(raise_exception=True)


def test_post_translation_serializer_new_post(db, create_user):
    """
    Newly created translation should have post and slug assigned to it
    """
    post_data = {
        "title": "This is a post title",
        "html_body": "<h1></h1>",
        "json_body": {"title": "hi"},
        "language": Languages.EN,
    }
    serializer = PostTranslationSerializer(
        data=post_data, context={"created_by": create_user()}
    )
    assert serializer.is_valid(raise_exception=True)

    translation = serializer.save()

    assert translation.slug == slugify(post_data["title"])
    assert translation.post.pk

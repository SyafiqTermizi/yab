from _pytest.outcomes import _with_exception
import pytest
from django.utils.text import slugify
from rest_framework import serializers
from prego.posts.models import PostTranslation

from prego.posts.serializers import PostTranslationSerializer, Languages


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

    translation = serializer.save()
    translation.post.title = slugify("Post title")


@pytest.mark.parametrize("language", ["zh", "ms", "non-existent-lang"])
def test_post_translation_seralizer_invalid_initial_language(db, create_user, language):
    """
    User should not be able to submit new posts.PostTranslation in 'zh' or 'ms'
    """
    user = create_user()
    data = {
        "title": "Post title",
        "body": "Post Body",
        "language": language,
    }
    serializer = PostTranslationSerializer(data=data, context={"created_by": user})

    with pytest.raises(serializers.ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.parametrize("language", ["zh", "ms", "en"])
def test_post_translation_seralizer_invalid_existing_language(
    db, create_user, create_post, create_post_translation, language
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

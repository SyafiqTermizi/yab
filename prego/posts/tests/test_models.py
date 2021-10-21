import pytest
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from prego.posts.models import PostTranslation, PostSeo


def test_post_translation_create_new_en_post(db, create_user):
    """
    Newly created PostTranslation in EN should have a Post instance assigned
    """

    user = create_user()
    title = "this is a test post"

    post_translation = PostTranslation.objects.create(
        title=title,
        language="en",
        created_by=user,
    )
    assert post_translation.post.pk
    assert post_translation.post.slug == slugify(title)


@pytest.mark.parametrize("lang", ["ms", "zh", "alien"])
def test_create_new_non_en_post(db, create_user, lang):
    """
    PostTranslation model should raise a ValidationError if this 2 conditions
    are met:
    1. The new PostTranslation doesn't have Post instance
    2. The new PostTranslation is not in EN
    """
    user = create_user()

    with pytest.raises(ValidationError):
        PostTranslation.objects.create(
            title="this is a test post",
            language=lang,
            created_by=user,
        )


@pytest.mark.parametrize("lang", ["ms", "zh", "en"])
def test_create_new_translation(db, create_post, lang):
    """
    Creating a PostTranslation with a Post instance with any language should
    not raise a ValidationError
    """
    post = create_post()

    pt = PostTranslation.objects.create(
        title="this is a test post",
        language=lang,
        created_by=post.created_by,
        post=post,
    )

    assert pt.post.pk == post.pk
    assert pt.language == lang


def test_post_seo_save(db, create_post_translation):
    """
    PostSeo.title should be auto-populated with PostTranslation.title if
    title is not passed
    """
    post_translation = create_post_translation()
    seo = PostSeo.objects.create(post=post_translation)

    assert seo.title == post_translation.title[:88]

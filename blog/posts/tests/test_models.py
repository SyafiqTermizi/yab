import pytest

from blog.posts.models import PostSeo


@pytest.mark.parametrize("lang", ["ms", "zh", "en"])
def test_create_new_translation_valid(db, create_post, create_post_translation, lang):
    """
    Creating a PostTranslation with a Post instance with any language should
    not raise a ValidationError
    """
    post = create_post()
    pt = create_post_translation(post=post, language=lang)

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

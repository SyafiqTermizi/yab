import pytest

from prego.posts.tests.factories import PostFactory, PostTranslationFactory


@pytest.fixture
def create_post():
    def fn(**kwargs):
        return PostFactory.create(**kwargs)

    return fn


@pytest.fixture
def create_post_translation():
    def fn(**kwargs):
        return PostTranslationFactory.create(**kwargs)

    return fn

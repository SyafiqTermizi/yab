import factory

from factory.django import DjangoModelFactory

from prego.users.tests.factories import UserFactory
from prego.posts.models import Post, PostTranslation


class PostFactory(DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)

    class Meta:
        model = Post


class PostTranslationFactory(DjangoModelFactory):
    slug = factory.Faker("slug")
    post = factory.SubFactory(PostFactory)
    title = factory.Faker("text")
    html_body = factory.Faker("paragraph")
    created_by = factory.SubFactory(UserFactory)

    class Meta:
        model = PostTranslation

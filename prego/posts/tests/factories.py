import factory

from factory.django import DjangoModelFactory

from prego.users.tests.factories import UserFactory
from prego.posts.models import Post, PostTranslation


class PostFactory(DjangoModelFactory):
    slug = factory.Faker("slug")
    created_by = factory.SubFactory(UserFactory)

    class Meta:
        model = Post


class PostTranslationFactory(DjangoModelFactory):
    post = factory.SubFactory(PostFactory)
    title = factory.Faker("text")
    body = factory.Faker("paragraph")
    created_by = factory.SubFactory(UserFactory)

    class Meta:
        model = PostTranslation

import factory

from factory.django import DjangoModelFactory

from blog.users.tests.factories import UserFactory
from blog.posts.models import Post, PostTranslation


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

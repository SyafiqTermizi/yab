from django.db.models.signals import post_save

import factory
from factory.django import DjangoModelFactory

from prego.users.models import User, EmailVerificationToken


@factory.django.mute_signals(post_save)
class UserFactory(DjangoModelFactory):
    username = factory.Faker("name")
    email = factory.Faker("email")

    class Meta:
        model = User


class EmailVerificationTokenFactory(DjangoModelFactory):
    token = factory.Faker("paragraph")
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = EmailVerificationToken

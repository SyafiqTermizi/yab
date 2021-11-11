from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import PrimaryKeyRelatedField

from .models import Post, PostTranslation, Languages


class PrimaryKeyRelatedFieldWithCustomMessage(PrimaryKeyRelatedField):
    default_error_messages = {
        "required": _("This field is required."),
        "does_not_exist": _(
            "Invalid choice - Please select from one of the available choice."
        ),
        "incorrect_type": _(
            "Invalid choice - Please select from one of the available choice."
        ),
    }


class PostTranslationSerializer(serializers.ModelSerializer):
    post = PrimaryKeyRelatedFieldWithCustomMessage(
        queryset=Post.objects.get_post_with_incomplete_translation(),
        required=False,
    )
    language = serializers.ChoiceField(choices=Languages.choices)

    class Meta:
        model = PostTranslation
        fields = [
            "post",
            "title",
            "json_body",
            "html_body",
            "language",
            "draft",
        ]

    def validate(self, data):
        validated_data = dict(super().validate(data))

        is_new_translation_entry = not self.instance and validated_data.get(
            "post", None
        )

        if is_new_translation_entry:

            languages = list(
                validated_data["post"].translations.values_list("language", flat=True)
            )
            if validated_data["language"] in languages:
                raise serializers.ValidationError(
                    {
                        "post": f"{validated_data['language'].capitalize()} translation for {validated_data['post'].slug} already exist",
                    }
                )

        return validated_data

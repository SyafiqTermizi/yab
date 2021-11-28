from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import PrimaryKeyRelatedField

from .models import Post, PostTranslation, Languages, PostTranslationImage


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

        is_new_post = not self.instance and not validated_data.get("post", None)
        is_new_translation_entry = not self.instance and validated_data.get(
            "post", None
        )

        if not self.instance:
            if validated_data["language"] != Languages.ZH:
                slug = slugify(validated_data["title"])
            else:
                slug = validated_data["title"].replace(" ", "-")
            validated_data.update({"slug": slug})

        if is_new_post:
            post = Post.objects.create(
                created_by=self.context["created_by"],
            )

            validated_data.update({"post": post})

        elif is_new_translation_entry:

            languages = list(
                validated_data["post"].translations.values_list("language", flat=True)
            )
            if validated_data["language"] in languages:
                raise serializers.ValidationError(
                    {
                        "post": f"{validated_data['language'].capitalize()} translation for {validated_data['post']} already exist",
                    }
                )

        return validated_data


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTranslationImage
        fields = ["image"]

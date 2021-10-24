from django.utils.text import slugify
from rest_framework import serializers

from .models import Post, PostTranslation, Languages


class PostTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTranslation
        fields = [
            "post",
            "title",
            "body",
            "language",
            "draft",
        ]

    def validate(self, data):
        validated_data = dict(super().validate(data))

        is_new_post_in_en = (
            not self.instance
            and validated_data["language"] == Languages.EN
            and not validated_data.get("post", None)
        )
        is_new_post_not_in_en = (
            not self.instance
            and validated_data["language"] != Languages.EN
            and not validated_data.get("post", None)
        )
        is_new_translation_entry = not self.instance and validated_data.get(
            "post", None
        )

        if is_new_post_in_en:
            validated_data.update(
                {
                    "post_id": Post.objects.create(
                        slug=slugify(validated_data["title"]),
                        created_by=self.context["created_by"],
                    ).pk
                }
            )
        elif is_new_post_not_in_en:
            raise serializers.ValidationError(
                {
                    "language": f"Initial post must be in {Languages.EN}",
                }
            )

        if is_new_translation_entry:
            languages = list(
                self.instance.post.translations.values_list("language", flat=True)
            )
            if self.instance.language in languages:
                raise serializers.ValidationError(
                    {
                        "post": f"{self.instance.language.capitalize()} translation for {self.instance.post.slug} already exist",
                    }
                )

        return validated_data

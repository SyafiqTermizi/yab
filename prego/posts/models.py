from django.db import models
from django.db.models.aggregates import Count

from prego.users.models import User


def get_seo_image_path(instance, filename: str):
    return f"posts/{instance.post.post.slug}/seo/{filename}"


class Languages(models.TextChoices):
    EN = "en", "English"
    MS = "ms", "Bahasa Melayu"
    ZH = "zh", "Zhongweng"


class PostManager(models.Manager):
    def get_post_with_incomplete_translation(self):
        return self.annotate(
            translation_count=Count("translations"),
        ).filter(translation_count__lt=len(Languages.choices))


class Post(models.Model):
    slug = models.SlugField()

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
    )

    objects = PostManager()

    def __str__(self) -> str:
        return self.slug


class PostTranslation(models.Model):
    post: Post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name="translations",
        blank=True,
    )

    title = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    language = models.CharField(
        max_length=10,
        choices=Languages.choices,
        default=Languages.EN,
    )
    draft = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        to=User,
        related_name="posts",
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self) -> str:
        return f"{self.post.slug} ({self.language})"


class PostSeo(models.Model):
    post: PostTranslation = models.OneToOneField(
        to=PostTranslation,
        on_delete=models.CASCADE,
        related_name="seo",
    )
    title = models.CharField(max_length=88, blank=True)
    summary = models.TextField(max_length=200, blank=True)
    image = models.ImageField(blank=True, upload_to=get_seo_image_path)

    def __str__(self) -> str:
        return f"SEO Config: {self.post.__str__()}"

    def save(self, *args, **kwargs):
        if not self.pk and not self.title:
            self.title = self.post.title[:88]
        return super().save(*args, **kwargs)

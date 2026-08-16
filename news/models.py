from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Blog(models.Model):

    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )

    title = models.CharField(
        max_length=200
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    featured_image = models.ImageField(
        upload_to="blogs/",
        blank=True,
        null=True
    )

    excerpt = models.TextField()

    content = models.TextField()

    author = models.CharField(
        max_length=100,
        default="Line Eight"
    )

    category = models.CharField(
        max_length=100,
        blank=True
    )

    reading_time = models.PositiveIntegerField(
        default=5,
        help_text="Estimated reading time in minutes."
    )

    meta_description = models.CharField(
        max_length=160,
        blank=True
    )

    featured = models.BooleanField(
        default=False
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ["-created_at"]

        verbose_name = "Blog"

        verbose_name_plural = "Blogs"

    def save(self, *args, **kwargs):

        if not self.slug:

            base_slug = slugify(self.title)

            slug = base_slug

            counter = 1

            while Blog.objects.filter(slug=slug).exclude(pk=self.pk).exists():

                slug = f"{base_slug}-{counter}"

                counter += 1

            self.slug = slug

        if not self.meta_description:

            self.meta_description = self.excerpt[:160]

        super().save(*args, **kwargs)

    def get_absolute_url(self):

        return reverse(
            "blog_detail",
            kwargs={
                "slug": self.slug
            }
        )

    def __str__(self):

        return self.title


class Subscriber(models.Model):

    email = models.EmailField(
        unique=True
    )

    subscribed_at = models.DateTimeField(
        auto_now_add=True
    )

    active = models.BooleanField(
        default=True
    )

    class Meta:

        ordering = ["-subscribed_at"]

        verbose_name = "Subscriber"

        verbose_name_plural = "Subscribers"

    def __str__(self):

        return self.email    
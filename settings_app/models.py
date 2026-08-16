from django.db import models


class SiteSettings(models.Model):

    company_name = models.CharField(
        max_length=150,
        default="Line Eight"
    )

    tagline = models.CharField(
        max_length=255,
        blank=True
    )

    logo = models.ImageField(
        upload_to="settings/",
        blank=True,
        null=True
    )

    favicon = models.ImageField(
        upload_to="settings/",
        blank=True,
        null=True
    )

    email = models.EmailField(
        blank=True
    )

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    whatsapp = models.CharField(
        max_length=30,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    google_maps = models.TextField(
        blank=True,
        help_text="Paste Google Maps embed code."
    )

    facebook = models.URLField(blank=True)

    instagram = models.URLField(blank=True)

    linkedin = models.URLField(blank=True)

    youtube = models.URLField(blank=True)

    tiktok = models.URLField(blank=True)

    twitter = models.URLField(blank=True)

    footer_text = models.TextField(
        blank=True
    )

    copyright_text = models.CharField(
        max_length=255,
        blank=True
    )

    seo_title = models.CharField(
        max_length=255,
        blank=True
    )

    seo_description = models.TextField(
        blank=True
    )

    seo_keywords = models.CharField(
        max_length=255,
        blank=True
    )

    def __str__(self):
        return "Website Settings"
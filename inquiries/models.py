from django.db import models


class Inquiry(models.Model):

    STATUS_CHOICES = (
        ("new", "New"),
        ("read", "Read"),
        ("replied", "Replied"),
    )

    SERVICE_CHOICES = (
        ("Website Design", "Website Design"),
        ("Graphic Design", "Graphic Design"),
        ("Branding", "Branding"),
        ("Photography", "Photography"),
        ("Videography", "Videography"),
        ("Other", "Other"),
    )

    name = models.CharField(
        max_length=120
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    company = models.CharField(
        max_length=120,
        blank=True
    )

    service = models.CharField(
        max_length=100,
        choices=SERVICE_CHOICES
    )

    budget = models.CharField(
        max_length=100,
        blank=True
    )

    subject = models.CharField(
        max_length=200,
        blank=True
    )

    message = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ["-created_at"]

        verbose_name = "Inquiry"

        verbose_name_plural = "Inquiries"

    def __str__(self):

        return f"{self.name} - {self.service}"
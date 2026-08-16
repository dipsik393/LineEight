from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):

    STATUS_CHOICES = (

        ("active", "Active"),

        ("inactive", "Inactive"),

    )

    user = models.OneToOneField(

        User,

        on_delete=models.CASCADE,

        related_name="client_profile"

    )

    company = models.CharField(

        max_length=200,

        blank=True

    )

    phone = models.CharField(

        max_length=30,

        blank=True

    )

    position = models.CharField(

        max_length=100,

        blank=True

    )

    avatar = models.ImageField(

        upload_to="clients/",

        blank=True,

        null=True

    )

    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default="active"

    )

    notes = models.TextField(

        blank=True

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    updated_at = models.DateTimeField(

        auto_now=True

    )

    class Meta:

        ordering = ["user__first_name"]

    def __str__(self):

        if self.company:

            return self.company

        return self.user.get_full_name()


class ProjectUpdate(models.Model):

    project = models.ForeignKey(
        "portfolio.Project",
        on_delete=models.CASCADE,
        related_name="updates"
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField()

    status = models.CharField(
        max_length=100,
        default="Update"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.project.title} - {self.title}"    


class ProjectFile(models.Model):

    project = models.ForeignKey(
        "portfolio.Project",
        on_delete=models.CASCADE,
        related_name="files"
    )

    name = models.CharField(
        max_length=200
    )

    file = models.FileField(
        upload_to="client_projects/files/"
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
        

class Message(models.Model):

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    project = models.ForeignKey(
        "portfolio.Project",
        on_delete=models.CASCADE,
        related_name="messages"
    )

    sender = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="sent_client_messages"
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.client} - {self.project}"        



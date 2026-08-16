from django.db import models
from django.utils.text import slugify
from clients.models import Client

class Project(models.Model):

    STATUS = (
        ("draft", "Draft"),
        ("published", "Published"),
    )

    title = models.CharField(max_length=200)

    slug = models.SlugField(unique=True, blank=True)

    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projects"
    )

    service = models.CharField(max_length=200)

    industry = models.CharField(max_length=200)

    

    duration = models.CharField(max_length=100)

    hero_image = models.ImageField(upload_to="projects/heroes/")

    website_url = models.URLField(blank=True)

    short_description = models.TextField()

    overview = models.TextField()

    featured = models.BooleanField(default=False)

    project_type = models.CharField(
    max_length=100,
    blank=True
    )

    challenge = models.TextField(blank=True)

    solution = models.TextField(blank=True)

    results = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="draft"
    )

    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projects"
    )

    owner = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="owned_projects"
    )
    cta_tag = models.CharField(
    max_length=100,
    default="LET'S BUILD SOMETHING AMAZING")
    cta_title = models.CharField(
    max_length=200,
    default="Ready to build your next project?"
    )

    cta_text = models.TextField(
    default="Let's build something exceptional together.")



    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)


    class Meta:

        ordering = ["-created_at"]


    def save(self, *args, **kwargs):

        if not self.slug:

            self.slug = slugify(self.title)

        super().save(*args, **kwargs)


    def __str__(self):

        return self.title
    


class ProjectImage(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="gallery"
    )

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to="projects/gallery/"
    )

    order = models.PositiveIntegerField(default=0)


    class Meta:

        ordering = ["order"]


    def __str__(self):

        return f"{self.project.title} - {self.title}"
    


class ProjectStep(models.Model):

    ICONS = (

        ("search", "Research"),

        ("palette", "Design"),

        ("code", "Development"),

        ("rocket", "Launch"),

    )

    project = models.ForeignKey(

        Project,

        on_delete=models.CASCADE,

        related_name="steps"

    )

    number = models.PositiveIntegerField()

    title = models.CharField(max_length=100)

    description = models.TextField()

    icon = models.CharField(

        max_length=30,

        choices=ICONS

    )


    class Meta:

        ordering = ["number"]


    def __str__(self):

        return self.title
    

class Category(models.Model):

    name = models.CharField(max_length=100)

    slug = models.SlugField(unique=True)




    def __str__(self):

        return self.name    
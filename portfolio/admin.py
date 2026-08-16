from django.contrib import admin
from .models import Project, Category, ProjectImage, ProjectStep


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


class ProjectStepInline(admin.TabularInline):
    model = ProjectStep
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "client",
        "industry",
        "status",
        "featured",
    )

    list_filter = (
        "status",
        "featured",  
        "category",
    )

    search_fields = (
        "title",
        "client",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    inlines = [
        ProjectImageInline,
        ProjectStepInline,
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    prepopulated_fields = {
        "slug": ("name",)
    }


admin.site.register(ProjectImage)
admin.site.register(ProjectStep)
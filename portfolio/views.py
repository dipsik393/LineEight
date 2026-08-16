from django.shortcuts import get_object_or_404, render

from .models import Project


def project_detail(request, slug):

    project = get_object_or_404(

        Project,

        slug=slug,

        status="published"

    )

    related_projects = (
        Project.objects
        .filter(status="published")
        .exclude(id=project.id)
        .order_by("-featured", "-created_at")[:3]
    )


    return render(

        request,

        "project_detail.html",

        {

            "project": project,
            "related_projects": related_projects,
            

        }

    )




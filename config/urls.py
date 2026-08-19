"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from portfolio.models import ProjectImage

def cloudinary_debug(request):
    img = ProjectImage.objects.first()

    return JsonResponse({
        "database_engine": settings.DATABASES["default"]["ENGINE"],
        "database_name": str(settings.DATABASES["default"]["NAME"]),
        "cloudinary_cloud": settings.CLOUDINARY_STORAGE.get("CLOUD_NAME"),
        "image_name": img.image.name if img else None,
        "image_url": img.image.url if img else None,
    })

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("website.urls")),
    path("dashboard/", include("core_dashboard.urls")),
    path("portfolio/",include("portfolio.urls")),
    path("dashboard/settings/",include("settings_app.urls")),
    path("dashboard/clients/",include("clients.urls")),
    path("dashboard/ai/",include("ai_agent.urls")),
    path("cloudinary-debug/", cloudinary_debug),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )



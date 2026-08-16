from django.shortcuts import render, redirect

from .models import SiteSettings
from .forms import SiteSettingsForm


def settings_view(request):

    settings, created = SiteSettings.objects.get_or_create(
        id=1
    )

    if request.method == "POST":

        form = SiteSettingsForm(

            request.POST,

            request.FILES,

            instance=settings

        )

        if form.is_valid():

            form.save()

            return redirect("dashboard_settings")

    else:

        form = SiteSettingsForm(
            instance=settings
        )

    return render(

        request,

        "dashboard/settings/settings.html",

        {

            "form": form

        }

    )
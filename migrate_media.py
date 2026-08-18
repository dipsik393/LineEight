import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from portfolio.models import Project, ProjectImage
from clients.models import Client, ProjectFile
from news.models import Blog
from settings_app.models import SiteSettings


BASE_DIR = Path(__file__).resolve().parent
MEDIA_ROOT = BASE_DIR / "media"


def upload_field(obj, field_name):
    field = getattr(obj, field_name)

    if not field:
        return False

    current_name = field.name

    # Already migrated to Cloudinary
    if current_name.startswith("http://") or current_name.startswith("https://"):
        print(f"SKIP   {obj} -> already external")
        return True

    local_path = MEDIA_ROOT / current_name

    if not local_path.exists():
        print(f"MISSING {obj} -> {current_name}")
        return False

    print(f"UPLOAD {obj} -> {current_name}")

    # Open local file and save it through the configured storage.
    with open(local_path, "rb") as f:
        field.save(
            Path(current_name).name,
            f,
            save=False,
        )

    obj.save(update_fields=[field_name])

    print(f"OK     {obj} -> {field.name}")

    return True


print("\n=== PROJECT HERO IMAGES ===")

for project in Project.objects.all():
    upload_field(project, "hero_image")


print("\n=== PROJECT GALLERY IMAGES ===")

for image in ProjectImage.objects.all():
    upload_field(image, "image")


print("\n=== CLIENT AVATARS ===")

for client in Client.objects.all():
    upload_field(client, "avatar")


print("\n=== PROJECT FILES ===")

for project_file in ProjectFile.objects.all():
    upload_field(project_file, "file")


print("\n=== BLOG IMAGES ===")

for blog in Blog.objects.all():
    upload_field(blog, "featured_image")


print("\n=== SITE SETTINGS ===")

for settings in SiteSettings.objects.all():
    upload_field(settings, "logo")
    upload_field(settings, "favicon")


print("\n================================")
print("MEDIA MIGRATION COMPLETE")
print("================================")
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from portfolio.models import Project, ProjectImage


BASE_DIR = Path(__file__).resolve().parent
MEDIA_DIR = BASE_DIR / "media"


def find_original_file(name):
    if not name:
        return None

    name = Path(name).name

    stem = Path(name).stem

    parts = stem.split("_")

    candidates = []

    for i in range(len(parts), 0, -1):
        candidates.append("_".join(parts[:i]))

    for candidate in candidates:
        matches = list(MEDIA_DIR.rglob(candidate + ".*"))

        if matches:
            return matches[0]

    return None


def migrate_image(instance, field_name, label):

    field = getattr(instance, field_name)

    if not field:
        return

    original_name = field.name

    print("\n" + label)
    print(f"Database BEFORE: {original_name}")

    local_file = find_original_file(original_name)

    if not local_file:
        print("❌ LOCAL FILE NOT FOUND")
        return

    print(f"FOUND: {local_file}")

    try:

        with open(local_file, "rb") as f:

            uploaded_name = field.storage.save(
                original_name,
                f
            )

        print(f"✅ CLOUDINARY: {uploaded_name}")

        # IMPORTANT:
        # Update the database with the actual Cloudinary name
        setattr(instance, field_name, uploaded_name)

        instance.save(update_fields=[field_name])

        print(f"✅ DATABASE UPDATED: {uploaded_name}")

        # Verify
        updated_field = getattr(instance, field_name)

        print(f"URL: {updated_field.url}")

    except Exception as e:

        print(f"❌ ERROR: {e}")


print("\n==============================")
print("PROJECT HERO IMAGES")
print("==============================")


for project in Project.objects.all():

    migrate_image(
        project,
        "hero_image",
        project.title
    )


print("\n==============================")
print("PROJECT GALLERY IMAGES")
print("==============================")


for image in ProjectImage.objects.all():

    migrate_image(
        image,
        "image",
        f"{image.project.title} / {image.title}"
    )


print("\n==============================")
print("MIGRATION FINISHED")
print("==============================")
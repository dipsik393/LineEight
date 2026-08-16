from clients.models import Client, ProjectUpdate, ProjectFile, Message


def get_client_projects(client):
    projects = client.projects.select_related(
        "category"
    ).all()

    return [
        {
            "id": project.id,
            "title": project.title,
            "service": project.service,
            "industry": project.industry,
            "status": project.status,
            "duration": project.duration,
            "description": project.short_description,
            "created_at": project.created_at.strftime("%Y-%m-%d"),
        }
        for project in projects
    ]


def get_client_updates(client):
    updates = ProjectUpdate.objects.filter(
        project__client=client
    ).select_related("project")

    return [
        {
            "id": update.id,
            "project": update.project.title,
            "title": update.title,
            "description": update.description,
            "status": update.status,
            "created_at": update.created_at.strftime(
                "%Y-%m-%d %H:%M"
            ),
        }
        for update in updates
    ]


def get_client_files(client):
    files = ProjectFile.objects.filter(
        project__client=client
    ).select_related("project")

    return [
        {
            "id": file.id,
            "name": file.name,
            "project": file.project.title,
            "description": file.description,
            "url": file.file.url if file.file else "",
            "created_at": file.created_at.strftime(
                "%Y-%m-%d %H:%M"
            ),
        }
        for file in files
    ]


def get_client_messages(client):
    messages = Message.objects.filter(
        client=client
    ).select_related(
        "project",
        "sender",
    )

    return [
        {
            "id": message.id,
            "project": message.project.title,
            "sender": (
                message.sender.get_full_name()
                or message.sender.username
            ),
            "message": message.message,
            "is_read": message.is_read,
            "created_at": message.created_at.strftime(
                "%Y-%m-%d %H:%M"
            ),
        }
        for message in messages
    ]


def get_client_overview(client):
    return {
        "client": (
            client.user.get_full_name()
            or client.user.username
        ),
        "company": client.company,
        "status": client.status,
        "projects": len(get_client_projects(client)),
        "updates": len(get_client_updates(client)),
        "files": len(get_client_files(client)),
        "messages": len(get_client_messages(client)),
    }
from clients.models import Client, ProjectUpdate, ProjectFile, Message
from portfolio.models import Project
from inquiries.models import Inquiry


def get_clients():
    clients = Client.objects.select_related("user").all()

    return [
        {
            "id": client.id,
            "name": client.user.get_full_name(),
            "username": client.user.username,
            "email": client.user.email,
            "company": client.company,
            "phone": client.phone,
            "position": client.position,
            "status": client.status,
        }
        for client in clients
    ]


def get_projects():
    projects = Project.objects.select_related(
        "client",
        "client__user",
        "category",
    ).all()

    return [
        {
            "id": project.id,
            "title": project.title,
            "client": (
                project.client.user.get_full_name()
                if project.client
                else "No client"
            ),
            "service": project.service,
            "industry": project.industry,
            "category": (
                project.category.name
                if project.category
                else "Uncategorized"),
            "status": project.status,
            "featured": project.featured,
            "created_at": project.created_at.strftime(
                "%Y-%m-%d"
            ),
        }
        for project in projects
    ]


def get_inquiries():
    inquiries = Inquiry.objects.all()

    return [
        {
            "id": inquiry.id,
            "name": inquiry.name,
            "email": inquiry.email,
            "phone": inquiry.phone,
            "company": inquiry.company,
            "service": inquiry.service,
            "budget": inquiry.budget,
            "subject": inquiry.subject,
            "status": inquiry.status,
            "created_at": inquiry.created_at.strftime(
                "%Y-%m-%d"
            ),
        }
        for inquiry in inquiries
    ]


def get_messages():
    messages = Message.objects.select_related(
        "client",
        "client__user",
        "project",
        "sender",
    ).order_by("-created_at")

    return [
        {
            "id": message.id,
            "client": message.client.user.get_full_name(),
            "project": message.project.title,
            "sender": message.sender.get_full_name()
            or message.sender.username,
            "message": message.message,
            "is_read": message.is_read,
            "created_at": message.created_at.strftime(
                "%Y-%m-%d %H:%M"
            ),
        }
        for message in messages
    ]


def get_dashboard_stats():
    return {
        "total_clients": Client.objects.count(),

        "active_clients": Client.objects.filter(
            status="active"
        ).count(),

        "total_projects": Project.objects.count(),

        "published_projects": Project.objects.filter(
            status="published"
        ).count(),

        "draft_projects": Project.objects.filter(
            status="draft"
        ).count(),

        "total_inquiries": Inquiry.objects.count(),

        "new_inquiries": Inquiry.objects.filter(
            status="new"
        ).count(),

        "unread_messages": Message.objects.filter(
            is_read=False
        ).count(),

        "total_files": ProjectFile.objects.count(),

        "total_updates": ProjectUpdate.objects.count(),
    }




# ==========================================
# CLIENT PROJECTS
# ==========================================

def get_my_projects(client):

    projects = (
        Project.objects
        .filter(client=client)
        .select_related("category")
        .order_by("-created_at")
    )

    return [
        {
            "id": project.id,
            "title": project.title,
            "service": project.service,
            "industry": project.industry,
            "status": project.status,
            "featured": project.featured,
            "created_at": project.created_at.strftime("%Y-%m-%d"),
        }
        for project in projects
    ]


# ==========================================
# CLIENT PROJECT UPDATES
# ==========================================

def get_my_updates(client):

    updates = (
        ProjectUpdate.objects
        .filter(project__client=client)
        .select_related("project")
        .order_by("-created_at")
    )

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


# ==========================================
# CLIENT FILES
# ==========================================

def get_my_files(client):

    files = (
        ProjectFile.objects
        .filter(project__client=client)
        .select_related("project")
        .order_by("-created_at")
    )

    return [
        {
            "id": file.id,
            "name": file.name,
            "project": file.project.title,
            "description": file.description,
            "created_at": file.created_at.strftime(
                "%Y-%m-%d %H:%M"
            ),
        }
        for file in files
    ]


# ==========================================
# CLIENT MESSAGES
# ==========================================

def get_my_messages(client):

    messages = (
        Message.objects
        .filter(client=client)
        .select_related(
            "project",
            "sender",
        )
        .order_by("-created_at")
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
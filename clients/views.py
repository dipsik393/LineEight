from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test, login_required
from django.db import models
from portfolio.models import Project
from inquiries.models import Inquiry
from .models import Client,ProjectUpdate,ProjectFile,Message
from .forms import ClientForm
from django.contrib.auth import update_session_auth_hash
from django.http import FileResponse




def staff_required(view_func):

    return user_passes_test(
        lambda user: user.is_staff
    )(view_func)


@staff_required
def client_list(request):

    clients = Client.objects.select_related("user")

    return render(

        request,

        "dashboard/clients/client_list.html",

        {

            "clients": clients

        }

    )

@staff_required
def client_create(request):

    if request.method == "POST":

        form = ClientForm(

            request.POST,

            request.FILES

        )

        if form.is_valid():

            user = User.objects.create_user(

                username=form.cleaned_data["username"],

                first_name=form.cleaned_data["first_name"],

                last_name=form.cleaned_data["last_name"],

                email=form.cleaned_data["email"],

                password=form.cleaned_data["password"]

                or "ChangeMe123"

            )

            client = form.save(

                commit=False

            )

            client.user = user

            client.save()

            return redirect(

                "dashboard_clients"

            )

    else:

        form = ClientForm()

    return render(

        request,

        "dashboard/clients/client_form.html",

        {

            "form": form,

            "title": "Create Client"

        }

    )

@staff_required
def client_edit(request, pk):

    client = get_object_or_404(

        Client,

        pk=pk

    )

    user = client.user

    if request.method == "POST":

        form = ClientForm(

            request.POST,

            request.FILES,

            instance=client

        )

        if form.is_valid():

            user.first_name = form.cleaned_data["first_name"]

            user.last_name = form.cleaned_data["last_name"]

            user.email = form.cleaned_data["email"]

            user.username = form.cleaned_data["username"]

            if form.cleaned_data["password"]:

                user.set_password(

                    form.cleaned_data["password"]

                )

            user.save()

            form.save()

            return redirect(

                "dashboard_clients"

            )

    else:

        form = ClientForm(

            instance=client,

            initial={

                "first_name": user.first_name,

                "last_name": user.last_name,

                "email": user.email,

                "username": user.username,

            }

        )

    return render(

        request,

        "dashboard/clients/client_form.html",

        {

            "form": form,

            "title": "Edit Client"

        }

    )

@staff_required
def client_delete(request, pk):

    client = get_object_or_404(

        Client,

        pk=pk

    )

    if request.method == "POST":

        client.user.delete()

        return redirect(

            "dashboard_clients"

        )

    return render(

        request,

        "dashboard/clients/client_delete.html",

        {

            "client": client

        }

    )
def client_login(request):

    if request.user.is_authenticated:

        if Client.objects.filter(
            user=request.user
        ).exists():

            return redirect("client_dashboard")

        logout(request)

    error = None

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            if user.is_active:

                if Client.objects.filter(
                    user=user
                ).exists():

                    login(
                        request,
                        user
                    )

                    return redirect(
                        "client_dashboard"
                    )

        error = "Invalid client username or password."

    return render(
        request,
        "client/login.html",
        {
            "error": error
        }
    )

@login_required(login_url="client_login")
def client_dashboard(request):

    client = Client.objects.filter(
        user=request.user
    ).first()

    if not client:

        logout(request)

        return redirect("client_login")

    projects = client.projects.select_related(
        "category"
    ).filter(
        status="published"
    ).order_by(
        "-created_at"
    )

    context = {
        "client": client,

        "projects": projects,

        "project_count": projects.count(),

        "message_count": 0,

        "invoice_count": 0,

        "meeting_count": 0,
    }

    return render(
        request,
        "client/dashboard.html",
        context
    )


@login_required(login_url="client_login")
def client_projects(request):

    client = Client.objects.filter(
        user=request.user
    ).first()

    if not client:

        logout(request)

        return redirect("client_login")

    projects = Project.objects.filter(
        client=client
    ).select_related(
        "category"
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "client/projects.html",
        {
            "client": client,
            "projects": projects,
        }
    )



@login_required(login_url="client_login")
def client_project_detail(request, pk):

    client = Client.objects.filter(
        user=request.user
    ).first()

    if not client:

        logout(request)

        return redirect("client_login")

    project = get_object_or_404(
        Project,
        pk=pk,
        client=client,
        status="published"
    )

    updates = project.updates.all()

    files = project.files.all()

    return render(
        request,
        "client/project_detail.html",
        {
            "client": client,
            "project": project,
            "updates": updates,
            "files": files,
        }
    )


def client_logout(request):

    logout(request)

    return redirect("client_login")

@staff_required
def project_updates(request, project_id):

    project = get_object_or_404(
        Project,
        pk=project_id
    )

    updates = ProjectUpdate.objects.filter(
        project=project
    )

    return render(
        request,
        "dashboard/clients/project_updates.html",
        {
            "project": project,
            "updates": updates,
        }
    )

@staff_required
def project_update_create(request, project_id):

    project = get_object_or_404(
        Project,
        pk=project_id
    )

    if request.method == "POST":

        title = request.POST.get("title")
        description = request.POST.get("description")
        status = request.POST.get("status")

        ProjectUpdate.objects.create(
            project=project,
            title=title,
            description=description,
            status=status
        )

        return redirect(
            "project_updates",
            project_id=project.id
        )

    return render(
        request,
        "dashboard/clients/project_update_form.html",
        {
            "project": project,
        }
    )
@staff_required
def dashboard_client_projects(request, client_id):

    client = get_object_or_404(
        Client,
        id=client_id
    )

    projects = Project.objects.filter(
        client=client
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "dashboard/clients/client_projects.html",
        {
            "client": client,
            "projects": projects,
        }
    )
@staff_required
def project_file_create(request, project_id):

    project = get_object_or_404(
        Project,
        pk=project_id
    )

    if request.method == "POST":

        name = request.POST.get("name")
        description = request.POST.get("description")
        uploaded_file = request.FILES.get("file")

        if uploaded_file:

            ProjectFile.objects.create(
                project=project,
                name=name,
                description=description,
                file=uploaded_file
            )

            return redirect(
                "project_files",
                project_id=project.id
            )

    return render(
        request,
        "dashboard/clients/project_file_form.html",
        {
            "project": project
        }
    )

@staff_required
def project_files(request, project_id):

    project = get_object_or_404(
        Project,
        pk=project_id
    )

    files = ProjectFile.objects.filter(
        project=project
    )

    return render(
        request,
        "dashboard/clients/project_files.html",
        {
            "project": project,
            "files": files
        }
    )


@login_required(login_url="client_login")
def client_messages(request, project_id):

    client = get_object_or_404(
        Client,
        user=request.user
    )

    project = get_object_or_404(
        Project,
        id=project_id,
        client=client
    )

    messages = Message.objects.filter(
        client=client,
        project=project
    ).select_related(
        "sender"
    )

    # Mark Line Eight messages as read
    Message.objects.filter(
        client=client,
        project=project,
        is_read=False
    ).exclude(
        sender=request.user
    ).update(
        is_read=True
    )

    if request.method == "POST":

        message_text = request.POST.get(
            "message"
        )

        if message_text:

            Message.objects.create(
                client=client,
                project=project,
                sender=request.user,
                message=message_text
            )

            return redirect(
                "client_messages",
                project_id=project.id
            )

    return render(
        request,
        "client/messages.html",
        {
            "client": client,
            "project": project,
            "messages": messages
        }
    )


@staff_required
def dashboard_messages(request):

    messages = Inquiry.objects.all()

    search = request.GET.get("search", "").strip()
    status = request.GET.get("status", "").strip()

    if search:

        messages = messages.filter(
            models.Q(name__icontains=search)
            | models.Q(email__icontains=search)
            | models.Q(company__icontains=search)
            | models.Q(subject__icontains=search)
            | models.Q(message__icontains=search)
        )

    if status:

        messages = messages.filter(
            status=status
        )

    return render(
        request,
        "dashboard/messages/message_list.html",
        {
            "messages": messages,
            "search": search,
            "status": status,
        }
    )



@staff_required
def dashboard_message_detail(request, pk):

    message = get_object_or_404(
        Message.objects.select_related(
            "client",
            "client__user",
            "project",
            "sender",
        ),
        pk=pk
    )

    # Mark the client's message as read
    if (
        message.sender == message.client.user
        and not message.is_read
    ):
        message.is_read = True
        message.save(update_fields=["is_read"])

    # Send staff reply
    if request.method == "POST":

        reply = request.POST.get("message", "").strip()

        if reply:

            Message.objects.create(
                client=message.client,
                project=message.project,
                sender=request.user,
                message=reply,
                is_read=False,
            )

            return redirect(
                "dashboard_message_detail",
                pk=pk
            )

    # Get the entire conversation
    conversation = (
        Message.objects
        .filter(
            client=message.client,
            project=message.project
        )
        .select_related("sender")
        .order_by("created_at")
    )

    return render(
        request,
        "dashboard/messages/message_detail.html",
        {
            "message": message,
            "conversation": conversation,
        }
    )


@staff_required
def dashboard_message_delete(request, pk):

    if request.method != "POST":
        return redirect("dashboard_messages")

    message = Message.objects.filter(
        pk=pk
    ).first()

    if message:
        message.delete()

    return redirect("dashboard_messages")


@login_required(login_url="client_login")
def client_files(request):

    client = Client.objects.filter(
        user=request.user
    ).first()

    if not client:

        logout(request)

        return redirect("client_login")

    files = ProjectFile.objects.filter(
        project__client=client
    ).select_related(
        "project"
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "client/files.html",
        {
            "client": client,
            "files": files,
        }
    )


@login_required(login_url="client_login")
def client_messages_list(request):

    client = Client.objects.filter(
        user=request.user
    ).first()

    if not client:

        logout(request)

        return redirect("client_login")

    messages = Message.objects.filter(
        client=client
    ).select_related(
        "project",
        "sender"
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "client/messages_list.html",
        {
            "client": client,
            "messages": messages,
        }
    )



@staff_required
def client_messages_dashboard(request):

    messages = (
        Message.objects
        .select_related(
            "client",
            "client__user",
            "project",
            "sender",
        )
        .order_by("-created_at")
    )

    unread_count = messages.filter(
        is_read=False
    ).exclude(
        sender=request.user
    ).count()

    return render(
        request,
        "dashboard/client_messages/message_list.html",
        {
            "messages": messages,
            "unread_count": unread_count,
        }
    )

@staff_required
def dashboard_inquiry_detail(request, pk):

    inquiry = get_object_or_404(
        Inquiry,
        pk=pk
    )

    # Mark inquiry as read when staff opens it
    if inquiry.status == "new":
        inquiry.status = "read"
        inquiry.save(update_fields=["status"])

    return render(
        request,
        "dashboard/messages/inquiry_detail.html",
        {
            "inquiry": inquiry,
        }
    )


@staff_required
def dashboard_inquiry_delete(request, pk):

    inquiry = get_object_or_404(
        Inquiry,
        pk=pk
    )

    if request.method == "POST":

        inquiry.delete()

        return redirect(
            "dashboard_messages"
        )

    return render(
        request,
        "dashboard/messages/inquiry_delete.html",
        {
            "inquiry": inquiry,
        }
    )


@staff_required
def dashboard_inquiry_reply(request, pk):

    inquiry = get_object_or_404(
        Inquiry,
        pk=pk
    )

    if request.method == "POST":

        inquiry.status = "replied"

        inquiry.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return redirect(
            "dashboard_inquiry_detail",
            pk=inquiry.id
        )

    return render(
        request,
        "dashboard/messages/inquiry_reply.html",
        {
            "inquiry": inquiry,
        }
    )


@login_required(login_url="client_login")
def client_change_password(request):

    client = Client.objects.filter(
        user=request.user
    ).first()

    if not client:

        logout(request)

        return redirect("client_login")

    error = None
    success = None

    if request.method == "POST":

        current_password = request.POST.get(
            "current_password",
            ""
        )

        new_password = request.POST.get(
            "new_password",
            ""
        )

        confirm_password = request.POST.get(
            "confirm_password",
            ""
        )

        # Check current password
        if not request.user.check_password(
            current_password
        ):

            error = "Your current password is incorrect."

        # Check password length
        elif len(new_password) < 8:

            error = "Your new password must be at least 8 characters."

        # Check passwords match
        elif new_password != confirm_password:

            error = "The new passwords do not match."

        # Prevent using the same password
        elif current_password == new_password:

            error = "Your new password must be different from your current password."

        else:

            request.user.set_password(
                new_password
            )

            request.user.save()

            # Keep the client logged in
            update_session_auth_hash(
                request,
                request.user
            )

            success = "Your password has been changed successfully."

    return render(
        request,
        "client/change_password.html",
        {
            "client": client,
            "error": error,
            "success": success,
        }
    )


@login_required(login_url="client_login")
def client_file_download(request, pk):

    client = get_object_or_404(
        Client,
        user=request.user
    )

    project_file = get_object_or_404(
        ProjectFile,
        pk=pk,
        project__client=client
    )

    return FileResponse(
        project_file.file.open("rb"),
        as_attachment=True,
        filename=project_file.name
    )

def staff_login(request):

    if request.user.is_authenticated:

        if request.user.is_staff:
            return redirect("dashboard")

        logout(request)

    error = None

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            if user.is_active and user.is_staff:

                login(request, user)

                return redirect("dashboard")

        error = "Invalid staff username or password."

    return render(
        request,
        "dashboard/login.html",
        {
            "error": error
        }
    )


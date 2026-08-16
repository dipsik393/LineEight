from django.shortcuts import render, get_object_or_404, redirect
from portfolio.models import Project,  ProjectStep, ProjectImage
from   portfolio.forms import ProjectForm,ProjectImageForm,ProjectStepForm
from news.models import Blog
from news.forms import BlogForm
from news.models import Subscriber
from inquiries.models import Inquiry
from django.db.models import Q

from portfolio.models import Project
from news.models import Blog
from inquiries.models import Inquiry


def dashboard(request):

    context = {

        # Projects
        "project_count": Project.objects.count(),

        # Blogs
        "blog_count": Blog.objects.count(),

        "published_blogs": Blog.objects.filter(
            status="published"
        ).count(),

        "draft_blogs": Blog.objects.filter(
            status="draft"
        ).count(),

        # Messages
        "message_count": Inquiry.objects.count(),

        "new_messages": Inquiry.objects.filter(
            status="new"
        ).count(),

        "read_messages": Inquiry.objects.filter(
            status="read"
        ).count(),

        "replied_messages": Inquiry.objects.filter(
            status="replied"
        ).count(),

        # Recent Activity
        "recent_blogs": Blog.objects.order_by(
            "-created_at"
        )[:5],

        "recent_messages": Inquiry.objects.order_by(
            "-created_at"
        )[:5],

        "recent_projects": Project.objects.order_by(
            "-created_at"
        )[:5],

    }

    return render(

        request,

        "dashboard/dashboard.html",

        context

    )


def project_list(request):

    projects = Project.objects.all()

    return render(
        request,
        "dashboard/projects/project_list.html",
        {
            "projects": projects
        }
    )

def project_create(request):

    if request.method == "POST":

        form = ProjectForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect("dashboard_projects")

    else:

        form = ProjectForm()

    return render(
        request,
        "dashboard/projects/project_form.html",
        {
            "form": form
        }
    )


def project_gallery(request, pk):

    project = Project.objects.get(pk=pk)

    if request.method == "POST":

        form = ProjectImageForm(

            request.POST,

            request.FILES

        )

        if form.is_valid():

            image = form.save(commit=False)

            image.project = project

            image.save()

            return redirect(
                "dashboard_gallery",
                pk=project.pk
            )

    else:

        form = ProjectImageForm()

    gallery = project.gallery.all()

    return render(

        request,

        "dashboard/projects/project_gallery.html",

        {

            "project": project,

            "gallery": gallery,

            "form": form,

        }

    )

def project_edit(request, id):

    project = get_object_or_404(Project, id=id)

    if request.method == "POST":

        form = ProjectForm(
            request.POST,
            request.FILES,
            instance=project
        )

        if form.is_valid():

            form.save()

            return redirect("dashboard_projects")

    else:

        form = ProjectForm(instance=project)

    return render(
        request,
        "dashboard/projects/project_form.html",
        {
            "form": form
        }
    )


def project_delete(request, id):

    project = get_object_or_404(Project, id=id)

    project.delete()

    return redirect("dashboard_projects")


def gallery_delete(request, pk):

    image = get_object_or_404(
        ProjectImage,
        pk=pk
    )

    project_id = image.project.pk

    image.delete()

    return redirect(
        "dashboard_gallery",
        pk=project_id
    )


def project_process(request, pk):

    project = get_object_or_404(Project, pk=pk)

    if request.method == "POST":

        form = ProjectStepForm(request.POST)

        if form.is_valid():

            step = form.save(commit=False)

            step.project = project

            step.save()

            return redirect(
                "dashboard_project_process",
                pk=project.pk
            )

    else:

        form = ProjectStepForm()

    steps = project.steps.all()

    return render(

        request,

        "dashboard/projects/project_process.html",

        {

            "project": project,

            "steps": steps,

            "form": form,

        }

    )

def project_process_edit(request, pk):

    step = get_object_or_404(
        ProjectStep,
        pk=pk
    )

    if request.method == "POST":

        form = ProjectStepForm(
            request.POST,
            instance=step
        )

        if form.is_valid():

            form.save()

            return redirect(
                "dashboard_project_process",
                pk=step.project.pk
            )

    else:

        form = ProjectStepForm(
            instance=step
        )

    return render(

        request,

        "dashboard/projects/project_process_form.html",

        {

            "form": form,

            "project": step.project,

        }

    )

def project_process_delete(request, pk):

    step = get_object_or_404(
        ProjectStep,
        pk=pk
    )

    project = step.project

    step.delete()

    return redirect(
        "dashboard_project_process",
        pk=project.pk
    )

# ===============================
# BLOGS
# ===============================

def blog_list(request):

    search = request.GET.get("search")

    status = request.GET.get("status")


    blogs = Blog.objects.all()

    if search:

        blogs = blogs.filter(
            title__icontains=search
        )

    if status:

        blogs = blogs.filter(
            status=status
        )    

    return render(

        request,

        "dashboard/blogs/blog_list.html",

        {

            "blogs": blogs,

            "search": search,

            "status": status,


        }

    )




def blog_create(request):

    if request.method == "POST":

        form = BlogForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect("dashboard_blogs")

    else:

        form = BlogForm()

    return render(
        request,
        "dashboard/blogs/blog_form.html",
        {
            "form": form
        }
    )


def blog_edit(request, id):

    blog = get_object_or_404(
        Blog,
        id=id
    )

    if request.method == "POST":

        form = BlogForm(
            request.POST,
            request.FILES,
            instance=blog
        )

        if form.is_valid():

            form.save()

            return redirect("dashboard_blogs")

    else:

        form = BlogForm(instance=blog)

    return render(
        request,
        "dashboard/blogs/blog_form.html",
        {
            "form": form
        }
    )


def blog_delete(request, id):

    blog = get_object_or_404(
        Blog,
        id=id
    )

    blog.delete()

    return redirect("dashboard_blogs")

def subscriber_list(request):

    subscribers = Subscriber.objects.all()

    return render(

        request,

        "dashboard/subscribers/subscriber_list.html",

        {

            "subscribers": subscribers

        }

    )


def subscriber_delete(request, pk):

    subscriber = get_object_or_404(
        Subscriber,
        pk=pk
    )

    subscriber.delete()

    return redirect(
        "dashboard_subscribers"
    )

def message_list(request):

    search = request.GET.get("search", "")

    status = request.GET.get("status", "")

    messages = Inquiry.objects.all()

    if search:

        messages = messages.filter(

            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(subject__icontains=search) |
            Q(service__icontains=search)

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

def message_detail(request, pk):

    message = get_object_or_404(
        Inquiry,
        pk=pk
    )

    if message.status == "new":

        message.status = "read"

        message.save()

    return render(

        request,

        "dashboard/messages/message_detail.html",

        {

            "message": message

        }

    )

def message_reply(request, pk):

    message = get_object_or_404(
        Inquiry,
        pk=pk
    )

    message.status = "replied"

    message.save()

    return redirect(
        "dashboard_message_detail",
        pk=pk
    )

def message_delete(request, pk):

    message = get_object_or_404(
        Inquiry,
        pk=pk
    )

    if request.method == "POST":

        message.delete()

        return redirect(
            "dashboard_messages"
        )

    return render(

        request,

        "dashboard/messages/message_delete.html",

        {

            "message": message

        }

    )
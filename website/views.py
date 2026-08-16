from django.shortcuts import render,get_object_or_404,redirect
from portfolio.models import Project
from news.models import Blog
from django.db.models import Count,Q
from news.forms import SubscriberForm
from django.contrib import messages
from django.core.paginator import Paginator

def home(request):
    featured_projects = Project.objects.filter(

        featured=True,

        status="published"

    )[:6]

    return render(

        request,

        "home.html",

        {

            "featured_projects": featured_projects

        }

    )
def services(request):
    return render(request, "service-page.html")


def blog(request):

    search = request.GET.get("q", "")

    category = request.GET.get("category", "")

    blogs = Blog.objects.filter(
        status="published"
    )

    if search:

        blogs = blogs.filter(

            Q(title__icontains=search) |

            Q(excerpt__icontains=search) |

            Q(content__icontains=search)

        )

    if category:

        blogs = blogs.filter(
            category=category
        )

    featured_blog = blogs.filter(
        featured=True
    ).first()

    if featured_blog:

        blogs = blogs.exclude(
            id=featured_blog.id
        )

    categories = (

        Blog.objects.filter(
            status="published"
        )

        .exclude(category="")

        .values("category")

        .annotate(total=Count("id"))

        .order_by("category")

    )

    # Newsletter Form
    if request.method == "POST":

        subscriber_form = SubscriberForm(request.POST)

        if subscriber_form.is_valid():

            subscriber_form.save()

            return redirect("blog")

    else:

        subscriber_form = SubscriberForm()

    # Pagination
    paginator = Paginator(blogs, 6)   # 6 articles per page

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(

        request,

        "blog.html",

        {

            "featured_blog": featured_blog,

            "page_obj": page_obj,

            "categories": categories,

            "subscriber_form": subscriber_form,

            "search": search,

            "selected_category": category,

        }

    )
    
def blog_detail(request, slug):

    blog = get_object_or_404(
        Blog,
        slug=slug,
        status="published"
    )

    recent_posts = Blog.objects.filter(
        status="published"
    ).exclude(
        id=blog.id
    )[:3]

    return render(
        request,
        "blog_detail.html",
        {
            "blog": blog,
            "recent_posts": recent_posts
        }
    )

def contact(request):
    return render(request, "contact-page.html")

def project_detail(request, slug):

    project = get_object_or_404(

        Project,

        slug=slug,

        status="published"

    )

    related_projects = Project.objects.filter(
        status="published",
       industry=project.industry
    ).exclude(
      id=project.id
    )[:3]

    if related_projects.count() < 3:

       remaining = Project.objects.filter(
         status="published"
       ).exclude(
         id=project.id
       ).exclude(
          id__in=related_projects.values_list("id", flat=True)
       )[: 3 - related_projects.count()]

       related_projects = list(related_projects) + list(remaining)

    return render(

        request,

        "project_detail.html",

        {

            "project": project,

            "related_projects": related_projects,

        }

    )



def projects(request):

    projects = Project.objects.filter(
        status="published"
    ).order_by("-featured", "-created_at")

    return render(

        request,

        "projects-page.html",

        {

            "projects": projects

        }

    )
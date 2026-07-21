from django.shortcuts import render

def home(request):
    return render(request, "home.html")

def services(request):
    return render(request, "service-page.html")

def projects(request):
    return render(request, "projects-page.html")

def blog(request):
    return render(request, "blog-page.html")

def contact(request):
    return render(request, "contact-page.html")

def project_detail(request):
    return render(request, "project_detail.html")

def astron(request):
    return render(request,"astron.html")

def hbp(request):
    return render(request,"hbp_detail.html")

def quest(request):
    return render(request,"quest_detail.html")

def healing_mama_africa(request):
    return render(request,"healing_detail.html")

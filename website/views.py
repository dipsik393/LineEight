from django.shortcuts import render

def home(request):
    return render(request, "home.html")

def services(request):
    return render(request, "service-page.html")

def process(request):
    return render(request, "process.html")

def blog(request):
    return render(request, "blog-page.html")

def contact(request):
    return render(request, "contact-page.html")
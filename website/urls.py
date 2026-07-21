from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.services, name="services"),
    path("blog/", views.blog, name="blog"),
    path("contact/", views.contact, name="contact"),
    path("projects/", views.projects, name="projects"),
    path("projects/pase/", views.project_detail, name="pase"),
     path("astron/",views.astron,name="astron"),
     path("hbp/", views.hbp, name="hbp"),
    path("quest/", views.quest, name="quest"),
    path("healing-mama-africa/", views.healing_mama_africa, name="healing_mama_africa"),

]
from django.urls import include, path
from . import views

urlpatterns = [

    path("", views.dashboard, name="dashboard"),
    path("projects/", views.project_list, name="dashboard_projects"),
    path( "projects/create/",views.project_create,name="dashboard_project_create",),
    path("projects/<int:pk>/gallery/",views.project_gallery,name ="dashboard_gallery",),
     path(
        "projects/<int:id>/edit/",
        views.project_edit,
        name="dashboard_project_edit"
    ),

    path(
        "projects/<int:id>/delete/",
        views.project_delete,
        name="dashboard_project_delete"
    ),
    path(
    "gallery/<int:pk>/delete/",
    views.gallery_delete,
    name="dashboard_gallery_delete"
    ),
    path(
    "projects/<int:pk>/process/",
    views.project_process,
    name="dashboard_project_process",
    ),

    path(
    "process/edit/<int:pk>/",
    views.project_process_edit,
    name="dashboard_process_edit",
   ),

    path(
    "process/delete/<int:pk>/",
    views.project_process_delete,
    name="dashboard_process_delete",
    ),

    path(
    "blogs/",
    views.blog_list,
    name="dashboard_blogs",
    ),

    path(
      "blogs/create/",
     views.blog_create,
     name="dashboard_blog_create",
    ),

    path(
      "blogs/<int:id>/edit/",
      views.blog_edit,
      name="dashboard_blog_edit",
    ),

    path(
      "blogs/<int:id>/delete/",
      views.blog_delete,
       name="dashboard_blog_delete",
    ),
    path(
     "subscribers/",
     views.subscriber_list,
     name="dashboard_subscribers",
    ),

    path(
     "subscribers/<int:pk>/delete/",
     views.subscriber_delete,
     name="dashboard_subscriber_delete",
    ),

    path(
    "messages/",
    views.message_list,
    name="dashboard_messages",
    ),

   path(
    "messages/<int:pk>/",
    views.message_detail,
    name="dashboard_message_detail",
   ),

   path(
     "messages/<int:pk>/reply/",
     views.message_reply,
     name="dashboard_message_reply",
   ),

   path(
     "messages/<int:pk>/delete/",
     views.message_delete,
     name="dashboard_message_delete",
   ),
]
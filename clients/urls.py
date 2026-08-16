from django.urls import path

from . import views


urlpatterns = [

    path(
     "login/",
     views.staff_login,
     name="staff_login"
    ),

    # Dashboard

    path(
        "",
        views.client_list,
        name="dashboard_clients"
    ),

    path(
        "create/",
        views.client_create,
        name="dashboard_client_create"
    ),

    path(
        "<int:pk>/edit/",
        views.client_edit,
        name="dashboard_client_edit"
    ),

    path(
        "<int:pk>/delete/",
        views.client_delete,
        name="dashboard_client_delete"
    ),
    path(
      "projects/<int:project_id>/updates/",
      views.project_updates,
      name="project_updates"
    ),

    path(
      "projects/<int:project_id>/updates/create/",
      views.project_update_create,
      name="project_update_create"
    ),

    path(
     "<int:client_id>/projects/",
     views.dashboard_client_projects,
     name="dashboard_client_projects"
    ),

    path(
      "projects/<int:project_id>/files/",
      views.project_files,
      name="project_files"
    ),

    path(
      "projects/<int:project_id>/files/create/",
      views.project_file_create,
       name="project_file_create"
    ),

    path(
     "messages/",
     views.dashboard_messages,
     name="dashboard_messages"
    ),

   path(
     "messages/<int:pk>/",
     views.dashboard_message_detail,
     name="dashboard_message_detail"
    ),

    path(
     "messages/<int:pk>/delete/",
     views.dashboard_message_delete,
     name="dashboard_message_delete"
    ),
    path(
      "client-messages/",
     views.client_messages_dashboard,
     name="client_messages_dashboard"
    ),

    path(
     "messages/<int:pk>/view/",
     views.dashboard_inquiry_detail,
     name="dashboard_inquiry_detail"
    ),

    path(
     "messages/<int:pk>/delete/",
      views.dashboard_inquiry_delete,
      name="dashboard_inquiry_delete"
    ),

    path(
     "messages/<int:pk>/reply/",
      views.dashboard_inquiry_reply,
      name="dashboard_inquiry_reply"
    ),

    # Client Portal

    path(
        "portal/login/",
        views.client_login,
        name="client_login"
    ),

    path(
        "portal/logout/",
        views.client_logout,
        name="client_logout"
    ),

    path(
        "portal/dashboard/",
        views.client_dashboard,
        name="client_dashboard"
    ),
    path(
         "portal/projects/<int:pk>/",
          views.client_project_detail,
          name="client_project_detail"
    ),

    path(
      "portal/projects/<int:project_id>/messages/",
      views.client_messages,
      name="client_messages"
    ),
    path(
     "portal/projects/",
     views.client_projects,
     name="client_projects"
    ),
    path(
     "portal/files/",
     views.client_files,
     name="client_files"
    ),

    path(
     "portal/messages/",
     views.client_messages_list,
     name="client_messages_list"
    ),
    path(
     "portal/change-password/",
     views.client_change_password,
     name="client_change_password"
   ),
   path(
     "portal/files/<int:pk>/download/",
     views.client_file_download,
     name="client_file_download"
    ),

    

]

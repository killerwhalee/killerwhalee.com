from django.urls import path

from projects.id221 import views

app_name = "id221"

urlpatterns = [
    path("", views.index, name="index"),
    path("project-1", views.project_1, name="project-1"),
    path("project-2", views.project_2, name="project-2"),
    path("project-3", views.project_3, name="project-3"),
]

from django.urls import path, include

from projects import views
from projects.utils import list_projects

app_name = "projects"

# Construct url pattern for each projects
projects_url = [
    path(
        f"{project.name}/",
        include(f"projects.{project.name}.urls"),
    )
    for project in list_projects()
]

# Construct url patterns
urlpatterns = [path("", views.index, name="index"), *projects_url]

from django.urls import path

from channels.routing import URLRouter

from importlib import import_module

from projects.utils import list_projects

# Construct url pattern for each projects
websocket_urlpatterns = [
    path(
        f"{project.name}/",
        URLRouter(
            import_module(f"projects.{project.name}.routes").websocket_urlpatterns
        ),
    )
    for project in list_projects()
    if project.routes
]

from django.urls import path, include

from projects import views

app_name = "projects"

urlpatterns = [
    # Index url
    path("", views.index, name="index"),
    # User applications
    path(
        "interactive",
        include("projects.interactive.urls"),
    ),
    path(
        "omok",
        include("projects.omok.urls"),
    ),
]

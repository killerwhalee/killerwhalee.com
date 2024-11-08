from django.urls import path, include
from django.shortcuts import render

app_name = "projects"

urlpatterns = [
    # Index url
    path("", lambda _: render(_, "home/projects.html"), name="index"),
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

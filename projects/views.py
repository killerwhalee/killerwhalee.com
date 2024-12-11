from django.shortcuts import render

from pathlib import Path
import os


def index(request):
    # Get project name from project directory
    project_dir = Path(__file__).resolve().parent
    projects = [
        path
        for path in os.listdir(project_dir)
        if os.path.isdir(project_dir / path) and path != "__pycache__"
    ]

    context = {"projects": projects}
    print(context)

    return render(request, "home/projects.html", context)

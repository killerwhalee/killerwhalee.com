from django.shortcuts import render

from projects.utils import list_projects


def index(request):
    projects = list_projects()
    context = {"projects": projects}

    return render(request, "home/projects.html", context)

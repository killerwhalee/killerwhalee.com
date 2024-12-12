from django.shortcuts import render

from projects.utils import list_projects


def index(request):
    projects = list_projects()

    context = {"projects": projects}
    print(context)

    return render(request, "home/projects.html", context)

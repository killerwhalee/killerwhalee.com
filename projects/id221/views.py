from django.shortcuts import render


def index(request):
    return render(request, "projects/id221/index.html")


def project_1(request):
    return render(request, "projects/id221/project-1.html")


def project_2(request):
    return render(request, "projects/id221/project-2.html")


def project_3(request):
    return render(request, "projects/id221/project-3.html")

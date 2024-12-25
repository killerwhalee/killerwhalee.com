from django.shortcuts import render


def index(request):
    return render(request, "id221/index.html")


def project_1(request):
    return render(request, "id221/project_1.html")


def project_2(request):
    return render(request, "id221/project_2.html")


def project_3(request):
    return render(request, "id221/project_3.html")

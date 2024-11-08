from django.shortcuts import render

from home.models import FunFact


def splash(request):
    return render(request, "home/splash.html")


def index(request):
    fact = FunFact.objects.order_by("?")[0]
    context = {"fact": fact.fact}

    return render(request, "home/index.html", context)


def projects(request):
    return render(request, "home/projects.html")


def login(request):
    return render(request, "home/login.html")

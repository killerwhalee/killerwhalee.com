from django.shortcuts import render

from home.models import FunFact


def splash(request):
    return render(request, "home/splash.html")


def index(request):
    # Get random facts from database
    facts_q = FunFact.objects.order_by("?")
    fun_fact = facts_q[0] if facts_q.exists() else "아직 들려드릴 사실이 없습니다🥺"

    context = {"fact": fun_fact.fact}

    return render(request, "home/index.html", context)


def credit(request):
    return render(request, "home/credit.html")

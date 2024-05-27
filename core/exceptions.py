from django.shortcuts import render


def bad_request(request, exception):
    return render(request, "error/400.html", {})


def page_not_found(request, exception):
    return render(request, "error/404.html", {})


def server_error(request):
    return render(request, "error/500.html", {})

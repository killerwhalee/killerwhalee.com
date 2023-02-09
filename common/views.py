from django.shortcuts import render


def login(request):
    return render(request, 'common/login.html')

def signup(request):
    pass


# Error handling

def error400(request, exception):
    return render(request, 'error/400.html', {})

def error404(request, exception):
    return render(request, 'error/404.html', {})

def error500(request, exception):
    return render(request, 'error/500.html', {})
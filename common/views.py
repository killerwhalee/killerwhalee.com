from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import UserForm

def logout(request):
    pass

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        print("???")
    return redirect('/')

def terms(request):
    return render(request, 'common/terms.html')

def profile(request, username):
    return redirect("/")

# Error handling

def error400(request, exception):
    return render(request, 'error/400.html', {})

def error404(request, exception):
    return render(request, 'error/404.html', {})

def error500(request):
    return render(request, 'error/500.html', {})
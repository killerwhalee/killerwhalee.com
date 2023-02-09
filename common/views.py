from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, 'common/login.html')

def signup(request):
    pass
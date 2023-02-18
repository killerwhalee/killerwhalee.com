from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Explore
from .forms import ExploreForm

# Create your views here.
def explore(request, explore_id):
    return HttpResponse(explore_id)

def explore_gallery(request):
    explore_list = Explore.objects.order_by('explore_id')
    arguments = {'explore_list': explore_list}
    return render(request, 'explore/explore-index.html', arguments)

@login_required(login_url="/common/login")
def explore_create(request):
    if request.method == "POST":
        form = ExploreForm(request.POST)
        if form.is_valid():
            explore = form.save(commit=False)
            explore.explore_author = request.user
            explore.explore_date_created = timezone.now()
            explore.save()
            return redirect('/gallery')

    return render(request, 'explore/explore-create.html')

@login_required(login_url="/common/login")
def explore_edit(request, explore_id):
    return HttpResponse(f"{explore_id} - edit")
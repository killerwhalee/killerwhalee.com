from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Explore
from .forms import ExploreForm

# Create your views here.
def explore(request, explore_id):
    return HttpResponse(explore_id)

def explore_gallery(request):
    explore_list = Explore.objects.order_by('explore_id')
    arguments = {'explore_list': explore_list}
    return render(request, 'gallery/explore-index.html', arguments)

@login_required(login_url='common:login')
def explore_create(request):
    if request.method == 'POST':
        form = ExploreForm(request.POST, request.FILES)
        if form.is_valid():
            explore = form.save(commit=False)
            explore.explore_author = request.user
            explore.explore_date_created = timezone.now()
            explore.save()
            return redirect('gallery:explore-gallery')

    return render(request, 'gallery/explore-create.html')

@login_required(login_url='common:login')
def explore_edit(request, explore_id):
    explore = Explore.objects.get(explore_id=explore_id)
    arguments = {'explore': explore}
    
    if request.user != explore.explore_author:
        message.error(request, 'You are not allowed to edit this explore!')
        return redirect('gallery:explore-gallery')

    if request.method == 'POST':
        form = ExploreForm(request.POST, request.FILES, instance=explore)
        if form.is_valid():
            form.save()
            return redirect('gallery:explore-gallery')

    return render(request, 'gallery/explore-edit.html', arguments)

@login_required(login_url='common:login')
def explore_delete(request, explore_id):
    explore = Explore.objects.get(explore_id=explore_id)

    if request.user != explore.explore_author:
        message.error(request, 'You are not allowed to edit this explore!')
        return redirect('gallery:explore-gallery')

    explore.delete()
    return redirect('gallery:explore-gallery')

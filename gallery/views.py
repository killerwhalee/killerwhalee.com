from django.shortcuts import render
from django.http import HttpResponse
from .models import Explore

# Create your views here.
def explore(request, explore_id):
    return HttpResponse(explore_id)

def explore_gallery(request):
    explore_list = Explore.objects.order_by('explore_id')
    arguments = {'explore_list': explore_list}
    return render(request, 'explore/explore-index.html', arguments)

def explore_create(request):
    return HttpResponse("create!")

def explore_edit(request, explore_id):
    return HttpResponse(f"{explore_id} - edit")
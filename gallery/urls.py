from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'gallery'

urlpatterns = [
    path('', views.explore_gallery, name='explore-gallery'),
    path('<int:explore_id>/', views.explore, name='explore'),
    path('create/', views.explore_create, name='explore-create'),
    path('edit/<int:explore_id>/', views.explore_edit, name='explore-edit')
]
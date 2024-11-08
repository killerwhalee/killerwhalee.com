from django.urls import path

from home import views

app_name = "home"

urlpatterns = [
    path("", views.splash, name="splash"),
    path("home", views.index, name="index"),
]

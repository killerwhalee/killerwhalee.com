from django.urls import path

from projects.interactive import views

app_name = "interactive"

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>", views.room, name="room"),
]

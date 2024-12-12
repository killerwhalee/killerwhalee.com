from django.urls import path

from projects.id221 import views

app_name = "id221"

urlpatterns = [
    path("", views.index, name="index"),
]
